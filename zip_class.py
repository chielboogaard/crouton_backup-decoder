import zipfile
import os
import shutil

# Class to handle ZIP files
class ZipHandler:
    # zip_file_path: Path to the ZIP file
    # extract_to_path: Path to extract the ZIP file contents
    def __init__(self, zip_file_path, extract_to_path="./tmp/"):
        # Initialize the ZipHandler with the ZIP file path and target extraction folder.
        self.zip_file_path = zip_file_path
        self.extract_to_path = extract_to_path

    # Extract the ZIP file contents to a variable.
    # in memory version of extract_files
    def extract_croutonFiles(self):
        all_contents = []
        # Opens zip in read mode
        with zipfile.ZipFile(self.zip_file_path, 'r') as zip_ref:
            # Iterates through all files in the zip
            for croutonFile in zip_ref.namelist():
                # Opens the file in the zip
                with zip_ref.open(croutonFile) as crouton:
                    # Reads the file and appends it to the list
                    all_contents.append(crouton.read().decode('utf-8')) # Decode bytes to string
        # Returns the list of all files in the zip
        return all_contents

    # Extract the ZIP file contents to the target folder.
    # Creates the folder if it doesn't exist.
    def extract_files(self):
        # Creates the target extraction folder if it doesn't exist.
        os.makedirs(self.extract_to_path, exist_ok=True)
        with zipfile.ZipFile(self.zip_file_path, 'r') as zip_ref:
            # Extracts all contents of the ZIP file to the target folder.
            zip_ref.extractall(self.extract_to_path)
        print(f"Files extracted to {self.extract_to_path}")

    # Iterate through all files in the extracted directory.
    def iterate_files(self):
        # Walk through the directory tree and yield each file path.
        for root, dirs, files in os.walk(self.extract_to_path):
            for file in files:
                # For each file found, it constructs the full file path and 
                # yields it, allowing you to process each file individually.
                file_path = os.path.join(root, file)
                yield file_path

    # Delete the extraction folder and all its contents.
    def clean_up(self):
        # Check if the extraction folder
        if os.path.exists(self.extract_to_path):
            # If it exists, remove the folder and all its contents
            shutil.rmtree(self.extract_to_path)
            print(f"Temporary folder {self.extract_to_path} deleted.")


# Example Usage
if __name__ == "__main__":
    zip_file = "add your zip path"
    handler = ZipHandler(zip_file)

    inMemory = handler.extract_croutonFiles()

    # Extract files on disk
    handler.extract_files()

    # Process files
    print("Processing files:")
    for file_path in handler.iterate_files():
        print(f"Found file: {file_path}")

    # Clean up the extracted files
    handler.clean_up()