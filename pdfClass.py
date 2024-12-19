import base64
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from io import BytesIO


class RecipePDFHandler:
    def __init__(self, json_data, output_path, output_file="recipe.pdf",):
        """
        Initialize the ZipHandler with the ZIP file path and target extraction folder.
        """
        self.json_data = json_data
        self.output_file = output_file
        self.output_path = output_path

    def decode_image(self, base64_string):
        """
        Decodes a base64 string into an ImageReader object for use with ReportLab.
        """
        image_data = base64.b64decode(base64_string)
        image = ImageReader(BytesIO(image_data))
        return image

    def draw_wrapped_text(self, c, text, x, y, font_size, max_width, max_y):
        """
        Draws wrapped text at (x, y) with a specified font size, checking for overflow.
        If there is not enough space, it creates a new page and resets the y position.
        """
        c.setFont("Helvetica", font_size)
        text_height = 14  # Assuming a line height of 14 for this example

        # Split the text into words for wrapping
        words = text.split(" ")
        current_line = ""
        for word in words:
            # Check if adding this word exceeds the width
            test_line = f"{current_line} {word}".strip()
            text_width = c.stringWidth(test_line, "Helvetica", font_size)

            if (
                text_width > max_width
            ):  # If it exceeds the max width, draw the current line
                # If the y position is too low, create a new page
                if y < max_y:
                    c.showPage()
                    y = A4[1] - 50  # Reset to top of the new page
                    c.setFont("Helvetica", font_size)  # Reset the font for the new page

                c.drawString(x, y, current_line.strip())  # Draw the current line
                y -= text_height  # Move y position down for the next line
                current_line = word  # Start a new line with the current word
            else:
                current_line = test_line  # Add the word to the current line

        # Draw any remaining text in the current line
        if current_line:
            if y < max_y:
                c.showPage()
                y = A4[1] - 50  # Reset to top of the new page
                c.setFont("Helvetica", font_size)

            c.drawString(x, y, current_line.strip())  # Draw the last line

        return y - text_height  # Return the new y position

    def generate_pdf(self):
        """
        Generates the pdf with use of reportlab
        """
        c = canvas.Canvas(f"{self.output_path}/{self.output_file}", pagesize=A4,)
        width, height = A4

        # Margins
        x_margin = 50
        y_margin = 50
        line_height = 14
        max_width = width - 2 * x_margin  # Maximum width for text

        # Add base64 image (if available) to the top-right
        base64_image = self.json_data.get("image", None)
        if base64_image:
            image = self.decode_image(base64_image)
            img_width = 150  # Adjust as needed
            img_height = 150  # Adjust as needed
            c.drawImage(
                image,
                width - x_margin - img_width,
                height - y_margin - img_height,
                width=img_width,
                height=img_height,
            )

        # Title
        y_position = height - y_margin
        c.setFont("Helvetica-Bold", 18)
        y_position = self.draw_wrapped_text(c, self.json_data.get("title", "Untitled Recipe"), x_margin, y_position, 18, max_width, y_margin)
        y_position -= line_height * 1.3

        # serves
        c.setFont("Helvetica", 12)
        serves = self.json_data.get("serves", "Unknown serves")
        c.drawString(x_margin, y_position, f"Recipe serves : {serves}")
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
            y_position = self.draw_wrapped_text(c, ingredient_text, x_margin, y_position, 12, max_width, y_margin)

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
            y_position = self.draw_wrapped_text(
                c, instruction_text, x_margin, y_position, 12, max_width, y_margin
            )

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
        "serves": "4",
        "image": base64_image_example.strip(),
        "ingredients": [
            {"name": "Spaghetti", "quantity": "200g"},
            {"name": "Eggs", "quantity": "3"},
        ],
        "instructions": [
            "Boil the spaghetti until al dente.",
            "Fry the pancetta in a pan until crispy.",
        ],
    }
    recipe_pdf = RecipePDFHandler(recipe_data, "spaghetti_carbonara_with_image.pdf")
    recipe_pdf.generate_pdf()
