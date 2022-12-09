let wasLibraryChanged = false;
async function refresh_library() {
  /**
   * Recreates the HTML that represents the library.
   */
  const entries = await eel.get_library_entry_names()();

  const types_element = document.getElementById("types");
  types_element.innerHTML = "";
  const functions_element = document.getElementById("functions");
  functions_element.innerHTML = "";
  const procedures_element = document.getElementById("procedures");
  procedures_element.innerHTML = "";
  const todos_element = document.getElementById("todos");
  todos_element.innerHTML = "";
  pairs = [
    [entries.types, types_element, "Type "],
    [entries.functions, functions_element, "Function "],
    [entries.procedures, procedures_element, "Procedure "],
  ];

  for (pair of pairs) {
    pair[0].forEach((entry) => {
      const entry_element = createLibraryEntryHTMLNode(pair[2] + entry);
      pair[1].appendChild(entry_element);

      const clone = createLibraryEntryHTMLNode(pair[2] + entry);
      todos_element.appendChild(clone);
    });
  }
}

function createLibraryEntryHTMLNode(content) {
  /**
   * Create an HTML node for a library entry.
   */
  const wrapper = document.createElement("div");
  wrapper.classList.add("library-entry-wrapper", "valign-wrapper");

  const element = document.createElement("a");
  element.classList.add("collection-item", "library-entry-name");
  element.innerText = content;
  wrapper.appendChild(element);
  element.onclick = () => {
    show_library_entry_code(element);
  };

  const delete_icon = document.createElement("i");
  delete_icon.classList.add("material-icons", "collection-item");
  delete_icon.innerText = "delete_forever";
  wrapper.appendChild(delete_icon);
  delete_icon.onclick = () => {
    remove_library_entry(element);
  };
  return wrapper;
}

async function add_file_to_library() {
  /**
   * Selects a GobStones file from the file system and adds the contents to the library.
   */
  if ((await eel.select_and_add_file_to_library()()) && !wasLibraryChanged) {
    OnLibraryChanged();
  }
  await refresh_library();
}

async function export_library_to_gbs() {
  /**
   * Exports the library to a .gbs file.
   */
  await eel.select_and_save_library_to_file();
}

async function save_library_changes() {
  /**
   * Saves all changes made to the library.
   */
  await eel.save_changes()();
  OnLibrarySaved();
}

async function revert_library_changes() {
  /**
   * Reverts all changes made to the library since the last time it was saved.
   */
  await eel.revert_changes()();
  OnLibrarySaved();
  await refresh_library();
}


async function show_library_entry_code(element_entry_node) {
  /** 
   * Shows the code of the given element entry in the HTML element with id "library-entry-code".
  */
  const code_html_element = document.getElementById("library-entry-code");
  const code = await eel.get_library_element(
    element_entry_node.innerText.split(" ")[1]
  )();
  code_html_element.innerText = code;
}

async function remove_library_entry(element_entry_node) {
  /**
   * Removes the given library entry.
   */
  const entry_name = element_entry_node.innerText.split(" ")[1];
  await eel.delete_library_entry(entry_name)();
  await refresh_library();
  OnLibraryChanged();
}

function OnLibraryChanged() {
  wasLibraryChanged = true;
  const library_changed_alert = document.getElementById(
    "library-changed-alert"
  );
  library_changed_alert.style.display = "block";
}

function OnLibrarySaved() {
  const library_changed_alert = document.getElementById(
    "library-changed-alert"
  );
  library_changed_alert.style.display = "none";
}

document.addEventListener("DOMContentLoaded", async () => {
  M.AutoInit();
  await refresh_library();
});
