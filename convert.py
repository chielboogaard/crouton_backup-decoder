from zipClass import ZipHandler
from croutonDecodeClass import CroutonDecodeHandler
from pdfClass import RecipePDFHandler

import json
import os

FILEPATH = "Crouton Recipes - 19 Dec 2024.zip"
OUTPUTPATH = "output"


def main():
    zip = ZipHandler(zip_file_path=FILEPATH)

    croutons = zip.extract_croutonFiles()

    os.makedirs(OUTPUTPATH, exist_ok=True)

    for recipe in croutons:
        crouton = CroutonDecodeHandler(croutonFile=json.loads(recipe))

        recipeInfo = crouton.get_recipeInfo()

        recipeData = {
                "title": recipeInfo.get("name"),
                "serves": recipeInfo.get("serves"),
                "image": recipeInfo.get("imagess", ""),
                "ingredients": crouton.get_ingredients(),
                "instructions": crouton.get_instructions(),
            }
        
        pdf = RecipePDFHandler(recipeData, OUTPUTPATH, f"{recipeInfo.get("name")}.pdf")
        pdf.generate_pdf()
        
        # break
    return


if __name__ == "__main__":
    main()
