import os
from handlers.file_handler import FileHandler
from handlers.git_ignore_handler import GitIgnoreHandler

GIT_DIR = '.git'
OUTPUT_FILE = '.ctxt'
GITIGNORE_FILENAME = '.gitignore'

class DirectoryHandler:
    def generate_directory_tree(self, dir_path, prefix='', ignore_rules=[]):
        items = os.listdir(dir_path)
        items.sort()
        for index, item in enumerate(items):
            if item == GIT_DIR or item == GITIGNORE_FILENAME:
                continue

            path = os.path.join(dir_path, item)
            if GitIgnoreHandler().should_ignore(path, ignore_rules):
                continue
            if os.path.isdir(path):
                yield prefix + '├── ' + item
                extension = '│   ' if index < len(items) - 1 else '    '
                yield from self.generate_directory_tree(path, prefix=prefix + extension, ignore_rules=ignore_rules)
            else:
                yield prefix + '├── ' + item

    def process_directory(self, directory, output_file, ignore_rules):
        for root, dirs, files in os.walk(directory, topdown=True):
            if ".git" in dirs:  
                dirs.remove(GIT_DIR)
            
            dirs[:] = [d for d in dirs if not GitIgnoreHandler().should_ignore(os.path.join(root, d), ignore_rules)]
            files.sort()
            for name in files:
                if name == GITIGNORE_FILENAME:
                    continue
                
                file_path = os.path.join(root, name)
                if GitIgnoreHandler().should_ignore(file_path, ignore_rules):
                    continue
                if FileHandler().is_text_file(file_path):
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        output_file.write(f"\nFile: {name}\n")
                        output_file.write("\n" + file.read())
                else:
                    output_file.write(f"\nCaminho do Arquivo: {file_path}\n")
                    output_file.write("Formato de arquivo não é válido para conversão.\n")