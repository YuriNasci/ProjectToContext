import os
from handlers.file_handler import FileHandler
from handlers.git_ignore_handler import GitIgnoreHandler
from utils.config_loader import configurations

class DirectoryHandler:
    def generate_directory_tree(self, dir_path, prefix='', ignore_rules=[]):
        items = os.listdir(dir_path)
        items.sort()
        for index, item in enumerate(items):
            if item == configurations.get('git_dir') or item == configurations.get('gitignore_filename'):
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
                dirs.remove(configurations.get('git_dir'))
            
            dirs[:] = [d for d in dirs if not GitIgnoreHandler().should_ignore(os.path.join(root, d), ignore_rules)]
            files.sort()
            for name in files:
                if name == configurations.get('gitignore_filename'):
                    continue
                
                file_path = os.path.join(root, name)
                if GitIgnoreHandler().should_ignore(file_path, ignore_rules):
                    continue
                
                output_file.write(f"\nFile: {name}\n")
                if FileHandler().is_text_file(file_path):
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        
                        output_file.write("\n" + file.read())
                else:
                    output_file.write("...\n")