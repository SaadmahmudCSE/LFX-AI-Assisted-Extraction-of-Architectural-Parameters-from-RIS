# Methodology

## Approach Overview

This project uses a **prompt-based extraction** approach with Large Language Models (LLMs) to identify and extract architectural parameters from RISC-V specification text.

## Pipeline Architecture

```text
Input Snippets → Prompt Engineering → LLM Processing → JSON Parsing → YAML Output
```

### 1. Input Processing

- Specification snippets stored as plain text files
- Each snippet tagged with source reference (e.g., "Privileged Spec 19.3.1")
- Preserves original formatting and context

### 2. Prompt Engineering

- **Structured prompt** with clear role, definition, and instructions
- **Keyword grounding** to focus on indicator words
- **Anti-hallucination constraints** to ensure accuracy
- **JSON schema** for consistent output format

### 3. LLM Processing

- Uses Google Gemini 1.5 Pro with low temperature (0.1)
- Processes each snippet independently
- Generates structured JSON response

### 4. Validation & Parsing

- JSON validation and parsing
- Pydantic models for type safety
- Error handling for malformed responses

### 5. Output Generation

- Aggregates parameters from all snippets
- Outputs to YAML format with required fields
- Preserves source traceability

## Key Design Decisions

### Why Gemini 1.5 Pro?

1. **Large context window** (1M tokens) - can handle long specifications
2. **Strong technical reasoning** - understands architectural concepts
3. **JSON mode** - native structured output support
4. **Cost-effective** - good performance-to-cost ratio

### Why Low Temperature (0.1)?

- Minimizes creative interpretation
- Ensures grounded, deterministic responses
- Reduces hallucination risk
- Maintains consistency across runs

### Why JSON then YAML?

- **JSON for LLM:** Easier for models to generate correctly
- **YAML for output:** More human-readable final format
- Best of both worlds

## Parameter Identification Strategy

### Keyword-Based Detection

Parameters are identified by presence of:

- **Optionality:** "may", "might", "should", "optional", "optionally"
- **Implementation Freedom:** "implementation-specific", "implementation-defined"
- **Configurability:** "can be configured", "system-dependent"

### Contextual Analysis

Beyond keywords, the LLM considers:

- Statements about variability across implementations
- Mentions of discovery mechanisms (software querying hardware)
- Constraints that apply "in some implementations"

## Anti-Hallucination Strategies

### 1. Explicit Constraints in Prompt

```text
- "Identify ONLY parameters explicitly mentioned"
- "DO NOT invent parameters not mentioned in the text"
- "Use exact quotes where possible"
```

### 2. Evidence Requirement

- Request keywords that indicated each parameter
- Forces model to justify extractions
- Enables post-hoc validation

### 3. Low Temperature Configuration

- Temperature: 0.1 (very low)
- Prioritizes high-probability, grounded tokens
- Reduces creative elaboration

### 4. Structured Output Format

- JSON schema enforcement
- Required fields prevent omissions
- Easier to validate programmatically

### 5. Quote Grounding

- Descriptions should use exact text from snippet
- Reduces paraphrasing errors
- Maintains fidelity to source

## Validation Approach

### Automated Validation

1. **JSON Schema Validation:** Ensure all required fields present
2. **Keyword Verification:** Check that listed keywords exist in source text
3. **Type Consistency:** Validate type field values
4. **Source Traceability:** Verify source references are correct

### Manual Review

1. **Completeness Check:** Review source text for missed parameters
2. **Accuracy Check:** Verify extracted parameters are correct
3. **Precision Check:** Identify any false positives

## Limitations & Future Work

### Current Limitations

1. **Single-pass extraction:** No iterative refinement
2. **No cross-reference resolution:** Parameters mentioned across snippets not linked
3. **Limited context:** Each snippet processed independently
4. **Manual validation required:** No automated ground truth comparison

### Future Enhancements

1. **Multi-model consensus:** Use multiple LLMs and aggregate results
2. **Chain-of-thought prompting:** Ask model to explain reasoning
3. **Few-shot learning:** Provide annotated examples
4. **Hierarchical extraction:** Process entire sections with context
5. **Confidence scoring:** Request confidence levels for each parameter
6. **Interactive refinement:** Allow human-in-the-loop corrections

## Reproducibility

### Environment

- Python 3.8+
- google-generativeai SDK
- Deterministic model configuration (temperature=0.1)

### Versioning

- Model version: gemini-1.5-pro (latest as of Jan 2026)
- Prompt version: Documented in `prompts/prompt_evolution.md`
- Input data: Versioned in `input/` directory

### Running the Extraction

```bash
# Set up environment
pip install -r requirements.txt
cp .env.example .env
# Add your GOOGLE_API_KEY to .env

# Run extraction
python src/extract_parameters.py

# View results
cat output/parameters.yaml
```
