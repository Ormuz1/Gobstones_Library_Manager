import eel 
import gobstones_library as lib
import os
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
    return library_buffer.get_element(element_name)
                
@eel.expose
def select_and_add_file_to_library():
    window = tk.Tk()
    window.attributes('-topmost', True, '-alpha',0)
    files = filedialog.askopenfilenames(filetypes=[('gbs files', "*.gbs")], multiple=True)
    for file in files:
        library_buffer.add_from_file(file)
    window.destroy()

@eel.expose
def save_changes():
    library_buffer.export_to_json()

@eel.expose
def select_and_save_library_to_file():
    window = tk.Tk()
    window.attributes('-topmost', True, '-alpha',0)
    path = filedialog.asksaveasfilename(filetypes=[("GBS file", ".gbs")], defaultextension=".gbs")
    library_buffer.export_to_gbs(path)
    window.destroy()


eel.init('gui')
eel.start('index.html')