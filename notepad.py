import tkinter as tk
import tkinter.filedialog as tkDialog
import tkinter.messagebox as msg
from pathlib import Path

root = tk.Tk()

original_text = ""
current_path = ""

text_widget = tk.Text(root, wrap=tk.CHAR)
text_widget.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))


#Commands
def create_new_command(event=None):
    if original_text == text_widget.get("1.0", "end-1c"):
        create_new()
    else:
        res = msg.askyesno("Warning", "This file is not saved. Do you want to save?")
        if res == True:
            check_existance()
        else:
            create_new()
    return

def open_file_command(event=None):
    if original_text != text_widget.get("1.0", "end-1c"):
        res = msg.askyesno("Warning", "This file is not saved. Do you want to save?")
        if res == True:
            check_existance()
            
    open_file()
    return

def over_write_command(event=None):
    check_existance()
    return

def save_file_as_command(event=None):
    save_as()
    return

def on_quit(event=None):
    global original_text
    if original_text != text_widget.get("1.0", "end-1c"):
        res = msg.askyesno("Warning", "This file is not saved. Do you want to save?")
        if res == True:
            check_existance()
    
    root.destroy()
    return


#Functions
def create_new():
    global original_text
    
    text_widget.delete("1.0", "end-1c")
    root.title("Notepad - Untitled")
    original_text = ""

def open_file():
    global original_text
    global current_path

    file_path = tkDialog.askopenfile(filetypes=[('テキストファイル', '*.txt')])
    text_widget.delete("1.0", "end-1c")
    text_widget.insert(tk.INSERT, file_path.read())

    root.title("Notepad - " + file_path.name)
    original_text = text_widget.get("1.0", "end-1c")
    current_path = file_path.name
    file_path.close()

def save_as():
    global original_text
    global current_path

    file_path = tkDialog.asksaveasfilename(filetypes=[('テキストファイル', '*.txt')])
    if file_path != "":
        with open(file_path, "w") as f:
            f.write(text_widget.get("1.0", "end-1c"))

            root.title("Notepad - " + f.name)
            original_text = text_widget.get("1.0", "end-1c")
            current_path = f.name
            f.close

def over_write():
    global original_text
    global current_path

    with open(current_path, "w") as f:
        f.write(text_widget.get("1.0", "end-1c"))

        root.title("Notepad - " + f.name)
        original_text = text_widget.get("1.0", "end-1c")
        current_path = f.name
        f.close

def check_existance():
    file = Path(current_path)
    if file.is_file() == True:
        over_write()
    else:
        save_as()

def create_menubar(root):
    """メニューバーを作成する"""
    menubar = tk.Menu(root)

    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="新規(N)", command=create_new_command)
    filemenu.add_command(label="開く(O)...", command=open_file_command)
    filemenu.add_command(label="上書き保存(S)", command=over_write_command)
    filemenu.add_command(label="名前を付けて保存(A)...", command=save_file_as_command)
    filemenu.add_separator()
    filemenu.add_command(label="終了(X)", command=on_quit)
    menubar.add_cascade(label="ファイル(F)", menu=filemenu)
    
    
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About...")
    menubar.add_cascade(label="ヘルプ(H)", menu=helpmenu)
    
    root.config(menu=menubar)


create_menubar(root)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.bind('<Control-KeyPress-s>', over_write_command)
root.bind('<Control-KeyPress-S>', save_file_as_command)
root.bind('<Control-KeyPress-n>', create_new_command)
root.bind('<Control-KeyPress-o>', open_file_command)
root.bind('<Control-KeyPress-x>', on_quit)
root.protocol("WM_DELETE_WINDOW", on_quit)

root.title("Notepad - Untitled")
root.geometry("400x400")
root.mainloop()