from genericpath import isdir, isfile
import py_cui
import os

class Ryte:

    def __init__(self, base):
        self.base = base

        # Menu that lists files in current directory, displayed on the left of Ryte GUI
        self.FilesListMenu = self.base.add_scroll_menu(title="Select File to Edit", row=0, column=0, row_span=3, column_span=2, padx=1, pady=0)
        self.FilesListMenu.add_item_list(os.listdir())
        self.FilesListMenu.add_key_command(py_cui.keys.KEY_ENTER, self.OpenDirOrFile)

        # Editing Box
        self.EditBox = self.base.add_text_block(title="Editor", row=0, column=2, row_span=4, column_span=3, padx=1, pady=0, initial_text="")

        # Ryte Status Box (To catch and display raised exceptions)
        self.StatusBox = self.base.add_text_box(title="Ryte Status", row=3, column=0, row_span=1, column_span=2, padx=1, pady=0, initial_text="")

    def OpenDirOrFile(self):

        # Get the absolute path of the selected file or folder
        cwd = os.getcwd()
        name = self.FilesListMenu.get()
        path = os.path.join(cwd, name)

        if(os.path.exists(path)):
            if(os.path.isfile(path)):
                OpenFile = open(path, "r")
                FileData = OpenFile.read()
                OpenFile.close()

                self.EditBox.set_text(FileData)
                self.EditBox.set_title("Editing File: " + path)
                

            if(os.path.isdir(path)):
                os.chdir(path)
                data = os.listdir()
                self.FilesListMenu.add_item_list(data)


base = py_cui.PyCUI(num_rows=4, num_cols=5)
base.set_title("Ryte Text Editor")
app = Ryte(base)
base.start()