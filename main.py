import os
import sys
import fnmatch

from networkx import configuration_model
from handlers.directory_handler import DirectoryHandler

from handlers.git_ignore_handler import GitIgnoreHandler
from utils.config_loader import configurations
def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <diretório de origem>")
        sys.exit(1)

    source_directory = sys.argv[1]
    ignore_rules = GitIgnoreHandler().read_gitignore_rules(source_directory)
    output_filename = configurations.get('output_file')

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
