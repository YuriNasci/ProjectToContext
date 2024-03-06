configurations = {
    'git_dir': '.git',
    'output_file': '.ctxt',
    'gitignore_filename': '.gitignore',
}

def get(key):
    """Retrieve a value from the configuration dictionary."""
    return configurations.get(key)
