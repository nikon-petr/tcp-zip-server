from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter import ttk

from client import Client


def start_ui():
    root = Tk()
    root.wm_title('Client')

    tree_wd = ttk.Treeview(root)
    request_btn = Button(root, text='Request', state=DISABLED)
    update_btn = Button(root, text='Update')

    tree_wd.grid(row=1, column=1, columnspan=2)
    request_btn.grid(row=2, column=1)
    update_btn.grid(row=2, column=2)

    def request(ev):
        request_path = tree_wd.item(tree_wd.focus())['values'][0]
        save_path = askdirectory(initialdir='~/')
        Client.get_directory_archive(request_path, save_path)

    def update(ev):
        tree = Client.get_directory_tree()
        for i in tree_wd.get_children():
            tree_wd.delete(i)
        update_directory_tree(tree_wd, tree['tree'])

    def allow_request(ev):
        request_btn['state'] = 'normal'

    request_btn.bind('<Button-1>', request)
    update_btn.bind('<Button-1>', update)
    tree_wd.bind('<Button-1>', allow_request)

    update(None)

    root.mainloop()


def update_directory_tree(treeview, tree_dict, parant_id=''):
    treeview.insert(parant_id, 'end', tree_dict['path'], text=tree_dict['name'], value=tree_dict['path'])
    treeview.item(tree_dict['path'], open=True)
    if tree_dict.get('children'):
        for child in tree_dict['children']:
            update_directory_tree(treeview, child, parant_id=tree_dict['path'])
