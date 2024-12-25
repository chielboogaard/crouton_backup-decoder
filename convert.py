# Use the data from the crouton file to generate a PDF file with the recipe information
from zip_class import ZipHandler
from crouton_decode_class import CroutonDecodeHandler
from pdf_class import RecipePDFHandler

import json
import os

# Define the file paths for the ZIP file and the output folder
FILEPATH = "Crouton_Recipes"
if not os.path.exists(FILEPATH):
    raise FileNotFoundError(f"File not found: {FILEPATH}")
OUTPUTPATH = "output"


def main():
    # Create a ZipHandler instance and extract the crouton files
    zip = ZipHandler(zip_file_path=FILEPATH)
    # Extract the crouton files from the ZIP file
    croutons = zip.extract_croutonFiles()
    # Create the output folder if it doesn't exist
    os.makedirs(OUTPUTPATH, exist_ok=True)

    # Iterate over the crouton files and process each recipe
    for recipe in croutons:
        # used to decode the JSON object representing a recipe
        crouton = CroutonDecodeHandler(croutonFile=json.loads(recipe))
        # Extract the recipe information
        recipeInfo = crouton.get_recipeInfo()
        # Extract the recipe ingredients and instructions
        recipeData = {
                "title": recipeInfo.get("name"),
                "serves": recipeInfo.get("serves"),
                "image": recipeInfo.get("imagess", ""),
                "ingredients": crouton.get_ingredients(),
                "instructions": crouton.get_instructions(),
            }
        
        # Generate a PDF file for the recipe
        pdf = RecipePDFHandler(recipeData, OUTPUTPATH, f"{recipeInfo.get("name")}.pdf")
        pdf.generate_pdf()
        
        # break
    return


if __name__ == "__main__":
    main()
