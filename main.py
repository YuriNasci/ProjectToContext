import os
import sys
import fnmatch

GIT_DIR = '.git'
OUTPUT_FILE = '.ctxt'

"""
Checks if the given file path is a text file.

Returns True if the file is a text file, False otherwise.
"""
def is_text_file(filepath: str) -> bool:
    """
    Verifica se o arquivo é um arquivo de texto.
    Retorna True para arquivos textuais, False para outros tipos.
    """
    try:
        with open(filepath, 'tr') as check_file:
            check_file.read(1024)
        return True
    except UnicodeDecodeError:
        return False

"""
Reads the .gitignore file and returns a list of patterns to ignore.

Parameters:
- directory (str): The path to the directory containing the .gitignore file.

Returns:
- list: A list of ignore patterns from the .gitignore file.
"""
def read_gitignore_rules(directory):
    """
    Lê o arquivo .gitignore e retorna uma lista de padrões a serem ignorados.
    """
    gitignore_path = os.path.join(directory, '.gitignore')
    if not os.path.exists(gitignore_path):
        return []
    
    with open(gitignore_path, 'r') as file:
        rules = [line.strip() for line in file if line.strip() and not line.startswith('#')]
    
    return rules

"""Determines if the given path should be ignored based on the provided .gitignore rules.

Args:
  path (str): The file path to check.
  ignore_rules (List[str]): The parsed .gitignore rules.

Returns:
  bool: True if the path matches any of the ignore rules, False otherwise.
"""
def should_ignore(path, ignore_rules):
    """
    Determina se o caminho deve ser ignorado com base nas regras do .gitignore.
    """
    for rule in ignore_rules:
        if fnmatch.fnmatch(path, rule) or fnmatch.fnmatch(os.path.basename(path), rule):
            return True
    return False

"""
Generates a tree representation of the given directory, ignoring files and directories according to .gitignore rules.

Parameters:
- dir_path (str): The path to the directory to generate the tree for.
- prefix (str): The prefix to use for each line (for indentation).
- ignore_rules (List[str]): The list of ignore rules from the .gitignore file.

Yields:
- str: Each line of the directory tree representation.
"""
def generate_directory_tree(dir_path, prefix='', ignore_rules=[]):
    """
    Gera uma representação de árvore do diretório especificado, ignorando arquivos e diretórios conforme .gitignore.
    """
    items = os.listdir(dir_path)
    items.sort()
    for index, item in enumerate(items):
        if item == GIT_DIR:
            continue

        path = os.path.join(dir_path, item)
        if should_ignore(path, ignore_rules):
            continue
        if os.path.isdir(path):
            yield prefix + '├── ' + item
            extension = '│   ' if index < len(items) - 1 else '    '
            yield from generate_directory_tree(path, prefix=prefix + extension, ignore_rules=ignore_rules)
        else:
            yield prefix + '├── ' + item

"""
Recursively processes the given directory, writing details to the output file, 
ignoring files and directories according to .gitignore rules.

Parameters:
- directory (str): The path to the directory to process.
- output_file (file object): The file to write output to.
- ignore_rules (List[str]): The .gitignore rules to determine which files/dirs to ignore.
"""
def process_directory(directory, output_file, ignore_rules):
    """
    Processa recursivamente o diretório fornecido, escrevendo detalhes no arquivo de saída, ignorando conforme .gitignore.
    """
    for root, dirs, files in os.walk(directory, topdown=True):
        # Pular pasta .git
        if ".git" in dirs:  
            dirs.remove(GIT_DIR)
        
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), ignore_rules)]
        files.sort()
        for name in files:
            file_path = os.path.join(root, name)
            if should_ignore(file_path, ignore_rules):
                continue
            if is_text_file(file_path):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    output_file.write(f"\nFile: {name}\n")
                    output_file.write("\n" + file.read())
            else:
                output_file.write(f"\nCaminho do Arquivo: {file_path}\n")
                output_file.write("Formato de arquivo não é válido para conversão.\n")

"""
main() is the entry point for the program. It parses command line arguments, reads .gitignore rules, generates a directory tree while ignoring files based on .gitignore, recursively processes text files in the directory to extract contents, and writes the output to a file.
"""
def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <diretório de origem>")
        sys.exit(1)

    source_directory = sys.argv[1]
    ignore_rules = read_gitignore_rules(source_directory)
    output_filename = OUTPUT_FILE

    # Verificar se arquivo de saída já existe e apagá-lo
    if os.path.exists(os.path.join(source_directory, output_filename)):
        os.remove(os.path.join(source_directory, output_filename))

    with open(os.path.join(source_directory, output_filename), 'w', encoding='utf-8') as output_file:
        tree = generate_directory_tree(source_directory, ignore_rules=ignore_rules)
        output_file.write(".\n")
        for line in tree:
            output_file.write(line + "\n")

        process_directory(source_directory, output_file, ignore_rules)

    print(f"Conversão concluída. Arquivo gerado: {output_filename}")

if __name__ == "__main__":
    main()
