class FileHandler:
    def is_text_file(self, filepath: str) -> bool:
        try:
            with open(filepath, 'tr') as check_file:
                check_file.read(1024)
            return True
        except UnicodeDecodeError:
            return False