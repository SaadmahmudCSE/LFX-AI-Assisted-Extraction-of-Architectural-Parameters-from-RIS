# Prompt Engineering Evolution

## Overview

This document tracks the development and refinement of prompts for extracting architectural parameters from RISC-V specifications.

## Iteration 1: Basic Extraction (Initial Attempt)

### Prompt (Iteration 1)

```text
Extract architectural parameters from this RISC-V specification text:
[snippet]
```

### Results (Iteration 1)

- **Issues:**
  - Too vague, led to over-extraction
  - Included non-parameters (e.g., standard definitions)
  - Inconsistent output format
  - Hallucinated parameters not in text

### Lessons Learned (Iteration 1)

- Need clear definition of what constitutes a "parameter"
- Must specify output format explicitly
- Should ground extraction in specific keywords

---

## Iteration 2: Keyword-Focused Extraction

### Prompt (Iteration 2)

```text
Extract parameters indicated by these keywords:
- "may", "might", "should"
- "optional", "optionally"
- "implementation-specific", "implementation-defined"

From this text:
[snippet]

Output as JSON with fields: name, description, type, constraints
```

### Results (Iteration 2)

- **Improvements:**
  - Better precision in identifying parameters
  - More consistent output format
  - Fewer hallucinations

- **Remaining Issues:**
  - Still some over-interpretation
  - Missing context about why something is a parameter
  - Type field often too generic

### Lessons Learned (Iteration 2)

- Keyword grounding works well
- Need to request evidence/quotes
- Should provide examples of good output

---

## Iteration 3: Structured with Examples (Current)

### Prompt Structure

1. **Role Definition:** "You are an expert in RISC-V architecture specifications"
2. **Clear Definition:** Explicit definition of what constitutes a parameter
3. **Keyword Grounding:** List specific indicator words
4. **Instructions:** Step-by-step extraction process
5. **Anti-Hallucination Rules:**
   - "Identify ONLY parameters explicitly mentioned"
   - "DO NOT invent parameters"
   - "Use exact quotes where possible"
6. **Output Format:** JSON schema with example
7. **Evidence Request:** Ask for keywords that indicated each parameter

### Full Prompt

```text
You are an expert in RISC-V architecture specifications. Your task is to extract architectural parameters from the following specification snippet.

DEFINITION: An architectural parameter is an aspect of the implementation that is:
- Implementation-specific or implementation-defined
- Optional or configurable
- Indicated by words like: "may", "might", "should", "optional", "optionally", "implementation-specific", "implementation-defined"

SNIPPET SOURCE: {source}

SNIPPET TEXT:
{snippet}

INSTRUCTIONS:
1. Identify ONLY parameters explicitly mentioned or strongly implied in the text
2. For each parameter, extract:
   - A short, descriptive name
   - A detailed description (use exact quotes where possible)
   - The type (integer, boolean, size, enumeration, etc.)
   - Any constraints or requirements mentioned
   - The specific keywords that indicated this is a parameter
3. DO NOT invent parameters not mentioned in the text
4. DO NOT make assumptions beyond what the text states
5. If a sentence mentions multiple related parameters, separate them

OUTPUT FORMAT (JSON):
[example JSON schema]

Now extract the parameters from the snippet above. Return ONLY valid JSON, no additional text.
```

### Results (Iteration 3)

- **Improvements:**
  - High precision and recall
  - Minimal hallucinations
  - Consistent, parseable output
  - Clear traceability (keywords field)

- **Metrics:**
  - Accuracy: ~95% (based on manual review)
  - False Positives: <5%
  - Format Compliance: 100%

---

## Anti-Hallucination Strategies

### 1. Low Temperature (0.1)

- Reduces creative interpretation
- Ensures deterministic output
- Prioritizes grounding in source text

### 2. Explicit Constraints

- "ONLY parameters explicitly mentioned"
- "DO NOT invent parameters"
- "Use exact quotes where possible"

### 3. Evidence Requirement

- Request keywords that indicated each parameter
- Forces model to justify extractions
- Enables validation of results

### 4. Structured Output

- JSON schema enforcement
- Reduces ambiguity in response format
- Easier to validate programmatically

### 5. Example-Driven

- Provide concrete example of expected output
- Shows desired level of detail
- Demonstrates proper formatting

### 6. Grounding in Keywords

- Explicit list of indicator words
- Focuses attention on relevant text
- Reduces over-interpretation

---

## Validation Approach

### Automated Checks

1. **JSON Validity:** Ensure parseable output
2. **Schema Compliance:** Verify all required fields present
3. **Keyword Verification:** Check that extracted keywords exist in source text
4. **Quote Verification:** Validate that descriptions contain text from snippet

### Manual Review

1. **Completeness:** Did we miss any parameters?
2. **Accuracy:** Are extracted parameters correct?
3. **Precision:** Are there false positives?

---

## Future Improvements

### Potential Enhancements

1. **Multi-Model Validation:** Use GPT-4 or Claude to validate Gemini results
2. **Chain-of-Thought:** Ask model to explain reasoning before extraction
3. **Few-Shot Learning:** Provide multiple examples from other specs
4. **Iterative Refinement:** Two-pass approach (extract, then validate)
5. **Confidence Scores:** Request confidence level for each parameter

### Handling Edge Cases

- **Implicit Parameters:** Parameters implied but not explicitly stated
- **Conditional Parameters:** Parameters that depend on other choices
- **Deprecated Parameters:** Historical parameters no longer recommended
