import zipfile
import os
import shutil

class ZipHandler:
    def __init__(self, zip_file_path, extract_to_path="./tmp/"):
        """
        Initialize the ZipHandler with the ZIP file path and target extraction folder.
        """
        self.zip_file_path = zip_file_path
        self.extract_to_path = extract_to_path

    def extract_files(self):
        """
        Extract the ZIP file contents to the target folder.
        Creates the folder if it doesn't exist.
        """
        os.makedirs(self.extract_to_path, exist_ok=True)
        with zipfile.ZipFile(self.zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(self.extract_to_path)
        print(f"Files extracted to {self.extract_to_path}")

    def iterate_files(self):
        """
        Iterate through all files in the extracted directory.
        Yields each file path.
        """
        for root, dirs, files in os.walk(self.extract_to_path):
            for file in files:
                file_path = os.path.join(root, file)
                yield file_path

    def clean_up(self):
        """
        Delete the extraction folder and all its contents.
        """
        if os.path.exists(self.extract_to_path):
            shutil.rmtree(self.extract_to_path)
            print(f"Temporary folder {self.extract_to_path} deleted.")


# Example Usage
if __name__ == "__main__":
    zip_file = "Crouton Recipes - 28 Nov 2024.zip"  # Replace with your ZIP file path
    handler = ZipHandler(zip_file)

    # Extract files
    handler.extract_files()

    # Process files
    print("Processing files:")
    for file_path in handler.iterate_files():
        print(f"Found file: {file_path}")

    # Clean up the extracted files
    handler.clean_up()