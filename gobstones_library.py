"""
    TODO:
    1. Implementar correctamente is_valid().
    2. Hacer el codigo mas defensivo.
"""
from re import split as re_split, search as re_search
import json
import tkinter as tk
DEFAULT_LIBRARY_FILE_PATH = "biblioteca.json"


class GobstonesLibrary:
    def __init__(self, filepath=DEFAULT_LIBRARY_FILE_PATH):
        success = False
        try:
            with open(filepath, "r") as file:
                library = json.loads(file.read())
            if not self.is_valid():
                raise InvalidLibraryError
            self.types = library["types"]
            self.procedures = library["procedures"]
            self.functions = library["functions"]
            success = True

        except ValueError as e:
            print("Invalid JSON code in library file.")

        except FileNotFoundError as e:
            print("Couldn't find library file in given path.")
        
        except InvalidLibraryError as e:
            print(str(e))
        
        finally:
            if not success:
                print("Recreating library...")
                self.__create_empty_library(filepath)
                self.__init__(filepath)

    def __create_empty_library(self, filepath):
        lib = {
            "types": {},
            "procedures": {},
            "functions": {}
        }
        with open(filepath, "w") as file:
            json.dump(lib, file)

    def add_from_file(self, filepath: str):
        """Adds all the types, functions and procedures from a .gbs file to the library

        Args:
            filepath (str): The path to the .gbs file.
        """
        # TODO: Reformat this shit.
        backup = self.to_dict()
        file_choice_window = DuplicateEntryChoiceDialog()
        parsed_file = parse_gobstones_file(filepath)
        elements_to_add = []
        for entry_type in parsed_file:
            for entry in parsed_file[entry_type]:
                if self.is_element_in_library(entry):
                    choice = file_choice_window.handleDuplicate(getattr(self, entry_type)[entry], parsed_file[entry_type][entry])
                    if choice == "Cancel":
                        self.types = backup["types"]
                        self.procedures = backup["procedures"]
                        self.functions = backup["functions"]
                        return
                    elif choice == "Keep original":
                        continue
                    elif choice == "Keep both":
                        new_entry_name = self.auto_rename_entry(entry)
                        while self.is_element_in_library(new_entry_name):
                            new_entry_name = self.auto_rename_entry(new_entry_name)
                        
                        new_entry_data = parsed_file[entry_type][entry]
                        entry_name_start = new_entry_data.index(" ")
                        entry_name_end = new_entry_data.index("(")
                        new_entry_data = new_entry_data[:entry_name_start] + f" {new_entry_name}" + new_entry_data[entry_name_end:]
                        getattr(self, entry_type)[new_entry_name] = new_entry_data
                        continue
                getattr(self, entry_type)[entry] = parsed_file[entry_type][entry]
        
        self.types = backup["types"]
        self.procedures = backup["procedures"]
        self.functions = backup["functions"]
        file_choice_window.destroy()


    def remove(self, element_to_remove: str):
        """Removes an element from the library.

        Args:
            element_to_remove (str): The name (key) of the element to be removed.
        """
        for blocktype in GobstonesLibrary.__blocktypes():
            for element_name in getattr(self, blocktype):
                if element_name == element_to_remove:
                    getattr(self, blocktype).pop(element_name)
                    return
        print("The element to remove from the library was not found.")


    def update(self, element_to_update: str, new_element_data: str):
        """Updates an element from the library-

        Args:
            element_to_update (str): The name (key) of the element to update.
            new_element_data (str): The codeblock (value) to update.
        """
        for blocktype in GobstonesLibrary.__blocktypes():
            for element_name in getattr(self, blocktype):
                if element_name == element_to_update:
                    getattr(self, blocktype)[element_to_update] = new_element_data
                    return
        print("The element to update from the library was not found.")
        pass


    def export_to_json(self, filepath:str=DEFAULT_LIBRARY_FILE_PATH):
        """Exports the library object to a .json file.

        Args:
            filepath (str, optional): The path in which to save the .json file. 
                Defaults to DEFAULT_LIBRARY_FILE_PATH.
        
        TODO: Validate filepath.
        """
        library_contents = self.to_dict()
        with open(filepath, "w") as library_file:
            library_file.write(json.dumps(library_contents, indent=4))
    
    def export_to_gbs(self, filepath:str="Biblioteca.gbs"):
        """Exports the library to a GobStones .gbs file.

        Args:
            filepath (str, optional): The path for the file. Defaults to "Biblioteca.gbs".

        TODO: Validate filepath.
        """
        with open(filepath, "w", encoding='utf-8') as file:
            for blocktype in GobstonesLibrary.__blocktypes():
                for element in getattr(self, blocktype).values():
                    file.write(element + "\n\n")
        
    def is_valid(self) -> bool:
        """Returns whether this library is valid.

        Returns:
            bool: A bool describing wether the library is valid.
        """
        # WIP
        return True


    def to_dict(self) -> dict:
        """Converts the library to a dictionary.

        Returns:
            dict: The library as a dictionary.
        """
        return {blocktype:getattr(self, blocktype) for blocktype in GobstonesLibrary.__blocktypes()}
    
    
    def is_element_in_library(self, element_name:str) -> bool:
        """Returns whether the library contains the element of the given name.

        Args:
            element_name (str): The name of the element to search.

        Returns:
            bool: A boolean describing whether the element is in the library.
        """
        for blocktype in GobstonesLibrary.__blocktypes():
            if element_name in getattr(self, blocktype):
                return True
        return False
    
    def get_element(self, element_name:str) -> str:
        for blocktype in GobstonesLibrary.__blocktypes():
            for entry in getattr(self, blocktype):
                if entry == element_name:
                    return getattr(self, blocktype)[entry]
    def auto_rename_entry(self, entry):
        new_entry_name = entry
        
        try: 
            if new_entry_name[-2] != "_":
                raise Exception
            entry_number = int(entry[-1])
            new_entry_name = entry[:-1] + str(entry_number + 1)
        except Exception as e:
            if new_entry_name[-1] != "_":
                new_entry_name += "_"
            new_entry_name += "1"
        return new_entry_name
    @staticmethod
    def __blocktypes() -> tuple:
        """Returns the Gobstones blocktypes supported by the GobstonesLibrary class.

        Returns:
            tuple: A tuple containing the supported blocktypes.
        """
        return ("types", "procedures", "functions")

    
