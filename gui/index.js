let types = [], functions = [], procedures = [], todos = [];
let vue_app;

async function refresh_library()
{
    const library = await eel.get_library_entry_names()();
    types.splice(0, types.length, ...library.types);
    functions.splice(0, functions.length, ...library.functions);
    procedures.splice(0, procedures.length, ...library.procedures);
    const todos = document.getElementById("todos");
    todos.innerHTML = "";
    for (child of document.querySelectorAll(".nombre-elemento"))
    {
        todos.appendChild(child.cloneNode(true));
    }
}

async function add_file_to_library()
{
    await eel.select_and_add_file_to_library()()
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
    const contenedor_codigo = document.getElementById("codigo");
    const codigo = await eel.get_library_element(element_entry_node.innerText.split(" ")[1])();
    contenedor_codigo.innerText = codigo;
}

document.addEventListener("DOMContentLoaded", async () => {
    /*
    TODO: 
        1. Translate spanish into english.
        2. Convert "nombre-elemento" into a Vue component.
        3. Wait until page is fully loaded before showing.
        */
   await refresh_library()
   libraryElementSelectedEvent = new Event("LibraryElementSelected");
   vue_app = new Vue({
       el: '#contenedor-principal',
       data: {
           types: types,
           functions: functions,
           procedures: procedures,
           todos: todos,
           hasLibraryChanged: false
        }
    });
    M.AutoInit();
});