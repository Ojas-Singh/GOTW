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
import script
import subprocess


def check_tleap():
    """
    Check if tleap is available in the current environment.
    """
    try:
        tleap_path = shutil.which("tleap")
        if tleap_path:
            st.success(f"tleap is available at {tleap_path}.")
        else:
            st.error("tleap not found. Ensure AmberTools is installed and tleap is in the PATH.")
    except subprocess.CalledProcessError as e:
        st.error(f"tleap check failed: {e.stderr.decode('utf-8')}")
    except FileNotFoundError:
        st.error("tleap not found. Ensure AmberTools is installed and tleap is in the PATH.")

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
                st.code(name)
                st.info("running Tleap...")
                output_folder_path = script.process_app(name,pdb,off,200)

    else:
        print(f"Request failed with status code {response.status_code}.")

    return output_folder_path, name

def zip_directory(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))


check_tleap()
st.set_page_config(layout="wide")

st.title("Glycan Of The Week Script")

url = st.text_input(
        "Enter URL ...",placeholder ="https://glycam.org/json/download/conformer/20c86833-40e2-43c3-bd38-b00c6765f97f/2ht_ogg/"
    )


if not url=="":
    st.write("fetching files from glycam...")
    output_folder_path, name = process(url)
    

    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, f"{name}.zip")
        zip_directory(output_folder_path, zip_path)

        with open(zip_path, "rb") as f:
            st.download_button(f"Download {name}.zip", f.read(), f"{name}.zip", "application/zip")

st.write("")
