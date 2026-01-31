import os
import json
import logging
import google.generativeai as genai
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


class Parameter(BaseModel):
    """Model for an architectural parameter"""
    name: str = Field(description="Short, descriptive name for the parameter")
    description: str = Field(description="Detailed description of what this parameter controls")
    type: str = Field(description="Data type or category (e.g., 'integer', 'boolean', 'enumeration', 'size')")
    constraints: str = Field(description="Any constraints, ranges, or requirements")
    source: str = Field(description="Source specification section")
    keywords: List[str] = Field(description="Keywords that indicated this parameter")


class ParameterExtractor:
    """Extracts architectural parameters from RISC-V specification text"""
    
    def __init__(self, model_name: str = "gemini-2.0-flash-lite-001"):
        """
        Initialize the extractor with specified model
        
        Args:
            model_name: Name of the Gemini model to use
        """
        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name
        
    def create_extraction_prompt(self, snippet: str, source: str) -> str:
        """
        Create the extraction prompt for the LLM
        
        This prompt has been refined to:
        1. Focus on specific keywords indicating parameters
        2. Request structured output
        3. Minimize hallucinations by grounding in text
        4. Request evidence/quotes for each parameter
        """
        prompt = f"""You are an expert in RISC-V architecture specifications. Your task is to extract architectural parameters from the following specification snippet.

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
Return a JSON array of objects, each with these fields:
- name: string
- description: string
- type: string
- constraints: string
- keywords: array of strings

EXAMPLE OUTPUT:
[
  {{
    "name": "cache_block_size",
    "description": "The size of a cache block, which must be uniform throughout the system",
    "type": "size",
    "constraints": "Must be uniform throughout the system; power-of-two or NAPOT aligned",
    "keywords": ["implementation-specific", "shall"]
  }}
]

Now extract the parameters from the snippet above. Return ONLY valid JSON, no additional text.
"""
        return prompt
    
    def extract_parameters(self, snippet: str, source: str) -> List[Parameter]:
        """
        Extract parameters from a specification snippet
        
        Args:
            snippet: The specification text
            source: The source reference (e.g., "Privileged Spec 19.3.1")
            
        Returns:
            List of extracted parameters
        """
        prompt = self.create_extraction_prompt(snippet, source)
        
        # Generate response
        try:
            retry_count = 0
            max_retries = 3
            import time
            
            while retry_count <= max_retries:
                try:
                    response = self.model.generate_content(
                        prompt,
                        generation_config=genai.GenerationConfig(
                            temperature=0.1,  # Low temperature to reduce hallucinations
                            top_p=0.95,
                            top_k=40,
                            max_output_tokens=2048,
                        )
                    )
                    break
                except Exception as e:
                    if "429" in str(e) and retry_count < max_retries:
                        logging.warning(f"Rate limit hit. Retrying in {2 ** retry_count * 5} seconds...")
                        time.sleep(2 ** retry_count * 5)
                        retry_count += 1
                        continue
                    else:
                        raise e
            
            # Parse JSON response
            import json
            try:
                # Extract JSON from response (handle markdown code blocks)
                response_text = response.text.strip()
                if response_text.startswith('```'):
                    # Remove markdown code block markers
                    lines = response_text.split('\n')
                    # Find start and end of code block
                    start = 0
                    if lines[0].startswith('```'):
                         start = 1
                    end = len(lines)
                    if lines[-1].strip() == '```':
                         end = -1
                    response_text = '\n'.join(lines[start:end])
                
                params_data = json.loads(response_text)
                logging.info(f"DEBUG: Parsed {len(params_data)} parameters from {source}")
                if len(params_data) == 0:
                    logging.info(f"DEBUG: Empty parameters. Raw response: {response_text}")
                
                # Convert to Parameter objects
                parameters = []
                for param_dict in params_data:
                    param_dict['source'] = source
                    parameters.append(Parameter(**param_dict))
                
                return parameters
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON response: {e}")
                print(f"Response text: {response.text}")
                return []
        except Exception as e:
            logging.error(f"Error generating content: {e}")
            if 'response' in locals() and hasattr(response, 'text'):
                logging.error(f"Raw response: {response.text}")
            return []

    def save_to_yaml(self, parameters: List[Parameter], output_path: str):
        """
        Save extracted parameters to YAML file (manually to avoid dependencies)
        
        Args:
            parameters: List of parameters to save
            output_path: Path to output YAML file
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("parameters:\n")
            for param in parameters:
                f.write(f"  - name: {param.name}\n")
                # Handle multiline descriptions nicely
                desc = param.description.replace('"', '\\"')
                f.write(f"    description: \"{desc}\"\n")
                f.write(f"    type: {param.type}\n")
                # Handle multiline constraints
                const = param.constraints.replace('"', '\\"')
                f.write(f"    constraints: \"{const}\"\n")
                f.write(f"    source: {param.source}\n")
                f.write("    keywords:\n")
                for keyword in param.keywords:
                    f.write(f"      - {keyword}\n")
                f.write("\n")
        
        print(f"Saved {len(parameters)} parameters to {output_path}")



def main():
    """Main execution function"""
    # Setup logging
    logging.basicConfig(filename='extraction.log', level=logging.INFO, format='%(asctime)s - %(message)s', filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)
    
    logging.info("RISC-V Architectural Parameter Extraction")
    logging.info("=" * 50)
    
    # Initialize extractor
    extractor = ParameterExtractor(model_name="gemini-2.0-flash-lite-001")
    logging.info(f"Using model: {extractor.model_name}")
    
    # Define input snippets
    snippets = [
        {
            'file': 'input/snippet1_caches.txt',
            'source': 'Privileged Spec 19.3.1'
        },
        {
            'file': 'input/snippet2_csr.txt',
            'source': 'Privileged Spec 2.1'
        }
    ]
    
    # Extract parameters from all snippets
    all_parameters = []
    
    for snippet_info in snippets:
        print(f"Processing: {snippet_info['source']}")
        
        # Read snippet
        with open(snippet_info['file'], 'r') as f:
            snippet_text = f.read()
        
        # Extract parameters
        parameters = extractor.extract_parameters(snippet_text, snippet_info['source'])
        all_parameters.extend(parameters)
        
        print(f"  Found {len(parameters)} parameters")
        for param in parameters:
            print(f"    - {param.name}")
        print()
    
    # Save to YAML
    output_path = 'output/parameters.yaml'
    extractor.save_to_yaml(all_parameters, output_path)
    
    print(f"\nTotal parameters extracted: {len(all_parameters)}")
    print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    main()
