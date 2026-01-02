import os
from pathlib import Path
import logging

logging.basicConfig(level = logging.INFO, format = '[%(asctime)s]: %(message)s:')

project_name = "multi_doc_chat"
list_of_files = [
    "github/workflows/.gitkeep",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/logger/custom_logger.py",
    f"{project_name}/exceptions/__init__.py",
    f"{project_name}/exceptions/custom_exception.py",
    f"{project_name}/config/config.yaml",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/common.py",
    f"{project_name}/src",
    f"{project_name}/prompts/__init__.py",
    f"{project_name}/model/__init__.py",
    "main.py",
    "requirements.txt",
    "templates/index.html",
    "static/css/styles.css",
    "notebooks",
    "data",
    "Dockerfile",
    "setup.py",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
        logging.info(f"Creating file: {filepath}")
    
    else:
        logging.info(f"{filename} already exists")