from genericpath import isdir, isfile
import traceback
import py_cui
import os

class Tide:

    def __init__(self, base):
        self.base = base
        self.base.set_title("Tide: Terminal Integrated Development Enviroment")

        # Menu that lists all of the Tide Operations
        self.commands = ["Open File (CTRL-o)", "Locate File (CTRL-l)"]
        self.OperationsMenu = self.base.add_scroll_menu(title="Tide Operations", row=0, column=0, row_span=2, column_span=2, padx=1, pady=0)
        self.OperationsMenu.add_item_list(self.commands)
        self.OperationsMenu.set_color(py_cui.CYAN_ON_BLACK)
        

        # Menu that lists files in current directory, displayed on the left of Tide GUI
        self.DirNav = self.base.add_scroll_menu(title="Directory Navigation", row=2, column=0, row_span=2, column_span=2, padx=1, pady=0)
        self.DirNav.add_item_list(os.listdir())
        self.DirNav.add_key_command(py_cui.keys.KEY_ENTER, self.OpenFileOrDir)
        self.DirNav.add_key_command(py_cui.keys.KEY_BACKSPACE, self.ChangeToParentDir)
        self.DirNav.set_color(py_cui.CYAN_ON_BLACK)

        # Tide Status Box (To catch and display raised exceptions)
        self.StatusBox = self.base.add_text_block(title="Tide Status", row=4, column=0, row_span=1, column_span=5, padx=1, pady=0, initial_text="")
        self.StatusBox.set_color(py_cui.CYAN_ON_BLACK)

        # Editing Box
        self.EditBox = self.base.add_text_block(title="Editor", row=0, column=2, row_span=4, column_span=3, padx=1, pady=0, initial_text="")
        self.EditBox.set_color(py_cui.CYAN_ON_BLACK)

    def OpenFileOrDir(self):
        try: 
            # Get the absolute path of the selected file or folder
            name = self.DirNav.get()
            path = os.path.abspath(name)

            if(os.path.exists(path)):

                if(os.path.isfile(path)):
                    OpenFile = open(path, "r")
                    FileData = OpenFile.read()
                    OpenFile.close()

                    self.EditBox.set_text(FileData)
                    self.EditBox.set_title("Editing File: " + path)
                    self.UpdateStatus("Editing File: " + path)

                if(os.path.isdir(path)):
                    os.chdir(path)
                    cwd = os.getcwd()
                    files = os.listdir()
                    self.DirNav.clear()
                    self.DirNav.add_item_list(files)
                    self.UpdateStatus("Navigated to new directory: " + path)

        except Exception:
            self.UpdateStatus(Exception)

    def ChangeToParentDir(self):
        try:
            ParentDir = os.path.dirname(os.getcwd())
            ParentDirAbsPath = os.path.abspath(ParentDir)
            if(os.path.isdir(ParentDirAbsPath)):
                os.chdir(ParentDirAbsPath)
                files = os.listdir()
                self.DirNav.clear()
                self.DirNav.add_item_list(files)

        except Exception:
            self.UpdateStatus(Exception)

    def UpdateStatus(self, UpdateContent):
        try:
            self.StatusBox.clear()
            self.StatusBox.set_text(UpdateContent)

        except Exception:
            error = traceback.format_exc()
            self.StatusBox.set_text("Error: " + error)

base = py_cui.PyCUI(num_rows=5, num_cols=5)
app = Tide(base)
base.start()