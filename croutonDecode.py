import os
import json


class ingredientHandler:
    def __init__(self, name: str, quantity: int):
        self.name = name
        self.quantity = quantity


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
        suffix_map = {
            "ITEM": "x",
            "GRAMS": "gr",
            "MILLS": "ml",
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
                    ingredientHandler(
                        name=ingredient["ingredient"]["name"], quantity=quantity
                    )
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
    jsonExample = r"""{"serves":4,"name":"Hartige Broccoli Taart","steps":[{"order":0,"step":"Zet de oven aan op 200 C","isSection":false,"uuid":"1AFE502F-DBDF-40F6-89B8-7359AD9609F1"},{"uuid":"8D042CD0-D331-47E8-893D-2AA932B9E4C2","isSection":false,"step":"Snij de ui en broccoli","order":1},{"step":"Kook de broccoli voor ong 5 mins","isSection":false,"order":2,"uuid":"9705CB9A-9196-4041-8C2C-8E1988C7E882"},{"isSection":false,"order":3,"uuid":"86D68030-D67F-4EA5-BADB-1840B4015A58","step":"Bak de spekjes en voeg de gesneden ui toe"},{"uuid":"AC8264B0-B9A6-4B4C-9065-13E69351121D","order":4,"step":"Vet het bakblik in en doe het bladerdeeg er in\n(Eventueel met een klein beetje parneermeel)","isSection":false},{"order":5,"uuid":"678B33AC-2233-4AC4-81AF-8B1EDFA0257A","step":"Doe de gekookte broccoli erin","isSection":false},{"isSection":false,"order":6,"step":"Verdeel de mix van ui en spekjes er overheen","uuid":"3691841E-C47A-4ED7-9B74-C004B64DB78C"},{"uuid":"9747BA5B-7375-4C51-8A5A-C39365510DDF","isSection":false,"step":"Voeg de eieren en kaas bij elkaar en mix even","order":7},{"step":"Giet deze mix over de taart heen","isSection":false,"order":8,"uuid":"6666C36E-A742-4598-B865-8C8BCC6DB048"},{"step":"Bak voor 35 a 40 mins","uuid":"F218F730-833C-4517-A7F7-A72CB48E491D","isSection":false,"order":9}],"uuid":"9E8B90D6-1CBD-41B7-9C20-8CF61E7D3B89","folderIDs":[],"isPublicRecipe":false,"defaultScale":1,"cookingDuration":40,"images":["iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="],"tags":[],"ingredients":[{"quantity":{"quantityType":"ITEM","amount":5},"ingredient":{"uuid":"677A9937-BF0C-422F-B937-DEE2E00CF4AF","name":"Bladerdeeg plakjes"},"uuid":"592CC07A-74DA-4253-9350-1457FB550605","order":0},{"ingredient":{"uuid":"66F2F928-2246-4958-AEE9-5246BB6F5269","name":"broccoliroosjes"},"order":1,"quantity":{"amount":300,"quantityType":"GRAMS"},"uuid":"4371A35B-81D2-40DE-86F8-E8DE10DCC444"},{"quantity":{"amount":1,"quantityType":"ITEM"},"order":2,"uuid":"B8624BD7-985E-452F-A5AA-185A40F250FA","ingredient":{"name":"Ui","uuid":"71D1FE41-A5B6-4E24-9275-2B53F15442E0"}},{"quantity":{"quantityType":"ITEM","amount":3},"ingredient":{"uuid":"13437BE0-CB00-4EAA-832B-F315BF1D4F24","name":"eieren"},"uuid":"ECEB7505-E21D-4637-B585-8276BB90A0F8","order":3},{"order":4,"ingredient":{"name":"creme fraiche","uuid":"BBBE293F-98DC-4C79-B30E-44634523CE7E"},"quantity":{"amount":100,"quantityType":"MILLS"},"uuid":"E1847304-A236-43A9-8716-A50E35D85F04"},{"order":5,"uuid":"312B84BA-503C-47E8-89E7-42F7A14AC9BD","quantity":{"quantityType":"GRAMS","amount":150},"ingredient":{"name":"spekreepjes","uuid":"467A794B-C87D-4B36-8CB8-EC0FC985FE9E"}},{"ingredient":{"name":"snufje zout en peper","uuid":"2F842E36-1B95-4591-A514-A1C446501815"},"uuid":"79C60D4E-88EE-466E-8E8D-704F2B01AA50","order":6},{"order":7,"ingredient":{"name":"Zakje geraspte kaas","uuid":"B3D321CF-8648-4C99-A2E5-176149583385"},"uuid":"3DB2D319-A63C-4AC9-93F6-8485FDB9D012","quantity":{"amount":1,"quantityType":"ITEM"}}],"duration":15}"""
    handler = CroutonDecodeHandler(json.loads(jsonExample))
    ingredients = handler.get_ingredients()
    instructions = handler.get_instructions()
    recipeInfo = handler.get_recipeInfo()
