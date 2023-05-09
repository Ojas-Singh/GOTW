import os
import zipfile
import tempfile
import requests
import json
from typing import Any
from typing import List
import shutil
from pathlib import Path
import streamlit as st
import main

def process(url: str):
    output_folder = "output"
    output_path = Path(output_folder)

    if output_path.exists():
        shutil.rmtree(output_folder)

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

                json_file = os.path.join(tmpdir, "info.json")
                
                off = os.path.join(tmpdir, "structure.off")
                pdb = os.path.join(tmpdir, "structure.pdb")
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    
                name = data.get("indexOrderedSequence", None)
                st.write(name)
                st.info("running Tleap...")
                output_folder_path = main.process_app(name,pdb,off,200)

    else:
        print(f"Request failed with status code {response.status_code}.")

    return output_folder_path

def zip_directory(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))



st.set_page_config(layout="wide")

st.title("Glycan Of The Week Script")

url = st.text_input(
        "Enter URL ...",placeholder ="http://glycam.org/json/download/conformer/be417aff-82c8-4870-b635-f336dd67a0c2/structure/"
    )


if not url=="":
    st.write("fetching files from glycam...")
    output_folder_path = process(url)
    

    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "output.zip")
        zip_directory(output_folder_path, zip_path)

        with open(zip_path, "rb") as f:
            st.download_button("Download output.zip", f.read(), "output.zip", "application/zip")

st.write("")
