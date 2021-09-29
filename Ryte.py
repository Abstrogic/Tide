import py_cui
import os

class FileSelectionList:

    def __init__(self, base):
        FilesListMenu = base.add_scroll_menu(title="Files in Current Directory", row=0, column=0, row_span=3, column_span=3, padx=1, pady=0)
        FilesListMenu.add_item_list(os.listdir())

class Ryte:

    def __init__(self, base):
        self.base = base
        self.main()

    def main(self):
        FileSelectionList(self.base)

base = py_cui.PyCUI(3, 3)
app = Ryte(base)
base.start()