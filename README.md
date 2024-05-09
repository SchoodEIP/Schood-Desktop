# Schood-Desktop
The desktop application for the Schood EIP Project

### How to install
> python -m pip install -r requirement.txt

### How to share packages
> python -m pip freeze > requirement.txt

### How to build the project for production
> pyinstaller --onefile --paths=src --add-data "src/images/logo_schood.png:." src/main.py