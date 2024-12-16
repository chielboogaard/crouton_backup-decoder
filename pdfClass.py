import base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from io import BytesIO

class RecipePDF:
    def __init__(self, json_data, output_file="recipe.pdf"):
        """
        Initialize the ZipHandler with the ZIP file path and target extraction folder.
        """
        self.json_data = json_data
        self.output_file = output_file

    def decode_image(self, base64_string):
        """
        Decodes a base64 string into an ImageReader object for use with ReportLab.
        """
        image_data = base64.b64decode(base64_string)
        image = ImageReader(BytesIO(image_data))
        return image

    def generate_pdf(self):
        """
        Generates the pdf with use of reportlab
        """
        c = canvas.Canvas(self.output_file, pagesize=letter)
        width, height = letter

        # Margins
        x_margin = 50
        y_margin = 50
        line_height = 14

        # Add base64 image (if available) to the top-right
        base64_image = self.json_data.get("image", None)
        if base64_image:
            image = self.decode_image(base64_image)
            img_width = 100  # Adjust as needed
            img_height = 100  # Adjust as needed
            c.drawImage(image, width - x_margin - img_width, height - y_margin - img_height, 
                        width=img_width, height=img_height)

        # Title
        y_position = height - y_margin
        c.setFont("Helvetica-Bold", 18)
        c.drawString(x_margin, y_position, self.json_data.get("title", "Untitled Recipe"))
        y_position -= line_height * 2

        # Author
        c.setFont("Helvetica", 12)
        author = self.json_data.get("author", "Unknown Author")
        c.drawString(x_margin, y_position, f"By: {author}")
        y_position -= line_height * 2

        # Ingredients Header
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.darkblue)
        c.drawString(x_margin, y_position, "Ingredients:")
        y_position -= line_height * 1.5
        c.setFillColor(colors.black)

        # Ingredients List
        c.setFont("Helvetica", 12)
        for ingredient in self.json_data.get("ingredients", []):
            ingredient_text = f"- {ingredient['quantity']} {ingredient['name']}"
            c.drawString(x_margin, y_position, ingredient_text)
            y_position -= line_height

        y_position -= line_height  # Spacing before instructions

        # Instructions Header
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.darkblue)
        c.drawString(x_margin, y_position, "Instructions:")
        y_position -= line_height * 1.5
        c.setFillColor(colors.black)

        # Instructions List
        c.setFont("Helvetica", 12)
        for i, step in enumerate(self.json_data.get("instructions", []), 1):
            instruction_text = f"{i}. {step}"
            c.drawString(x_margin, y_position, instruction_text)
            y_position -= line_height

            # Handle page overflow
            if y_position < y_margin:
                c.showPage()
                y_position = height - y_margin
                c.setFont("Helvetica", 12)

        # Save the PDF
        c.save()
        print(f"PDF saved as {self.output_file}")

# Example Usage
if __name__ == "__main__":
    # Base64 image example (replace with your actual image in base64 format)
    base64_image_example = """
    iVBORw0KGgoAAAANSUhEUgAAAAUA
    AAAFCAYAAACNbyblAAAAHElEQVQI12P4
    //8/w38GIAXDIBKE0DHxgljNBAAO
    9TXL0Y4OHwAAAABJRU5ErkJggg==
    """

    recipe_data = {
        "title": "Spaghetti Carbonara",
        "author": "John Doe",
        "image": base64_image_example.strip(),
        "ingredients": [
            {"name": "Spaghetti", "quantity": "200g"},
            {"name": "Eggs", "quantity": "3"},
        ],
        "instructions": [
            "Boil the spaghetti until al dente.",
            "Fry the pancetta in a pan until crispy.",
        ]
    }
    recipe_pdf = RecipePDF(recipe_data, "spaghetti_carbonara_with_image.pdf")
    recipe_pdf.generate_pdf()
