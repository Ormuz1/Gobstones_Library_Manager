async function show_library_entry(element_entry_node)
{
    const contenedor_codigo = document.getElementById("codigo");
    console.log(element_entry_node.innerText.split(" "[1]));
    const codigo = await eel.get_library_element(element_entry_node.innerText.split(" ")[1])();
    console.log(codigo);
    contenedor_codigo.innerText = codigo;
}

document.addEventListener("DOMContentLoaded", async () => {
    /*
    TODO: 
        1. Translate spanish into english.
        2. Convert "nombre-elemento" into a Vue component.
    */
    libraryElementSelectedEvent = new Event("LibraryElementSelected");
    const library = await eel.get_library_entry_names()();
    const library_selector = new Vue({
        el: '#contenedor-nombres-elementos',
        data: {
            types: library.types,
            procedures: library.procedures,
            functions: library.functions
        }
    })

    const todos = document.getElementById("todos");
    for (child of document.querySelectorAll(".nombre-elemento"))
    {
        todos.appendChild(child.cloneNode(true));
    }
    M.AutoInit();
});