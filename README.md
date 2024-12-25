# Crouton Backup Decoder

This Python project extracts crouton recipe files from a ZIP archive, decodes the recipe data, and generates a PDF for each recipe. The generated PDFs contain the recipe's title, ingredients, instructions, and additional details such as servings and images.

## Features

- Extracts recipe files from a ZIP archive.
- Decodes recipe data stored in JSON format.
- Generates PDF files for each recipe.
- Saves the PDFs in a specified output directory.

## Requirements

- Python 3.7 or higher
- Required Python libraries:
  - `json`
  - `os`
  - `reportlab`
  - `shutil`

## Setup

1. **Clone the repository** to your local machine:
```bash
git clone https://github.com/your-username/crouton-recipe-pdf-converter.git

cd crouton-recipe-pdf-converter
```

2. **install the required packages** to your machine
```bash
pip install reportlab
```
or 
```bash
pip install -r requirements.txt
```