# Grocery List Categorizer using Ollama

An intelligent tool that takes a raw grocery list and categorizes it using the power of Local LLMs via **Ollama**.

## 🧠 How it Works

- **LLM Context**: It uses a prompt to ask the model (e.g., `llama3` or `mistral`) to group items into categories like "Produce", "Dairy", "Pantry", etc.
- **Local Execution**: All processing happens on your machine.

## 🛠️ Setup

1.  **Install Ollama**: Download from [ollama.com](https://ollama.com).
2.  **Pull the Model**:
    ```bash
    ollama pull llama3  # or your preferred model
    ```

## 🚀 How to Run

1.  Add your items to `grocery_list.txt`.
2.  Run the categorizer:
    ```bash
    python main.py
    ```
3.  The results will be saved in `categorized_grocery_list.txt`.

## 📁 File Structure

- `main.py`: The Python script interacting with the Ollama API.
- `grocery_list.txt`: Input file containing the list of items.
- `categorized_grocery_list.txt`: Generated output file.
