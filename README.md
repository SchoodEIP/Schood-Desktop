# Schood-Desktop
The desktop application for the Schood EIP Project

### How to install
> python -m pip install -r requirement.txt

### How to share packages
> python -m pip freeze > requirement.txt

### How to build the project for production
> pyinstaller --onefile --name=Schood --paths=src --add-data="src/images/*:." --icon="src/images/m_logo_schood.ico" src/main.py