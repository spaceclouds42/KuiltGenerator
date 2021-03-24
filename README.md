# FabriKGenerator
A simple python app for generating fabric mods in Kotlin.

## Usage
Simple run `main.py` from your mod development directory so that the generated mod is placed with your other mods. To be able to run FabriKGenerator from anywhere, you can do the following:
```bash
# Open .bashrc in preferred text editor
nano ~/.bashrc

# Add this line to it and save
alias fabrikgen="python $HOME/path_to_dir_containing_app/FabriKGenerator/main.py"
```
Once you have done this, you can run `fabrikgen` anywhere to start generating a mod in your current directory.