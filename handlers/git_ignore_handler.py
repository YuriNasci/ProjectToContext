import fnmatch
import os
import utils.config_loader as configurations

class GitIgnoreHandler:
    """Reads the rules from the .gitignore file in the given directory.
    
    Args:
        directory: The path to the directory containing the .gitignore file.
    
    Returns:
        A list of ignore rules parsed from the .gitignore file.
    """
    def read_gitignore_rules(self, directory):
        gitignore_path = os.path.join(directory, configurations.get('gitignore_filename'))
        if not os.path.exists(gitignore_path):
            return []

        rules = []
        with open(gitignore_path, 'r') as file:
            for line in file:
                stripped_line = line.strip()
                if stripped_line and not stripped_line.startswith('#'):
                    rules.append(stripped_line)

        return rules
    
    """Checks if a path should be ignored based on the provided ignore rules.
    
    Args:
        path: The path to check.
        ignore_rules: The list of ignore rules.
    
    Returns:
        True if the path matches any of the ignore rules, False otherwise.
    """
    def should_ignore(self, path, ignore_rules):
        return any(fnmatch.fnmatch(path, rule) or fnmatch.fnmatch(os.path.basename(path), rule) for rule in ignore_rules)