async function get_library()
{
    return await eel.get_library()();
}

function get_active_library_selector()
{
    const search = document.getElementsByClassName("library-element-selector");
    for (selector of search)
    {
        if(selector.offsetParent === null) return selector;
    }
    return null
}


function get_selected_library_element(selector)
{
    const search = selector.getElementsByClassName("active");
    return search.length === 0 ? null : search[0];  
}


function get_library_element(library, element_name)
{
    for (i in library)
    {

        for (j in library[i])
        {
            console.log(j)
            if (j === element_name)
            {
                console.log(j)
                return library[i][j]
            }
        }
    }
    return null
}

/* Initialize the library element selector.
 TODO: 
    1. Use the library element selected event for this shit.
    2. Refactor this please.
 */
function initialize_library_element_selector(library)
{
    libraryElementSelectedEvent = new Event("LibraryElementSelected");
    let all_library_elements = []
    for (const library_part in library)
    {
        let library_part_node = document.getElementById(library_part);
        console.log(library_part_node);
        for (const element in library[library_part])
        {
            const node = document.createElement("a");
            node.classList.add("collection-item", "nombre-elemento");
            const text = document.createTextNode(library_part.slice(0, -1) + " " + element);
            node.appendChild(text);
            library_part_node.appendChild(node);
            all_library_elements.push(node.cloneNode(true));
        }
    }
    const todos = document.getElementById("todos");
    all_library_elements.forEach(element => {
        todos.appendChild(element);
    });
    
    const codigo = document.getElementById("codigo");
    const element_type_tabs = document.getElementById("element-type-tabs");
    for (tab of element_type_tabs.getElementsByClassName("tab"))
    {
        tab.addEventListener("click", function() {active_library_selector = get_active_library_selector() } );
    }
    let active_library_selector = get_active_library_selector();
    const library_selectors = document.getElementsByClassName("library-element-selector");
    for (selector of library_selectors)
    {
        for(item of selector.getElementsByClassName("collection-item"))
        {
            item.addEventListener("click", function (event) {
                let selected_element = get_selected_library_element(event.target.parentElement);
                document.dispatchEvent(libraryElementSelectedEvent);
                codigo.innerText = get_library_element(library, event.target.innerText.split(" ")[1]);
                if (selected_element !== null) selected_element.classList.remove("active");
                event.target.classList.add("active");
                selected_element = event.target;
            });
        }
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    const library = await get_library();
    initialize_library_element_selector(library);

    // Initialize materialize framework elements.
    M.AutoInit();
});