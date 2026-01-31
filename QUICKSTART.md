# Quick Start Guide

## Setup (One-time)

1. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API key:**

   ```bash
   # Copy the template
   cp .env.example .env
   
   # Edit .env and add your Google API key
   # GOOGLE_API_KEY=your_actual_api_key_here
   ```

   > Get a free API key at: <https://makersuite.google.com/app/apikey>

## Run Extraction

```bash
python src/extract_parameters.py
```

This will:

1. Read snippets from `input/` directory
2. Process each snippet with Gemini 1.5 Pro
3. Extract architectural parameters
4. Save results to `output/parameters.yaml`

## View Results

```bash
# Windows
type output\parameters.yaml

# Linux/Mac
cat output/parameters.yaml
```

## Project Structure

```text
.
├── README.md                    # Project overview
├── SUMMARY.md                   # Detailed summary report
├── QUICKSTART.md                # This file
├── requirements.txt             # Python dependencies
├── .env.example                 # API key template
│
├── input/                       # Input specification snippets
│   ├── snippet1_caches.txt
│   └── snippet2_csr.txt
│
├── src/                         # Source code
│   └── extract_parameters.py   # Main extraction script
│
├── output/                      # Generated results
│   ├── sample_parameters.yaml  # Example output
│   └── parameters.yaml         # Actual results (generated)
│
├── docs/                        # Documentation
│   ├── llm_details.md          # LLM specifications
│   └── methodology.md          # Technical approach
│
└── prompts/                     # Prompt engineering
    └── prompt_evolution.md     # Prompt development history
```

## Troubleshooting

### "No module named 'google.generativeai'"

```bash
pip install google-generativeai
```

### "API key not found"

Make sure you:

1. Created `.env` file (copy from `.env.example`)
2. Added your actual API key to `.env`
3. Running from project root directory

### "JSON parsing error"

The LLM occasionally returns malformed JSON. The script will print the error and continue. This is rare with temperature=0.1.

## Next Steps

- **Add more snippets:** Place new `.txt` files in `input/` directory
- **Modify prompts:** Edit the prompt in `src/extract_parameters.py`
- **Validate results:** Review `output/parameters.yaml` for accuracy
- **Read documentation:** See `docs/` for detailed methodology

## Support

For issues or questions:

1. Check `SUMMARY.md` for detailed documentation
2. Review `prompts/prompt_evolution.md` for prompt engineering insights
3. See `docs/methodology.md` for technical details