def parse_gobstones_file(filepath: str) -> dict:
    """Parses the given .gbs file into a dictionary containing its types, functions and procedures.

    Args:
        filepath (str): The path to the .gbs file.

    Returns:
        dict: A dictionary containing the supported blocktype names and their code.
    """
    # TODO: Validate given filepath.
    data = ""
    parsed_data = {
        "functions": {},
        "types": {},
        "procedures": {}
    }

    with open(filepath, "r", encoding='utf-8') as file:
        data = re_split(r"(type|function|procedure|program)", file.read())

    # The re.split() function adds a wrong item at the beginning which
    # fucks everything up, so we have to remove it
    data = data[1:]
    
    for i in range(0, len(data), 2):
        token = data[i]
        # 'program' blocks must be skipped.
        if token == "program":
            continue

        block = token + data[i + 1]
        block_name = re_search("\s+(\w+)", data[i + 1]).group().strip()
        if token == "type":
            parsed_data["types"][block_name] = block
        elif token == "procedure":
            parsed_data["procedures"][block_name] = block
        elif token == "function":
            parsed_data["functions"][block_name] = block

    return parsed_data



class InvalidLibraryError(Exception):
    def __init__(self, library_file, *args):
        super().__init__(args)
        self.library_file = library_file

    def __str__(self):
        return f'The Gobstones library found at {self.library_file} was invalid.'

class DuplicateEntryChoiceDialog(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x300")
        tk.Label(self, text="The following entry that you are trying to add:").pack(fill="x")
        self.newEntryText = tk.Text(self, height=5)
        self.newEntryText.pack()
        tk.Label(self, text="Has the same name as the following existing entry:").pack(fill="x")
        self.originalEntryText = tk.Text(self, height=5)
        self.originalEntryText.pack()
        buttonFrame = tk.Frame(self)
        buttonFrame.pack(pady=16)
        tk.Button(buttonFrame, text="Keep original", command=lambda: self.__makeChoice("Keep original")).grid(padx=6)
        tk.Button(buttonFrame, text="Keep new", command=lambda: self.__makeChoice("Keep new")).grid(padx=6, row=0, column=1)
        tk.Button(buttonFrame, text="Keep both", command=lambda: self.__makeChoice("Keep both")).grid(padx=6, row=0, column=2)
        tk.Button(buttonFrame, text="Cancel", command=lambda: self.__makeChoice("Cancel")).grid(padx=6, row=0, column=3)
        self.withdraw()

    def handleDuplicate(self, originalEntry, newEntry):
        self.newEntryText.config(state=tk.NORMAL)
        self.originalEntryText.config(state=tk.NORMAL)
        self.newEntryText.insert(tk.INSERT, newEntry)
        self.originalEntryText.insert(tk.INSERT, originalEntry)
        self.newEntryText.config(state=tk.DISABLED)
        self.originalEntryText.config(state=tk.DISABLED)
        self.choice = None
        self.deiconify()
        while (self.choice is None):
            self.update()
            self.update_idletasks()
        self.withdraw()
        return self.choice

    def __makeChoice(self, choice):
        self.choice = choice
