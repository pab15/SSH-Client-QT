class File:
    def __init__(self, file_name, parent):
        self.parent = parent
        self.file_name = file_name
        self.file_type = self.file_name.split('.')[1]
        self.content = None
    
    def add_content(self, content):
        self.content = content

    def get_content(self):
        return self.content

    def __str__(self):
        return self.file_name