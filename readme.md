# ProjectToContext
ProjectToContext is a Python application that generates a directory tree text file for a given source directory. It includes empty folders and excludes files/folders that match .gitignore rules.
## Directory Structure:
```
ProjectToContext
├── handlers
│   ├── __init__.py
│   ├── directory_handler.py
│   ├── file_handler.py
│   ├── git_ignore_handler.py
├── main.py
├── utils
    ├── __init__.py
    ├── config_loader.py
```
## Usage
```shell
python main.py <source directory>
```
## Files
### main.py
This is the main entry point of the application. It parses command line arguments, processes the given directory to generate a directory tree text file, and handles .gitignore rules.
### handlers/directory_handler.py
This file contains the DirectoryHandler class which is responsible for generating a directory tree structure with prefixes to show the tree hierarchy and processing all files and directories under the given directory.
### handlers/file_handler.py
This file contains the FileHandler class which is responsible for checking if a file is a text file.
### handlers/git_ignore_handler.py
This file contains the GitIgnoreHandler class which is responsible for reading the rules from the .gitignore file in the given directory and checking if a path should be ignored based on the provided ignore rules.
utils/config_loader.pyThis file contains the configurations for the application.
## Configurations
The application uses the following configurations:
- git_dir: .git
- output_file: .ctxt
- gitignore_filename: .gitignore

These can be retrieved using the get(key) function in config_loader.py.