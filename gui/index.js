let wasLibraryChanged = false;

async function refresh_library() {
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

  for (pair of pairs)
  {
    pair[0].forEach(entry => {
        const entry_element = createLibraryEntryElement(pair[2] + entry);
        pair[1].appendChild(entry_element);
        entry_element.onclick = () => {show_library_entry(entry_element);};
        
        const clone = entry_element.cloneNode(true);
        todos_element.appendChild(clone);
        clone.onclick = () => {show_library_entry(clone);}
    })
  }
}


function createLibraryEntryElement(content)
{
    const element = document.createElement("a");

    element.classList.add("collection-item", "library-entry-name");
    element.innerHTML = content;
    return element;
}



async function add_file_to_library() {
  if (await eel.select_and_add_file_to_library()() && !wasLibraryChanged)
  {
    OnLibraryChanged();
  }
  await refresh_library();
}

async function export_library_to_gbs() {
  await eel.select_and_save_library_to_file();
}

async function save_library_changes() {
  await eel.save_changes()();
  OnLibrarySaved()
}

async function show_library_entry(element_entry_node) {
  const code_html_element = document.getElementById("library-entry-code");
  const code = await eel.get_library_element(
    element_entry_node.innerText.split(" ")[1]
  )();
  code_html_element.innerText = code;
}

function OnLibraryChanged()
{
    wasLibraryChanged = true;
    const library_changed_alert = document.getElementById("library-changed-alert");
    library_changed_alert.style.display = "block";
}

function OnLibrarySaved()
{
    const library_changed_alert = document.getElementById("library-changed-alert");
    library_changed_alert.style.display = "none";
}

document.addEventListener("DOMContentLoaded", async () => {

  M.AutoInit();
  await refresh_library();
  libraryElementSelectedEvent = new Event("LibraryElementSelected");
});
