import File, Folder

class FileSystem:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.current_dir = root_dir
        self.current_path = '/'
        self.relative_path = ''
    
    def move_down(self, move_location):
        for sub_folder in self.current_dir.contents['Sub-Folders']:
            if sub_folder.folder_name == move_location:
                self.current_dir = sub_folder
                self.current_path = self.current_path + self.current_dir.folder_name + '/'

    def move_up(self):
        if self.current_dir.parent != None:
            self.current_path = self.current_path.replace(self.current_dir.folder_name + '/', '')
            self.current_dir = self.current_dir.parent
            

def main():
    root_folder = Folder.Folder('/', None)
    fs = FileSystem(root_folder)
    root_folder.add_folder(Folder.Folder('home', root_folder))
    root_folder.add_folder(Folder.Folder('etc', root_folder))
    fs.move_down('home')
    print(fs.current_dir)
    print(fs.current_path)
    fs.current_dir.add_folder(Folder.Folder('administratoor', fs.current_dir))
    print('Moved Up:')
    fs.move_down('administratoor')
    print(fs.current_dir)
    print(fs.current_path)
    fs.move_up()
    print('Moved Up:')
    print(fs.current_dir)
    print(fs.current_path)
    fs.move_up()
    print('Moved Up:')
    print(fs.current_dir)
    print(fs.current_path)
    pass

if __name__ == '__main__':
    main()
