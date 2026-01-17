import ollama
import os 
import re
import shutil
import subprocess

MODEL = "llama3.2:latest"
OUTPUT_FILE = "categorized_grocery_list.txt"
INPUT_FILE = "grocery_list.txt"

# Ensure the input file exists
if not os.path.exists(INPUT_FILE):
    print(f"Input file '{INPUT_FILE}' does not exist.")
    exit(1)

# Ensure output directory exists
# os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

with open(INPUT_FILE, "r") as file:
    grocery_list = file.read().strip()

PROMPT_TEMPLATE = """
You are a strict, literal grocery categorization assistant.
You must follow the rules EXACTLY. Any violation is incorrect.

Grocery List:
{grocery_list}

Rules:
1. Each item must be placed in exactly one category:
   Fruits, Vegetables, Dairy, Meat, Grains, Snacks,
   Beverages, Frozen Foods, Condiments, Other.

2. Use only items explicitly provided.
   Do not rename, infer, expand, or correct items.

3. Categorize by common grocery-store usage only.

4. Sort items alphabetically (A–Z) within each category.

5. Output format must be EXACT:
CategoryName:
    1. Item
    2. Item

6. If a category has no items:
CategoryName:
    None

7. Do not repeat items across categories.

Return ONLY the categorized list.
"""



def ensure_ollama_running():
    """Ensure Ollama CLI is installed and the daemon is reachable."""
    if not shutil.which("ollama"):
        raise RuntimeError("Ollama CLI not found. Install from https://ollama.com/download")
    try:
        proc = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
    except Exception as e:
        raise RuntimeError(f"Failed to run 'ollama list': {e}") from e
    if proc.returncode != 0 or "could not connect" in (proc.stderr or "").lower():
        raise RuntimeError(
            "Ollama CLI found but not connected to a running instance. "
            "Start the Ollama desktop app or daemon and try again. See https://ollama.com/docs/get-started"
        )

try:
    ensure_ollama_running()
    response = ollama.generate(
    model=MODEL,
    prompt=PROMPT_TEMPLATE.format(grocery_list=grocery_list),
    options={
        "temperature": 0.0,
        "top_p": 0.1,
        "repeat_penalty": 1.1
    }
    )
    generated_text = response.get("response", "")
    generated_text = re.sub(r"<tool_call>.*?<tool_call>", "", generated_text, flags=re.DOTALL).strip()

    print("==== Categorized List: ====\n")
    print(generated_text.strip())

    with open(OUTPUT_FILE, "w") as output_file:
        output_file.write(generated_text.strip())

    print(f"\n✅ Categorized grocery list saved to '{OUTPUT_FILE}'.")
except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)