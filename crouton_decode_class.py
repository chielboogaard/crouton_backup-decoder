import os
import json


class CroutonDecodeHandler:
    def __init__(self, croutonFile):
        """
        Initialize the ZipHandler with the ZIP file path and target extraction folder.
        """
        self.croutonFile = croutonFile

    def convert_quantity(self, quantityAmount: int, quantityType: str):
        """
        Convert the quantity name in the crouton format to a logical unit name
        Also add the amount
        """
        if quantityType == "SECTION":
            return "--section--"
        suffix_map = {
            "ITEM": "",
            "GRAMS": "gr",
            "MILLS": "ml",
            "CUP": "cup",
            "TABLESPOON": "tbsp",
            "TEASPOON": "tsp",
            "SECTION": ""
        }
        suffix = suffix_map.get(quantityType, "???")
        return f"{quantityAmount}{suffix}"

    def get_ingredients(self):
        """
        Process the json in the crouton file and format it to:
        [{"name": "Example ingredient", "quantity": "999"}]
        """
        ingredients = []
        try:
            for ingredient in self.croutonFile.get("ingredients", []):
                # get the quantity type name
                quantity_data = ingredient.get("quantity", {})
                amount = quantity_data.get("amount", 1)
                quantityType = quantity_data.get("quantityType", "ITEM")

                quantity = self.convert_quantity(
                    quantityAmount=amount,
                    quantityType=quantityType,
                )

                ingredients.append(
                    {"name": ingredient["ingredient"]["name"], "quantity": quantity}
                )
        except KeyError as e:
            print(f"Missing key in ingredient data: {e}")
        except Exception as e:
            print(f"An error occurred while processing ingredients: {e}")
        return ingredients

    def get_instructions(self):
        """
        Process the json in the crouton file to sort and get the instructions
        """
        instructions = []
        try:
            for instruction in self.croutonFile.get("steps", []):
                instructions.append(instruction.get("step", ""))
        except KeyError as e:
            print(f"Missing key in ingredient data: {e}")
        except Exception as e:
            print(f"An error occurred while processing ingredients: {e}")
        return instructions

    def get_recipeInfo(self):
        """
        Get the info of the recipe:
        name, serves, duration of prep, cooking duration and images
        """
        try:
            name = self.croutonFile.get("name", "unknown")
            serves = self.croutonFile.get("serves", "unknown")
            duration = self.croutonFile.get("duration", "unknown")
            cookingDuration = self.croutonFile.get("cookingDuration", "unknown")
            images = self.croutonFile.get("images", "")
        except KeyError as e:
            print(f"Missing key in ingredient data: {e}")
        except Exception as e:
            print(f"An error occurred while processing ingredients: {e}")
        return {
            "name": name,
            "serves": serves,
            "prepTime": duration,
            "cookingDuration": cookingDuration,
            "images": images,
        }


# Example Usage
if __name__ == "__main__":
    jsonExample = r"""{"serves": 4,"name": "Spaghetti Carbonara","steps": [{"order": 0,"step": "Boil the spaghetti until al dente.","isSection": false,"uuid": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXX"},{"uuid": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXX","isSection": false,"step": "Fry the pancetta in a pan until crispy.","order": 1}],"uuid": "9E8B90D6-1CBD-41B7-9C20-8CF61E7D3B89","folderIDs": [],"isPublicRecipe": false,"defaultScale": 1,"cookingDuration": 40,"images": ["iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="],"tags": [],"ingredients": [{"quantity": {"quantityType": "GRAMS","amount": 200},"ingredient": {"uuid": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXX","name": "Spaghetti"},"uuid": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXX","order": 0},{"ingredient": {"uuid": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXX","name": "Eggs"},"quantity": {"amount": 3 ,"quantityType": "ITEM"},"uuid": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXX","order": 1}],"duration": 15}"""
    handler = CroutonDecodeHandler(json.loads(jsonExample))
    ingredients = handler.get_ingredients()
    instructions = handler.get_instructions()
    recipeInfo = handler.get_recipeInfo()

    print(ingredients)
    print(instructions)
    print(recipeInfo)