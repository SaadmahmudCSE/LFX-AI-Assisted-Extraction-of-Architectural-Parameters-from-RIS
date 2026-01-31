# LLM Details

## Model Information

### Primary Model: Google Gemini 2.0 Flash Lite

**Model Specifications:**

- **Name:** gemini-2.0-flash-lite-001
- **Version:** Latest stable experimental (as of January 2026)
- **Context Length:** ~1M tokens
- **Output Limit:** 8,192 tokens
- **Modality:** Text input/output
- **API:** Google AI Studio / Vertex AI

**Why Gemini 2.0 Flash?**

1. **Performance:** Significantly faster than Pro models
2. **Availability:** Currently accessible via standard API keys (unlike 1.5 Pro/Classic Pro in some regions)
3. **Structured Output:** Strong capability in following JSON schemas
4. **Efficiency:** Good balance of quality and rate limit usage

## Model Configuration

### Generation Parameters

```python
temperature=0.1      # Very low to minimize hallucinations
top_p=0.95          # Nucleus sampling for consistency
top_k=40            # Limit token selection
max_output_tokens=2048  # Sufficient for parameter extraction
```

### Rationale for Low Temperature

- Temperature of 0.1 ensures deterministic, grounded responses
- Reduces creative interpretation that could lead to hallucinations
- Maintains consistency across multiple runs

### Rate Limit Handling

The system implements exponential backoff retries to handle `429 Quota Exceeded` errors, which are common on the free tier.

## Alternative Models Considered

### OpenAI GPT-4 Turbo

- **Context Length:** 128K tokens
- **Pros:** Excellent instruction following, strong JSON output
- **Cons:** Higher cost, smaller context than Gemini 1.5 Pro
- **Use Case:** Could be used as validation/comparison

### Claude 3 Opus

- **Context Length:** 200K tokens
- **Pros:** Strong technical understanding, good at following constraints
- **Cons:** Higher latency, cost considerations
- **Use Case:** Alternative for complex specifications

## API Access

The implementation uses the `google-generativeai` Python SDK with API key authentication.
