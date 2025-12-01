# crouton_backup-decoder

## Introduction

**crouton_backup-decoder** is a Python tool that extracts and converts recipe data from Crouton backup files into formatted PDF documents. It allows users to extract recipes from ZIP archives containing Crouton recipe files, parse the recipe information, and generate beautiful, printable PDF documents for each recipe.

This project is perfect for users who want to preserve their Crouton recipe collections in a portable, offline format.

## Features

- ZIP Archive Extraction
- Recipe Data Parsing
- **PDF Generation**
  - Recipe images
  - Ingredient lists with quantities
  - Detailed cooking instructions
  - Multi-page support for longer recipes

## Setup

### Requirements

- Python 3.7+

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd crouton_backup-decoder
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare your Crouton backup file**:
   - Place your Crouton Recipes backup ZIP file in the project directory
   - Update the `FILEPATH` variable in `convert.py` with your backup file path

### Usage

Run the conversion script:
```bash
python convert.py
```

The script will:
1. Extract recipes from your Crouton backup ZIP file
2. Parse each recipe's metadata, ingredients, and instructions
3. Generate PDF files for each recipe in the `output/` directory

### Project Structure

- `convert.py` - Main script that orchestrates the extraction and conversion process
- `zip_class.py` - Handles ZIP file extraction and iteration
- `crouton_decode_class.py` - Parses Crouton recipe JSON format
- `pdf_class.py` - Generates formatted PDF documents
- `requirements.txt` - Python package dependencies 