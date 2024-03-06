import fnmatch
import os

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