# TinyGPT

A minimal, character-level GPT-style language model implemented from scratch in PyTorch, trained on the Tiny Shakespeare dataset. Everything — tokenizer, bigram baseline, self-attention, and training loop — lives in a single notebook: [main.ipynb](main.ipynb).

## Overview

The notebook builds up from a simple bigram model to a small decoder-only Transformer:

- **Character-level tokenizer** — vocabulary is just the unique characters in the dataset (65 for Shakespeare).
- **`BigramLanguageModel`** — a baseline that predicts the next character from only the current one.
- **`TinyGPT`** — a GPT-style model with token + positional embeddings, stacked Transformer blocks (multi-head self-attention + feed-forward), layer norm, and dropout.

### Model config

| Constant | Value | Description |
|---|---|---|
| `batch_size` | 32 | Sequences per training batch |
| `block_size` | 256 | Context length |
| `n_embd` | 128 | Embedding dimension |
| `n_head` | 4 | Attention heads |
| `n_layer` | 4 | Transformer blocks |
| `dropout` | 0.2 | Dropout rate |
| `learning_rate` | 3e-4 | AdamW learning rate |
| `max_iters` | 20000 | Training iterations |

Training uses mixed precision (`bfloat16`) and a fused AdamW optimizer on CUDA when available, falling back to CPU/float32 otherwise.

## Setup

```bash
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

Open [main.ipynb](main.ipynb) and run the cells in order. Training checkpoints (`checkpoint.pt` for TinyGPT, `bigram_checkpoint.pt` for the baseline) are saved periodically and auto-resumed if present. The final trained weights are saved to `tinygpt.pt`.

## Results

After 20,000 steps, `TinyGPT` reaches a train loss of ~1.31 and val loss of ~1.54 on Tiny Shakespeare, producing text with correct play-script structure (character names, dialogue formatting) and Shakespearean vocabulary, though not yet coherent at the sentence level:

```
ROMEO:
Well, my name counted his body.
Juliet wantil; by mew's thy still? O lock.

LADY CAPULET:
For but I'll displice.
```

## Data

The model is trained on the Tiny Shakespeare corpus (~1.1M characters), split 90/10 into train/validation sets. The corpus is not included in this repo; download it and place it as `data.txt` in this directory before running the notebook.

## Possible next steps

Training has plateaued at this config (val loss ~1.54, flat over the last several thousand steps). To push quality further:

- **Scale up the model** — more layers/heads/embedding dim (e.g. 6 layers, 6 heads, 384 embd) is the biggest lever for better samples.
- **LR schedule** — add warmup + cosine decay instead of a flat learning rate.
- **Longer training with a bigger model** — current `max_iters=20000` is enough to converge at this size; a larger model would need more steps too.
- **Switch to subword tokenization** (e.g. BPE) instead of character-level, for more semantically meaningful tokens.
