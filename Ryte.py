import py_cui
import os

class Ryte:

    def __init__(self, base):
        self.base = base

        self.FilesListMenu = base.add_scroll_menu(title="Files in Current Directory", row=0, column=0, row_span=2, column_span=2, padx=1, pady=0)
        self.FilesListMenu.add_item_list(os.listdir())

        self.UserInputBox = base.add_text_box(title="Enter File to Edit", row=3, column=3, row_span = 1, column_span = 1, padx = 1, pady = 0, initial_text="")
        
    def OpenFile(self):
        file = self.UserInputBox.get()


base = py_cui.PyCUI(4, 4)
base.set_title("Ryte Text Editor")
app = Ryte(base)
base.start()