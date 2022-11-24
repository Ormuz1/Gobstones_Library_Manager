import eel 
import gobstones_library as lib
import os

library_buffer = lib.GobstonesLibrary()
@eel.expose
def get_library():
    return library_buffer.to_dict()
eel.init('gui')
eel.start('index.html')