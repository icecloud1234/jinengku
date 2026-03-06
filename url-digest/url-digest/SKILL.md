---
name: url-digest
description: Extract and structure key information from web pages using web fetch. Use when the user asks to analyze, summarize, or extract insights from URLs with structured output (key points, risks, action items). Ideal for queries like "summarize this URL", "what are the main points from this page", or "analyze this article".
---

# URL Digest

Extract and structure key information from web pages into actionable digests.

## When to use

Use this skill when users request:
- "Summarize this URL with key points"
- "What are the main takeaways from this page?"
- "Analyze this article and tell me what to do next"
- "Give me a structured summary of this link"
- Any request to extract structured insights from a URL

## Standard digest format

When processing a URL, use the fetch_content tool to retrieve the page content, then analyze it and present results in this structure:

### 📋 Key Points (5 items)
1. [Most important insight]
2. [Second key point]
3. [Third key point]
4. [Fourth key point]
5. [Fifth key point]

### ⚠️ Risks & Considerations (3 items)
1. [Potential risk or limitation]
2. [Important caveat or concern]
3. [Notable warning or constraint]

### ✅ Next Steps (up to 3 items)
1. [Recommended immediate action]
2. [Follow-up task if applicable]
3. [Additional action if relevant]

## Handling difficult pages

If the page fails to load or is blocked:

1. **Try alternative approaches**:
   - Use fetch_content with the URL directly
   - If blocked, try searching for the page title or content

2. **Suggest alternatives**: Recommend publicly accessible alternatives:
   - GitHub READMEs
   - Public documentation sites
   - PDF versions (if available)
   - Archive.org snapshots
   - Cached versions

3. **Inform the user**: Clearly explain the issue and what alternatives were tried

## Examples

**User request:**
> "总结这个页面：https://github.com/features。输出：1) 5 条要点 2) 3 个风险/注意事项 3) 我下一步该做什么（最多 3 条）"

**Response:**
1. Use fetch_content to retrieve the page: `https://github.com/features`
2. Analyze the content and extract key information
3. Present in structured format:

### 📋 Key Points
1. GitHub provides AI-powered coding assistance through Copilot
2. Integrated CI/CD with Actions for automated workflows
3. Advanced security scanning and dependency management
4. Collaborative code review tools with pull requests
5. Project management features including issues and boards

### ⚠️ Risks & Considerations
1. Copilot requires separate subscription for full features
2. Actions minutes are limited on free tier
3. Advanced security features only available on paid plans

### ✅ Next Steps
1. Evaluate which features align with your team's needs
2. Review pricing tiers if advanced features are required
3. Set up a trial repository to test key features

## Output customization

Adjust the analysis depth based on user needs:

- **Shorter summary**: Focus on the most critical 3 key points
- **More detailed**: Expand to more than 5 key points if content is rich
- **Specific focus**: If user asks about specific aspects, prioritize those in the analysis
- **Technical level**: Adjust language complexity based on the page content and user's apparent expertise

## Tips

- Use fetch_content tool to retrieve web page content
- Analyze the fetched content thoroughly before structuring the digest
- Adapt the number of points/risks/steps if the content is minimal or extensive
- If the page is very technical, adjust language to match user's expertise level
- Extract actionable insights rather than just summarizing facts
- Focus on what matters most to the user's likely goals
