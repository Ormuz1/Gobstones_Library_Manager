import eel 
import gobstones_library as lib
import os

library_buffer = lib.GobstonesLibrary()
library_buffer.remove("Mover_VecesAl_")
library_buffer.update("PonerUnaDeCada", "procedure PonerUnaDeCada()\n{\n    Poner(Verde) Poner(Rojo) Poner(Azul) Poner(Negro)\n}")
pass