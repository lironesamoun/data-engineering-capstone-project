# setup.py
from pathlib import Path

from setuptools import find_namespace_packages, setup

# Load packages from requirements.txt
BASE_DIR = Path(__file__).parent
with open(Path(BASE_DIR, "requirements.txt")) as file:
    required_packages = [ln.strip() for ln in file.readlines()]

docs_packages = ["mkdocs==1.4.2", "mkdocstrings==0.19.0", "mkdocstrings_python==0.8.3"]
style_packages = ["black==22.12.0", "flake8==6.0.0", "autoflake==2.0.0", "isort==5.11.4", "pylint==2.15.10"]
test_packages = ["pytest==7.2.0", "pytest_cov==4.0.0", "great_expectations==0.15.42"]


# setup.py
setup(
    name="global-terrorism-data-engineering-project",
    version="0.1",
    description="Data Engineering Zoomcamp - Capstone Project",
    author="Lirone Samoun",
    python_requires=">=3.10",
    packages=find_namespace_packages(),
    install_requires=[required_packages],
    extras_require={
        "dev": docs_packages + style_packages + test_packages + ["pre-commit==2.21.0"],
        "docs": docs_packages,
        "test": test_packages,
    },
)