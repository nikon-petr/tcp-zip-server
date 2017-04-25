from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror
from tkinter import ttk

from client.client import Client
from client.client import ServerError
from client.client import ServerNotFound


def start_ui():

    def handle_error(decorating):
        def wrapper(*args):
            try:
                return decorating(*args)
            except ServerError as e:
                error_message(str(e))
            except ServerNotFound as e:
                error_message(str(e))
        return wrapper

    root = Tk()
    root.wm_title('Client')

    # root.resizable(0, 0)

    tree_wd = ttk.Treeview(root)
    request_btn = Button(root, text='Request', state=DISABLED)
    update_btn = Button(root, text='Update')

    tree_wd.grid(row=1, column=1, columnspan=2)
    request_btn.grid(row=2, column=1)
    update_btn.grid(row=2, column=2)

    @handle_error
    def request(ev):
        request_path = tree_wd.item(tree_wd.focus())['values'][0]
        save_path = askdirectory(initialdir='~/')
        Client.get_directory_archive(request_path, save_path)

    @handle_error
    def update(ev):
        tree = Client.get_directory_tree()
        clean_tree(tree_wd)
        update_directory_tree(tree_wd, tree)

    def allow_request(ev):
        request_btn['state'] = 'normal'

    def disallow_request():
        request_btn['state'] = 'disabled'

    def error_message(message):
        showerror('Error', message)
        clean_tree(tree_wd)
        disallow_request()

    def center(toplevel):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

    request_btn.bind('<Button-1>', request)
    update_btn.bind('<Button-1>', update)
    tree_wd.bind('<Button-1>', allow_request)

    update(None)

    center(root)

    root.mainloop()


def update_directory_tree(treeview, tree_dict, parant_id=''):
    treeview.insert(parant_id, 'end', tree_dict['path'], text=tree_dict['name'], value=tree_dict['path'])
    treeview.item(tree_dict['path'], open=True)
    if tree_dict.get('children'):
        for child in tree_dict['children']:
            update_directory_tree(treeview, child, parant_id=tree_dict['path'])


def clean_tree(tree):
    for i in tree.get_children():
        tree.delete(i)
