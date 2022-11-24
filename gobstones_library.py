"""
    TODO:
    1. Implementar correctamente is_valid().
    2. Hacer el codigo mas defensivo.
"""
from re import split as re_split, search as re_search
import json
DEFAULT_LIBRARY_FILE_PATH = "biblioteca.json"


class GobstonesLibrary:
    def __init__(self, filepath=DEFAULT_LIBRARY_FILE_PATH):
        try:
            with open(filepath, "r") as file:
                library = json.loads(file.read())
            if not self.is_valid():
                raise InvalidLibraryError
            self.types = library["types"]
            self.procedures = library["procedures"]
            self.functions = library["functions"]

        except ValueError as e:
            raise ValueError("Error: Invalid JSON code in library file.")

        except FileNotFoundError as e:
            raise FileNotFoundError("Error: Couldn't find library file.")


    def add_from_file(self, filepath: str):
        """Adds all the types, functions and procedures from a .gbs file to the library

        Args:
            filepath (str): The path to the .gbs file.
        """
        parsed_file = parse_gobstones_file(filepath)

        for blocktype in parsed_file:
            for blockname in parsed_file[blocktype]:
                if self.is_element_in_library(blockname):
                    print(f"{blockname} already exists in the library. Skipping over...")
                    continue
                getattr(self, blocktype)[blockname] = parsed_file[blocktype][blockname]


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
        """
        library_contents = self.to_dict()
        with open(filepath, "w") as library_file:
            library_file.write(json.dumps(library_contents, indent=4))
        return
    
    
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
    

    @staticmethod
    def __blocktypes() -> tuple:
        """Returns the Gobstones blocktypes supported by the GobstonesLibrary class.

        Returns:
            tuple: A tuple containing the supported blocktypes.
        """
        return ("types", "procedures", "functions")

    
def parse_gobstones_file(filepath: str) -> dict:
    """Parses the given .gbs file into a dictionary

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

    # The re.split() function can add an empty item at the beginning which
    # fucks everything up, so we have to remove it
    if data[0] == "": 
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
