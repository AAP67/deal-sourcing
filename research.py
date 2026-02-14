import json
import time
import anthropic


def _call_with_retry(client, max_retries=3, status_callback=None, **kwargs):
    """Call Claude API with automatic retry on rate limits."""
    for attempt in range(max_retries):
        try:
            return client.messages.create(**kwargs)
        except anthropic.RateLimitError as e:
            wait_time = 60 * (attempt + 1)
            if status_callback:
                status_callback(f"⏳ Rate limited — waiting {wait_time}s before retry ({attempt + 1}/{max_retries})...")
            time.sleep(wait_time)
            if attempt == max_retries - 1:
                raise
        except anthropic.APIError as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                wait_time = 60 * (attempt + 1)
                if status_callback:
                    status_callback(f"⏳ Rate limited — waiting {wait_time}s before retry ({attempt + 1}/{max_retries})...")
                time.sleep(wait_time)
                if attempt == max_retries - 1:
                    raise
            else:
                raise


def build_prompt(industry: str, stages: list[str], geo: str, kpis: list[str], result_count: int) -> str:
    return f"""You are a VC analyst doing deal sourcing research. Find {result_count} real startups/companies that match the following investment criteria:

**Industry:** {industry}
**Stages:** {', '.join(stages)}
**Geography:** {geo}
**Scoring KPIs:**
{chr(10).join(f'- {kpi}' for kpi in kpis)}

CRITICAL RULES:
1. ONLY return companies at these EXACT stages: {', '.join(stages)}. Do NOT include companies at any other stage. If the user selected "Seed", do not return Series A, B, C, or Growth companies. If the user selected "Series A", do not return Seed, Series B, C, or Growth companies. This is the #1 most important rule.
2. RECENCY REQUIREMENTS:
   - Funding rounds MUST be within the last 6 months. Do not include companies whose last round was more than 6 months ago.
   - Traction data (revenue, user growth, hiring, partnerships) MUST be from the last 6 months.
   - News and press mentions used as signals MUST be from the last 6 months.
   - Founder backgrounds, founding date, technical moat, patents, and accelerator history CAN be older — these are historical facts.
3. Search the web thoroughly for real companies matching these criteria. Use multiple searches.
4. Score each company 0-100 ONLY against the specific KPIs listed above. A company that matches all KPIs well should score 85+. A company matching few should score below 60.
5. Focus on companies that are actively operating and have verifiable information online.
6. Look at Crunchbase, TechCrunch, PitchBook summaries, Product Hunt, LinkedIn, Y Combinator, and other startup databases.
7. For geography "{geo}", only include companies operating in that region. If "Global", any region is fine.

Return ONLY a valid JSON array with exactly {result_count} objects. No markdown, no explanation, no code fences. Each object must have:
{{
  "name": "Company Name",
  "domain": "company.com",
  "stage": "Must be one of: {', '.join(stages)}",
  "location": "City, Country",
  "founded": "2024",
  "last_round": "$XM Stage · Mon YYYY",
  "founders": "Brief founder background",
  "rationale": "ONE sentence only, max 30 words. Why this is a good investment based on the KPIs.",
  "kpi_match": 85,
  "signals": ["2-4 word tag", "2-4 word tag", "2-4 word tag"],
  "source": "Where you found this info"
}}

FORMATTING RULES:
- "rationale" MUST be exactly ONE sentence, no longer than 30 words. Not a paragraph.
- "signals" MUST be short tags of 2-4 words each like "YC W24", "GitHub trending", "$2M ARR", "Repeat founder". NOT full sentences.
- Maximum 3 signals per company.
- For geography "Global", ensure results span at LEAST 3 different countries/regions. Do NOT return all US companies.

REMINDER: The "stage" field MUST be one of [{', '.join(stages)}]. Any other stage is WRONG.

Return ONLY the JSON array. No other text."""


def research_deals(
    api_key: str,
    industry: str,
    stages: list[str],
    geo: str,
    kpis: list[str],
    result_count: int,
    status_callback=None,
) -> list[dict]:
    """Call Claude API with web search to find real startup deals."""

    client = anthropic.Anthropic(api_key=api_key)

    prompt = build_prompt(industry, stages, geo, kpis, result_count)

    if status_callback:
        status_callback("🔍 Constructing research queries...")

    response = _call_with_retry(
        client,
        status_callback=status_callback,
        model="claude-haiku-4-5-20251001",
        max_tokens=4000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}],
    )

    if status_callback:
        status_callback("🌐 Scanning startup databases & news...")

    # Extract text from response - handle multi-block responses from tool use
    full_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            full_text += block.text

    # If we got tool use but no final text, we need to continue the conversation
    tool_use_blocks = [b for b in response.content if b.type == "tool_use"]

    if tool_use_blocks and not full_text.strip():
        messages = [{"role": "user", "content": prompt}]
        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in tool_use_blocks:
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": "Search completed successfully.",
                }
            )
        messages.append({"role": "user", "content": tool_results})

        if status_callback:
            status_callback("👤 Analyzing founder backgrounds...")

        response = _call_with_retry(
            client,
            status_callback=status_callback,
            model="claude-haiku-4-5-20251001",
            max_tokens=4000,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=messages,
        )

        full_text = ""
        for block in response.content:
            if hasattr(block, "text"):
                full_text += block.text

    if status_callback:
        status_callback("📊 Scoring against your KPIs...")

    # Parse JSON from response
    results = _parse_results(full_text)

    # Post-process: strictly filter to only selected stages
    allowed_stages_lower = [s.lower() for s in stages]
    results = [r for r in results if r["stage"].lower() in allowed_stages_lower]

    if status_callback:
        status_callback(f"✅ Found {len(results)} deals matching your criteria!")

    return results


def _parse_results(text: str) -> list[dict]:
    """Extract and parse JSON results from Claude's response."""
    text = text.strip()

    # Remove markdown code fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    if text.startswith("json"):
        text = text[4:].strip()

    # Try to find JSON array in the text
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1:
        text = text[start : end + 1]

    try:
        results = json.loads(text)
        if isinstance(results, list):
            return _validate_results(results)
    except json.JSONDecodeError:
        pass

    return []


def _validate_results(results: list) -> list[dict]:
    """Ensure each result has required fields with defaults."""
    validated = []
    required_fields = {
        "name": "Unknown",
        "domain": "N/A",
        "stage": "Unknown",
        "location": "Unknown",
        "founded": "N/A",
        "last_round": "N/A",
        "founders": "N/A",
        "rationale": "No rationale provided",
        "kpi_match": 50,
        "signals": [],
        "source": "Web search",
    }

    for item in results:
        if not isinstance(item, dict):
            continue
        validated_item = {}
        for field, default in required_fields.items():
            validated_item[field] = item.get(field, default)
        # Clamp kpi_match
        validated_item["kpi_match"] = max(0, min(100, int(validated_item["kpi_match"])))
        # Ensure signals is a list
        if not isinstance(validated_item["signals"], list):
            validated_item["signals"] = [str(validated_item["signals"])]
        validated.append(validated_item)

    # Sort by kpi_match descending
    validated.sort(key=lambda x: x["kpi_match"], reverse=True)
    return validated
