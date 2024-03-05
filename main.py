import os
import sys
import fnmatch

GIT_DIR = '.git'
OUTPUT_FILE = '.ctxt'

class FileHandler:
    def is_text_file(self, filepath: str) -> bool:
        try:
            with open(filepath, 'tr') as check_file:
                check_file.read(1024)
            return True
        except UnicodeDecodeError:
            return False

class GitIgnoreHandler:
    def read_gitignore_rules(self, directory):
        gitignore_path = os.path.join(directory, '.gitignore')
        if not os.path.exists(gitignore_path):
            return []
        
        with open(gitignore_path, 'r') as file:
            rules = [line.strip() for line in file if line.strip() and not line.startswith('#')]
        
        return rules

    def should_ignore(self, path, ignore_rules):
        for rule in ignore_rules:
            if fnmatch.fnmatch(path, rule) or fnmatch.fnmatch(os.path.basename(path), rule):
                return True
        return False

class DirectoryHandler:
    def generate_directory_tree(self, dir_path, prefix='', ignore_rules=[]):
        items = os.listdir(dir_path)
        items.sort()
        for index, item in enumerate(items):
            if item == GIT_DIR:
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

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <diretório de origem>")
        sys.exit(1)

    source_directory = sys.argv[1]
    ignore_rules = GitIgnoreHandler().read_gitignore_rules(source_directory)
    output_filename = OUTPUT_FILE

    if os.path.exists(os.path.join(source_directory, output_filename)):
        os.remove(os.path.join(source_directory, output_filename))

    with open(os.path.join(source_directory, output_filename), 'w', encoding='utf-8') as output_file:
        tree = DirectoryHandler().generate_directory_tree(source_directory, ignore_rules=ignore_rules)
        output_file.write(".\n")
        for line in tree:
            output_file.write(line + "\n")

        DirectoryHandler().process_directory(source_directory, output_file, ignore_rules)

    print(f"Conversão concluída. Arquivo gerado: {output_filename}")

if __name__ == "__main__":
    main()
