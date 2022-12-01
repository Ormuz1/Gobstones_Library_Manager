import eel 
import gobstones_library as lib
import tkinter as tk
from tkinter import filedialog


library_buffer = lib.GobstonesLibrary()

@eel.expose
def get_library_entry_names():
    return {
        "types": list(library_buffer.types),
        "procedures": list(library_buffer.procedures),
        "functions": list(library_buffer.functions)
    }

@eel.expose
def get_library_element(element_name):
    return library_buffer.getEntry(element_name)
                
@eel.expose
def select_and_add_file_to_library():
    window = tk.Tk()
    window.attributes('-topmost', True, '-alpha',0)
    files = filedialog.askopenfilenames(filetypes=[('gbs files', "*.gbs")], multiple=True)
    were_changes_made = False
    for file in files:
        were_changes_made = were_changes_made or library_buffer.importFileToLibrary(file)
    window.destroy()
    return were_changes_made

@eel.expose
def save_changes():
    library_buffer.exportToJSON()

@eel.expose
def select_and_save_library_to_file():
    window = tk.Tk()
    window.attributes('-topmost', True, '-alpha', 0)
    path = filedialog.asksaveasfilename(filetypes=[("GBS file", ".gbs")], defaultextension=".gbs")
    library_buffer.exportToGbsFile(path)
    window.destroy()

eel.init('gui')
eel.start('index.html')