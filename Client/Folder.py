class Folder:
    def __init__(self, folder_name, parent):
        self.parent = parent
        self.folder_name = folder_name
        self.contents = {
            'Files' : [],
            'Sub-Folders' : []
        }
        self.added = False
    
    def swap_parent(self, new_parent):
        self.parent = new_parent

    def add_file(self, file):
        self.contents['Files'].append(file)

    def add_folder(self, folder):
        self.contents['Sub-Folders'].append(folder)

    def get_files(self):
        return self.contents['Files']
    
    def get_sub_folders(self):
        return self.contents['Sub-Folders']

    def get_contents(self):
        return contents

    def __str__(self):
        return self.folder_name