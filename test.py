import os
import requests
import zipfile
import tempfile
from typing import List

def download_and_extract_zip(url: str) -> List[str]:
    file_paths = []

    # Download the zip file
    response = requests.get(url)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as zip_file:
            zip_file.write(response.content)
            zip_file_path = zip_file.name

        # Create a temporary folder for extracting the files
        with tempfile.TemporaryDirectory() as tmpdir:
            # Extract the zip file
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)
            print(tmpdir)
            # Iterate through the extracted files and append their paths to the list
            for root, _, files in os.walk(tmpdir):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_paths.append(file_path)

    else:
        print(f"Request failed with status code {response.status_code}.")

    return file_paths

# Example usage
url = "http://glycam.org/json/download/conformer/be417aff-82c8-4870-b635-f336dd67a0c2/structure/"
file_paths = download_and_extract_zip(url)
# for path in file_paths:
    # print(path)
