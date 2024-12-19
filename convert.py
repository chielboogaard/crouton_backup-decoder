from zipClass import ZipHandler
from croutonDecode import CroutonDecodeHandler
from pdfClass import RecipePDFHandler

import json
import os

FILEPATH = "Crouton Recipes - 19 Dec 2024.zip"
OUTPUTPATH = "output"


def main():
    zipClass = ZipHandler(zip_file_path=FILEPATH)

    croutons = zipClass.extract_croutonFiles()

    os.makedirs(OUTPUTPATH, exist_ok=True)

    for crouton in croutons:
        croutonClass = CroutonDecodeHandler(croutonFile=json.loads(crouton))

        instructions = croutonClass.get_instructions()
        ingredients = croutonClass.get_ingredients()
        recipeInfo = croutonClass.get_recipeInfo()

        print(instructions)
        recipe = {
                "title": recipeInfo.get("name"),
                "serves": recipeInfo.get("serves"),
                "image": recipeInfo.get("imagess", ""),
                "ingredients": ingredients,
                "instructions": instructions,
            }
        
        pdfClass = RecipePDFHandler(recipe, OUTPUTPATH, f"{recipeInfo.get("name")}.pdf")
        pdfClass.generate_pdf()
        
        # break
    return


if __name__ == "__main__":
    main()
