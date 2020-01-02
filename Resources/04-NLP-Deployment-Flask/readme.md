# Create and activate pythonvirtual environment

```
python3 -m virtualenv venv
source venv/bin/activate
```
To deactivate
```
deactivate
```

# Add `.gitignore` for clean version control

- Goto `gitignore.io` website and search for the stacks, programming lnguages, IDEs you will use. Here, `xcode`, `python`, `flask`
- Click on `create`
- copy the text in `gitignore.io` file and save it in main directory (or child directory). You can even restrict folders from being comitted / pushed to github by adding the path to the folder or file at the end of the file. *Note: The path must be mentioned relative to the location of `.gitignore` file. For example, i don't want to include `venv` virtual environment folder in my commits. As it is in the same directory as `.gitignore` file, at the eof, i will mention `venv` in new line.*

# Deployment with docker
