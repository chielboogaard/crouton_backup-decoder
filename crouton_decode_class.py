import os
import json

# The code defines a class CroutonDecodeHandler that processes a JSON object 
# representing a recipe, typically from a file format called "crouton." This 
# class extracts relevant information, such as the recipe ingredients, instructions, 
# and additional details like the recipe name, servings, and cooking time.
class CroutonDecodeHandler:
    # Initialize the ZipHandler with the ZIP file path and target extraction folder.
    def __init__(self, croutonFile):
        self.croutonFile = croutonFile

    def convert_quantity(self, quantityAmount: int, quantityType: str):
        # Convert the quantity name in the crouton format to a logical unit name
        # Also add the amount
        if quantityType == "SECTION":
            return "--section--"
        
        # Get the suffix for the quantity type
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
        # Return the amount and their type
        return f"{quantityAmount}{suffix}"

    # Process the json in the crouton file and format it to:
    # [{"name": "Example ingredient", "quantity": "999"}]
    def get_ingredients(self):
        ingredients = []
        try:
            for ingredient in self.croutonFile.get("ingredients", []):
                # get the quantity type name
                quantity_data = ingredient.get("quantity", {})
                # get the amount and quantity type
                amount = quantity_data.get("amount", 1)
                quantityType = quantity_data.get("quantityType", "ITEM")

                # Convert the quantity to a logical unit
                quantity = self.convert_quantity(
                    quantityAmount=amount,
                    quantityType=quantityType,
                )

                # Append the ingredient to the list
                ingredients.append(
                    {"name": ingredient["ingredient"]["name"], "quantity": quantity}
                )
        # Catch the errors        
        except KeyError as e:
            print(f"Missing key in ingredient data: {e}")
        except Exception as e:
            print(f"An error occurred while processing ingredients: {e}")
        
        # Return the list of ingredients
        return ingredients

    # Process the json in the crouton file to sort and get the instructions
    def get_instructions(self):
        instructions = []
        # Get the instructions from the crouton file
        try:
            for instruction in self.croutonFile.get("steps", []):
                # Append the instruction to the list
                instructions.append(instruction.get("step", ""))
        # Catch the errors
        except KeyError as e:
            print(f"Missing key in ingredient data: {e}")
        except Exception as e:
            print(f"An error occurred while processing ingredients: {e}")
        # Return the list of instructions
        return instructions

    # Get the info of the recipe:
    # name, serves, duration of prep, cooking duration and images
    def get_recipeInfo(self):
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
        # Return the recipe info
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