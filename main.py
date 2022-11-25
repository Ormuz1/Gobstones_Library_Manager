import eel 
import gobstones_library as lib
import os

library_buffer = lib.GobstonesLibrary()
@eel.expose
def get_library_entry_names():
    print({
        "types": library_buffer.types.keys(),
        "procedures": library_buffer.procedures.keys(),
        "functions": library_buffer.functions.keys()
    })
    return {
        "types": list(library_buffer.types),
        "procedures": list(library_buffer.procedures),
        "functions": list(library_buffer.functions)
    }

@eel.expose
def get_library_element(element_name):
    return library_buffer.get_element(element_name)
                
eel.init('gui')
eel.start('index.html')