import ollama
import os 
import re

MODEL = "qwen3:8b"
OUTPUT_FILE = "data/categorized_grocery_list.txt"
INPUT_FILE = "data/grocery_list.txt"

# Ensure the input file exists
if not os.path.exists(INPUT_FILE):
    print(f"Input file '{INPUT_FILE}' does not exist.")
    exit(1)

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

with open(INPUT_FILE, "r") as file:
    grocery_list = file.read().strip()

PROMPT_TEMPLATE = """
You are a precise and literal assistant that categorizes grocery items without assumptions.

Here is a grocery list:
{grocery_list}

Instructions:
1. Categorize each item into exactly one of these categories:
   - Fruits
   - Vegetables
   - Dairy
   - Meat
   - Grains
   - Snacks
   - Beverages
   - Frozen Foods
   - Condiments
   - Other

2. Use **only the items provided**. Do not add or imply missing items (e.g., don’t add “Oranges” for “Orange Juice”).

3. Sort items alphabetically within each category.

4. Format the output exactly as:
   CategoryName:
   1. Item1
   2. Item2
   ...
   If no items exist in a category, write `None`.

Now, provide the categorized and alphabetized grocery list:
"""

try:
    response = ollama.generate(
        model=MODEL,
        prompt=PROMPT_TEMPLATE.format(grocery_list=grocery_list)
    )
    generated_text = response.get("response", "")
    generated_text = re.sub(r"<think>.*?</think>", "", generated_text, flags=re.DOTALL).strip()
    
    print("==== Categorized List: ====\n")
    print(generated_text.strip())

    with open(OUTPUT_FILE, "w") as output_file:
        output_file.write(generated_text.strip())

    print(f"\n✅ Categorized grocery list saved to '{OUTPUT_FILE}'.")
except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)