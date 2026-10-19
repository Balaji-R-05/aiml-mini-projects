# arXiv Power Distribution Paper Collector

A Jupyter notebook that collects arXiv papers matching the search phrase **"power distribution"**, downloads their PDFs, and records paper metadata in an Excel spreadsheet.

## Project contents

- `arxiv_scraper.ipynb` - Searches arXiv and processes paper pages in batches.
- `arxiv_links_power_distribution.txt` - Collected arXiv abstract-page URLs.
- `processed_links.txt` - URLs already processed by the notebook.
- `arxiv_data.xlsx` - Spreadsheet index containing each paper's title, abstract, URL, date, authors, and PDF filename.
- `pdfs/` - Downloaded paper PDFs.

## Requirements

- Python
- Jupyter support in your editor or a Jupyter installation
- Google Chrome (used by Selenium to load arXiv pages)

Install the notebook's Python dependencies from a terminal:

```bash
python -m pip install selenium pandas beautifulsoup4 openpyxl requests
```

Selenium uses Chrome to browse arXiv. Ensure Chrome is installed and available; Selenium Manager may download or locate the matching driver when needed.

## Run the scraper

1. Open `arxiv_scraper.ipynb` and select a Python kernel with the dependencies installed.
2. Run the first code cell to search arXiv and write results to `arxiv_links_power_distribution.txt`.
3. Run the next code cell to process up to 20 links that are not already in `processed_links.txt`.
4. Run that processing cell again to continue with later links.

The processing cell creates or updates `arxiv_data.xlsx`, saves PDFs in `pdfs/`, and appends successfully processed abstract-page URLs to `processed_links.txt`. Keep these files in the notebook's working directory. The scraper makes network requests to arXiv and may take time to process a batch.