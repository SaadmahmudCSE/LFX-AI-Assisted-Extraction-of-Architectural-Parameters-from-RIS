# AI-Assisted Extraction of Architectural Parameters from RISC-V Specifications

## Overview

This project extracts architectural parameters from RISC-V ISA specification text using Large Language Models (LLMs). It identifies implementation-defined aspects using keyword patterns and structures results as YAML.

## Project Structure

```text
.
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── input/                       # Input specification snippets
│   ├── snippet1_caches.txt
│   └── snippet2_csr.txt
├── prompts/                     # Prompt development and refinement
│   └── prompt_evolution.md
├── src/                         # Source code
│   └── extract_parameters.py
├── output/                      # Generated results
│   └── parameters.yaml
└── docs/                        # Documentation
    ├── llm_details.md
    └── methodology.md
```

## Key Features

- Identifies parameters using keywords: "may/might/should", "optional/optionally", "implementation defined/specific"
- Extracts parameter name, description, type, and constraints
- Outputs structured YAML format
- Documents prompt engineering process and anti-hallucination strategies

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run extraction
python src/extract_parameters.py

# View results
cat output/parameters.yaml
```

## Challenge Requirements

✅ LLM details (name, version, context length)  
✅ Prompt development and refinement process  
✅ Anti-hallucination strategies  
✅ YAML-formatted results with required fields
