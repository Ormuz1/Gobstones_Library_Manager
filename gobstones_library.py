"""
    TODO:
    1. Implementar correctamente is_valid().
    2. Hacer el codigo mas defensivo.
    3. Reformatear add_from_file pq es terrible spaghetti
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
            if not self.__isValid():
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
            # If there was any exception, recreate the library from scratch.
            if not success:
                print("Recreating library...")
                self.__createEmptyLibrary(filepath)
                self.__init__(filepath)

    def __createEmptyLibrary(self, filepath):
        lib = {
            "types": {},
            "procedures": {},
            "functions": {}
        }
        with open(filepath, "w") as file:
            json.dump(lib, file)

    def importFileToLibrary(self, filepath: str) -> bool:
        """Adds all the types, functions and procedures from a .gbs file to the library.

        Args:
            filepath (str): The path to the .gbs file.
        Returns:
            bool: A bool describing changes were made to the library.
        """
        # TODO: Reformat this shit.
        backup = self.to_dict()
        file_choice_window = DuplicateEntryChoiceDialog()
        parsed_file = parse_gobstones_file(filepath)
        were_changes_made = False
        for entry_type in parsed_file:
            for entry in parsed_file[entry_type]:
                if self.isEntryInLibrary(entry):
                    choice = file_choice_window.handleDuplicate(
                        getattr(self, entry_type)[entry], parsed_file[entry_type][entry])
                    if choice == "Cancel":
                        self.types = backup["types"]
                        self.procedures = backup["procedures"]
                        self.functions = backup["functions"]
                        file_choice_window.destroy()
                        return False
                    elif choice == "Keep original":
                        continue
                    elif choice == "Keep both":
                        new_entry_name = auto_rename_entry(entry)
                        while self.isEntryInLibrary(new_entry_name):
                            new_entry_name = auto_rename_entry(
                                new_entry_name)

                        new_entry_data = parsed_file[entry_type][entry]
                        entry_name_start = new_entry_data.index(" ")
                        entry_name_end = new_entry_data.index("(")
                        new_entry_data = new_entry_data[:entry_name_start] + \
                            f" {new_entry_name}" + \
                            new_entry_data[entry_name_end:]
                        getattr(self, entry_type)[
                            new_entry_name] = new_entry_data
                        continue
                getattr(self, entry_type)[
                    entry] = parsed_file[entry_type][entry]
                were_changes_made = True

        self.types = backup["types"]
        self.procedures = backup["procedures"]
        self.functions = backup["functions"]
        file_choice_window.destroy()
        return were_changes_made

    def removeEntry(self, entry_to_remove: str):
        """Removes an entry from the library.

        Args:
            entry_to_remove (str): The name (key) of the entry to be removed.
        """
        for blocktype in GobstonesLibrary.__blocktypes():
            for entry_name in getattr(self, blocktype):
                if entry_name == entry_to_remove:
                    getattr(self, blocktype).pop(entry_name)
                    return
        print("The entry to remove from the library was not found.")

    def updateEntry(self, entry_to_update: str, new_entry_data: str):
        """Updates an entry from the library-

        Args:
            entry_to_update (str): The name (key) of the entry to update.
            new_entry_data (str): The codeblock (value) to update.
        """
        for blocktype in GobstonesLibrary.__blocktypes():
            for entry_name in getattr(self, blocktype):
                if entry_name == entry_to_update:
                    getattr(self, blocktype)[
                        entry_to_update] = new_entry_data
                    return
        print("The entry to update from the library was not found.")
        pass

    def exportToJSON(self, filepath: str = DEFAULT_LIBRARY_FILE_PATH):
        """Exports the library object to a .json file.

        Args:
            filepath (str, optional): The path in which to save the .json file. 
                Defaults to DEFAULT_LIBRARY_FILE_PATH.

        TODO: Validate filepath.
        """
        library_contents = self.to_dict()
        with open(filepath, "w") as library_file:
            library_file.write(json.dumps(library_contents, indent=4))

    def exportToGbsFile(self, filepath: str = "Biblioteca.gbs"):
        """Exports the library to a GobStones .gbs file.

        Args:
            filepath (str, optional): The path for the file. Defaults to "Biblioteca.gbs".

        TODO: Validate filepath.
        """
        with open(filepath, "w", encoding='utf-8') as file:
            for blocktype in GobstonesLibrary.__blocktypes():
                for entry in getattr(self, blocktype).values():
                    file.write(entry + "\n\n")

    def __isValid(self) -> bool:
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
        return {blocktype: getattr(self, blocktype) for blocktype in GobstonesLibrary.__blocktypes()}

    def isEntryInLibrary(self, entry_name: str) -> bool:
        """Returns whether the library contains the entry of the given name.

        Args:
            entry_name (str): The name of the entry to search.

        Returns:
            bool: A boolean describing whether the entry is in the library.
        """
        for blocktype in GobstonesLibrary.__blocktypes():
            if entry_name in getattr(self, blocktype):
                return True
        return False

    def getEntry(self, entry_name: str) -> str:
        for blocktype in GobstonesLibrary.__blocktypes():
            for entry in getattr(self, blocktype):
                if entry == entry_name:
                    return getattr(self, blocktype)[entry]

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


def auto_rename_entry(entry):
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
        tk.Label(self, text="The following entry that you are trying to add:").pack(
            fill="x")
        self.newEntryText = tk.Text(self, height=5)
        self.newEntryText.pack()
        tk.Label(self, text="Has the same name as the following existing entry:").pack(
            fill="x")
        self.originalEntryText = tk.Text(self, height=5)
        self.originalEntryText.pack()
        buttonFrame = tk.Frame(self)
        buttonFrame.pack(pady=16)
        tk.Button(buttonFrame, text="Keep original",
                  command=lambda: self.__makeChoice("Keep original")).grid(padx=6)
        tk.Button(buttonFrame, text="Keep new", command=lambda: self.__makeChoice(
            "Keep new")).grid(padx=6, row=0, column=1)
        tk.Button(buttonFrame, text="Keep both", command=lambda: self.__makeChoice(
            "Keep both")).grid(padx=6, row=0, column=2)
        tk.Button(buttonFrame, text="Cancel", command=lambda: self.__makeChoice(
            "Cancel")).grid(padx=6, row=0, column=3)
        self.withdraw()

    def handleDuplicate(self, originalEntry, newEntry):
        self.newEntryText.config(state=tk.NORMAL)
        self.originalEntryText.config(state=tk.NORMAL)
        self.newEntryText.delete("1.0", "end")
        self.originalEntryText.delete("1.0", "end")
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
