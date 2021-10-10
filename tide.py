from genericpath import isdir, isfile
import traceback
import py_cui
import os
import argparse

class Tide:

    def __init__(self, base, startdir):

        try:
            os.chdir(dir)

        except Exception:
            self.UpdateStatus(Exception)

        self.base = base
        self.base.set_title("Tide: Terminal Integrated Development Enviroment")

        # Menu that lists all of the Tide Operations
        self.operations = ["Save File (CTRL-s)", "Create New File (CTRL-n)", "Refresh Editor (CTRL-r)", "Delete File (CTRL-d)", "Quick Directory Change (CTRL-q)"]
        self.OperationsMenu = self.base.add_scroll_menu(title="Tide Operations List", row=0, column=0, row_span=1, column_span=2, padx=1, pady=0)
        self.OperationsMenu.add_item_list(self.operations)
        self.OperationsMenu.set_color(py_cui.CYAN_ON_BLACK)
        self.OperationsMenu.add_key_command(py_cui.keys.KEY_ENTER, self.OperationsMenuFunction)

        # Menu that lists files in current directory, displayed on the left of Tide GUI
        self.DirNav = self.base.add_scroll_menu(title="Directory Navigation", row=1, column=0, row_span=5, column_span=2, padx=1, pady=0)
        self.DirNav.add_item_list(os.listdir())
        self.DirNav.set_color(py_cui.CYAN_ON_BLACK)
        self.DirNav.add_key_command(py_cui.keys.KEY_ENTER, self.OpenFileOrDir)
        self.DirNav.add_key_command(py_cui.keys.KEY_BACKSPACE, self.ChangeToParentDir)
        self.DirNav.add_key_command(py_cui.keys.KEY_CTRL_D, self.DeleteFile)


        # Tide Status Box (To catch and display raised exceptions)
        self.StatusBox = self.base.add_text_block(title="Tide Status", row=6, column=0, row_span=1, column_span=10, padx=1, pady=0, initial_text="")
        self.StatusBox.set_color(py_cui.GREEN_ON_BLACK)

        # Editing Box
        self.EditBox = self.base.add_text_block(title="Editor", row=0, column=2, row_span=6, column_span=8, padx=1, pady=0, initial_text="")
        self.EditBox.set_color(py_cui.CYAN_ON_BLACK)
        self.EditBox.add_key_command(py_cui.keys.KEY_CTRL_S, self.SaveOpenFile)
        self.EditBox.add_key_command(py_cui.keys.KEY_CTRL_N, self.CreateNewFilePrompt)
        self.EditBox.add_key_command(py_cui.keys.KEY_CTRL_R, self.RefreshEditBox)

    def OperationsMenuFunction(self):
        try:
            SelectedOperation = self.OperationsMenu.get()

            for AvailableOperations in self.operations:
                if(AvailableOperations == SelectedOperation):

                    # Save File
                    if(SelectedOperation == self.operations[0]):
                        self.SaveOpenFile()

                    # Create New File
                    if(SelectedOperation == self.operations[1]):
                        self.CreateNewFilePrompt()

                    # Refresh Edit Box
                    if(SelectedOperation == self.operations[2]):
                        self.RefreshEditBox()

                    # Delete File
                    if(SelectedOperation == self.operations[3]):
                        self.DeleteFile()

        except Exception:
            self.UpdateStatus(Exception)

    # Function wraps the py_cui API warning popup to make it easier to call
    def ShowWarningPopup(self, title, msg):
        try:
            self.base.show_warning_popup(title, msg)

        except Exception:
            self.UpdateStatus(Exception)

    # Function wraps the py_cui API error popup to make it easier to call
    def ShowErrorPopup(self, title, msg):
        try:
            self.base.show_error_popup(title, msg)

        except Exception:
            self.UpdateStatus(Exception)

    # Function wraps the py_cui API message popup to make it easier to call
    def ShowMsgPopup(self, title, msg):
        try:
            self.base.show_message_popup(title, msg)

        except Exception:
            self.UpdateStatus(Exception)

    def DeleteFile(self):
        try:
            file = self.DirNav.get()
            path = os.path.abspath(file)

            def Delete(choice):
                if(choice == True):
                    os.remove(path)
                    self.ShowMsgPopup("File Deleted.", "This file has been deleted: " + path)
                    self.UpdateStatus("File deleted: " + path)
                    self.DirNav.clear()
                    self.DirNav.add_item_list(os.listdir())
                    self.RefreshEditBox()

                if(choice == False):
                    self.ShowMsgPopup("File Not Deleted.", "The file deletion operation has been cancelled.")
                    self.UpdateStatus("File Not Deleted. The file deletion operation has been cancelled.")

            if(os.path.exists(path)):
                self.base.show_yes_no_popup("Confirm deletion of file: " + path, Delete)

        except Exception:
            self.UpdateStatus(Exception)

    # If file is open in editor, save the opened file
    def SaveOpenFile(self):
        try:
            if(self.EditBox.get_title() != "Editor"):
                file = open(self.EditBox.get_title(), "w")
                file.write(self.EditBox.get())
                file.close()
                self.ShowMsgPopup("File Saved.", "The file has been saved as: " + self.EditBox.get_title())
                self.UpdateStatus("File Saved As: " + self.EditBox.get_title())
            
            else:
                self.ShowWarningPopup("Unable to save file.", "There is no file open in the editor.")
                self.UpdateStatus("Unable to save file. There isn't a file open in the editor.")

        except Exception:
            self.UpdateStatus(Exception)

    def CreateNewFilePrompt(self):
        try:
            def CreateNewFile(file):
                f = open(file, "x")
                f.write(self.EditBox.get())
                f.close()
                self.DirNav.clear()
                self.DirNav.add_item_list(os.listdir())
                self.UpdateStatus("New file created: " + os.path.abspath(file))

            if(self.EditBox.get_title() == "Editor"):
                self.base.show_text_box_popup("File to save name: ", CreateNewFile)

        except Exception:
            self.UpdateStatus(Exception)

    def RefreshEditBox(self):
        try:
            self.EditBox.clear()
            self.EditBox.set_title("Editor")

        except Exception:
            self.UpdateStatus(Exception)

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
                    self.EditBox.set_title(path)
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
            self.StatusBox.set_color(py_cui.GREEN_ON_BLACK)
            self.StatusBox.set_text(UpdateContent)

        except Exception:
            self.ShowErrorPopup("IDE Error", "View the Tide Status Box for specifics.")
            error = traceback.format_exc()
            self.StatusBox.set_text("Error: " + error)
            self.StatusBox.set_color(py_cui.RED_ON_BLACK)

def ParseCMDArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-startdir", help="Directory to start Tide in.", type=str)
    args = vars(parser.parse_args())

    print(args)

ParseCMDArgs()

base = py_cui.PyCUI(num_rows=7, num_cols=10)
app = Tide(base, startdir="D:\Stuff\PythonProjects\Tide\py_cui-docs")
base.start()