import py_cui
import os

def ListCurrentDir():
    CurrentDirFiles = os.listdir()
    FilesListMenu = base.add_scroll_menu(title="Files in Current Directory", row=1, column=1, row_span=1, column_span=1, padx=1, pady=0)
    FilesListMenu.add_item_list(CurrentDirFiles)

def exit_script():
    exit()

while True:
    base = py_cui.PyCUI(3, 3)
    base.add_key_command(py_cui.keys.KEY_CTRL_E, exit_script)
    print(base.get_absolute_size())

    ListCurrentDir()

    base.start()