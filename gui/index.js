let types = [], functions = [], procedures = [], all_entries = [];
let vue_app;


async function refresh_library()
{
    const library = await eel.get_library_entry_names()();
    types.splice(0, types.length, ...library.types);
    functions.splice(0, functions.length, ...library.functions);
    procedures.splice(0, procedures.length, ...library.procedures);
    vue_app.$nextTick( () => {
        const all_entries_html_element = document.getElementById("todos");
        all_entries_html_element.innerHTML = "";
        for (child of document.querySelectorAll(".library-entry-name"))
        {
            all_entries_html_element.appendChild(child.cloneNode(true));
        }
    }
    )
}


async function add_file_to_library()
{
    await eel.select_and_add_file_to_library()()
    console.log("finished");
    vue_app.hasLibraryChanged = true;
    await refresh_library()
}


async function export_library_to_gbs()
{
    await eel.select_and_save_library_to_file()
}

async function save_library_changes()
{
    await eel.save_changes()()
    vue_app.hasLibraryChanged = false;
}

async function show_library_entry(element_entry_node)
{
    const code_html_element = document.getElementById("library-entry-code");
    const code = await eel.get_library_element(element_entry_node.innerText.split(" ")[1])();
    code_html_element.innerText = code;
}

document.addEventListener("DOMContentLoaded", async () => {
    /*
    TODO: 
        2. Convert "library-entry-name" into a Vue component.
        3. Wait until page is fully loaded before showing.
    */
   vue_app = new Vue({
       el: '#main-container',
       data: {
           types: types,
           functions: functions,
           procedures: procedures,
           hasLibraryChanged: false
        }
    });
   await refresh_library()
   libraryElementSelectedEvent = new Event("LibraryElementSelected");
    M.AutoInit();
});