biblioteca = {
    "types": {
        "EmpresaDeBuses": "type EmpresaDeBuses is record {\n/*\n PROP\u00d3SITO: Modela una empresa de buses.\n  INV.REP:\n  * El campo\u201drutaARealizar\u201d de cualquier pasaje vendido en *pasajes* se corresponde\n    con alg\u00fan n\u00famero en el campo \u201crutaId\u201d de alguna ruta en *rutas*.\n  * El campo \u201cviajeAsignado\u201d de cualquier pasaje vendido en *pasajes* se\n    corresponde con alg\u00fan n\u00famero en el campo\u201dn\u00fameroDeViaje\u201d de alg\u00fan viaje en\n    *viajes*.\n  * No hay dos rutas en *rutas* con el mismo n\u00famero de id.\n  * No hay dos viajes en *viajes* con el mismo n\u00famero de viaje.\n  * No hay dos pasajes vendidos en *pasajes* con el mismo nombre de cliente.\n  * No hay dos pasajes vendidos en *pasajes* que contengan el mismo n\u00famero\n    de viaje pero distinto n\u00famero de ruta.\n*/\n  field rutas      // [Ruta]\n  field viajes     // [ViajeEnBus]\n  field pasajes    // [PasajeVendido]\n}",
        "Ruta": "type Ruta is record {\n/*\n  PROP\u00d3SITO: Modela una ruta.\n  INV.REP:\n  * *origen* y *destino* son\n    diferentes y no son el string\n    vac\u00edo.\n  * *rutaId* es mayor a cero.\n*/\n  field rutaId  // N\u00famero\n  field origen  // String\n  field destino // String\n}",
        "ViajeEnBus": "type ViajeEnBus is record {\n/*\n  PROP\u00d3SITO: Modela un viaje en bus.\n  INV.REP:\n  * *capacidad*, *n\u00fameroDeViaje* y\n    *horaDeSalida* son todos mayores a\n    cero.\n  * *horaDeLlegada* es mayor a\n    *horaDeSalida*.\n*/\n  field n\u00fameroDeViaje  // N\u00famero\n  field horaDeSalida   // N\u00famero\n  field horaDeLlegada  // N\u00famero\n  field tipoDeVeh\u00edculo // TipoDeBus\n  field capacidad      // N\u00famero\n}",
        "PasajeVendido": "type PasajeVendido is record {\n/*\n  PROP\u00d3SITO: Modela un pasaje vendido\n    a un pasajero.\n  INV.REP:\n  * *nombrePasajero* no es el string\n    vac\u00edo.\n  * *rutaARealizar* y *viajeAsignado*\n    son ambos mayores a cero.\n*/\n  field nombrePasajero // String\n  field rutaARealizar  // N\u00famero\n  field viajeAsignado  // N\u00famero\n}",
        "TipoDeBus": "type TipoDeBus is variant {\n/*\n  PROP\u00d3SITO: Modela los distintos tipos\n  de buses.\n*/\n  case Simple    {}\n  case DoblePiso {}\n  case Pullman   {}\n}"
    },
    "procedures": {
        "Mover_VecesAl_": "procedure Mover_VecesAl_(cantidadAMover, direccionAMover)\n{\n    repeat (cantidadAMover) { Mover(direccionAMover)}\n}",
        "PonerUnaDeCada": "procedure PonerUnaDeCada()\n{\n    Poner(Rojo) Poner(Verde) Poner(Azul) Poner(Negro)\n}",
        "Poner_DeColor_": "procedure Poner_DeColor_(cantidadAPoner, colorAPoner)\n{\n    repeat(cantidadAPoner) { Poner(colorAPoner)}\n}",
        "Sacar_DeColor_": "procedure Sacar_DeColor_(cantidadASacar, colorASacar)\n{\n    repeat (cantidadASacar) { Sacar(colorASacar) }\n}",
        "VaciarCelda": "procedure VaciarCelda(){\n    SacarTodasDeColor_(Rojo)\n    SacarTodasDeColor_(Negro)\n    SacarTodasDeColor_(Verde)\n    SacarTodasDeColor_(Azul)\n}\n\n",
        "SacarTodasDeColor_": "procedure SacarTodasDeColor_(color)\n{\n    repeat (nroBolitas(color))\n    {\n        Sacar(color)\n    }\n}"
    },
    "functions": {
        "viajesDeDoblePisoSobrevendidosEn_": "function viajesDeDoblePisoSobrevendidosEn_(empresaDeBuses){\n    /*\n        PROPOSITO: describe la lista con los n\u00fameros de viajes \n            que son en veh\u00edculos de doble piso y que han sido \n            sobrevendidos.\n        PARAMETROS: \n            - empresaDeBuses: EmpresaDeBuses\n        PRECONDICIONES:\n            - No tiene\n        TIPO: [N\u00famero]\n        OBSERVACIONES: Estrategia de filtro\n    */\n    \n    viajesSobrevendidos := []\n    \n    foreach viaje in viajes(empresaDeBuses){\n        viajesSobrevendidos:= viajesSobrevendidos ++ \n            singular_Si_(n\u00fameroDeViaje(viaje), esUnViaje_ConBusDeDoblePisoYEstaSobrevendidoEn_(viaje,empresaDeBuses) )\n    }\n    return (viajesSobrevendidos)\n}",
        "esUnViaje_ConBusDeDoblePisoYEstaSobrevendidoEn_": "function esUnViaje_ConBusDeDoblePisoYEstaSobrevendidoEn_(viaje, empresa){\n    /*\n        PROPOSITO: indica si el viaje dado es doble y esta sobrevendido\n        PARAMETROS: \n            - viaje: ViajeEnBus\n            - empresa: EmpresaDeBuses\n        PRECONDICIONES:\n            - No tiene\n        TIPO: Booleano\n    */\n    \n    return( TipoDeBus(viaje) == DoblePiso && longitudDe_(pasajesVendidosEnViaje_En_(viaje, empresa)) > capacidad(viaje))\n    \n}",
        "cantidadDePasajesVendidosEnViaje_En_": "function cantidadDePasajesVendidosEnViaje_En_(viaje, empresa){\n    /*\n        PROPOSITO: describe la cantidad de pasajes vendidos que \n            tiene el viaje dado en la empresa dada\n        PARAMETROS: \n            - viaje: ViajeEnBus\n            - empresa: EmpresaDeBuses\n        PRECONDICIONES:\n            - No tiene\n        TIPO: N\u00famero\n        OBSERVACIONES: recorrido de acumulaci\u00f3n\n    */\n    \n    cantidadDePasajesVendidosHastaAhora:= 0\n    foreach pasaje in pasajes(empresa){\n        cantidadDePasajesVendidosHastaAhora:= cantidadDePasajesVendidosHastaAhora +\n            unoSi_CeroSino(n\u00fameroDeViaje(viaje) == viajeAsignado(pasaje))\n    }\n    return(cantidadDePasajesVendidosHastaAhora)\n}",
        "pasajesVendidosEnViaje_En_": "function pasajesVendidosEnViaje_En_(viaje, empresa){\n    pasajesVistosHastaAhora:= []\n    foreach pasaje in pasajes(empresa){\n        pasajesVistosHastaAhora:= pasajesVistosHastaAhora ++\n            singular_Si_(pasaje, n\u00fameroDeViaje(viaje) == viajeAsignado(pasaje))\n    }\n    return(pasajesVistosHastaAhora)\n}",
        "destinoDelPasajeroLlamado_En_": "function destinoDelPasajeroLlamado_En_(nombreDePasajero, empresa){\n    /*\n        PROPOSITO: describe el destino que tiene el pasaje vendido a ese \n            pasajero en la empresa. Si no tiene, devuelve \u201cPASAJERO INV\u00c1LIDO\u201d.\n        PARAMETROS: \n            - nombreDePasajero: String\n            - empresa: EmpresaDeBuses\n        PRECONDICIONES:\n            - No tiene\n        TIPO: String\n    */  \n    \n    return(\n        choose  destinoDelPasaje_En_(pasajeDePasajeroLlamado_En_(nombreDePasajero,empresa),empresa) when (hayPasajeConPasajero_En_(nombreDePasajero,empresa))\n                \"PASAJERO INVALIDO\" otherwise\n        )\n}",
        "hayPasajeConPasajero_En_": "function hayPasajeConPasajero_En_(nombreDePasajero,empresa){\n    /*\n        PROPOSITO: indicando si hay un pasaje con el nombre de pasajero dado en la empresa.\n        PARAMETROS: \n            - nombreDePasajero: String\n            - empresa: EmpresaDeBuses\n        PRECONDICIONES:\n            - No tiene\n        TIPO: Booleano\n        OBSERVACIONES: recorrido de b\u00fasqueda.\n    */      \n    pasajesARecorrer:= pasajes(empresa)\n    while(not esVac\u00eda(pasajesARecorrer) && nombreDePasajero =/ nombrePasajero(primero(pasajesARecorrer)){\n        pasajesARecorrer := resto(pasajesARecorrer)\n    }\n    return(not esVac\u00eda(pasajesARecorrer))\n}",
        "destinoDelPasaje_En_": "function destinoDelPasaje_En_(pasaje, empresa){\n    /*\n        PROPOSITO: describe el destino del pasaje dado en la empresa dada.\n        PARAMETROS: \n            - pasaje: PasajeVendido\n            - empresa: EmpresaDeBuses\n        PRECONDICIONES:\n            - El pasaje corresponde a la empresa dada.\n        TIPO: String\n        OBSERVACIONES: recorrido de b\u00fasqueda.\n    */\n    rutasARecorrer := rutas(empresa)\n    while(rutaARealizar(pasaje) /= rutaId(primero(rutasARecorrer))){\n        rutasARecorrer:= resto(rutasARecorrer)\n    }\n    return(destino(primero(rutasARecorrer)))\n    \n}\n\n\n\"cajon de ginebra grande\" \"cajon de ginebra chico\"",
        "empresaConRutasExtendidasDesde_Hasta_En_": "function empresaConRutasExtendidasDesde_Hasta_En_(destinoAExtender, nuevoDestino, empresa){\n    /*\n        PROPOSITO: describe la empresa donde todas las rutas que ten\u00edan por destino \n            'destinoAExtender' cambidos a nuevoDestino. \n        PARAMETROS: \n            - destinoAExtender: String\n            - nuevoDestino: String\n            - empresa: EmpresaDeBuses\n        PRECONDICIONES:\n            - El nuevoDestino no debe ser un string vac\u00edo\n        TIPO: EmpresaDeBuses\n    */    \n    \n    return(\n        Empresa( empresa |\n                rutas <- rutas_EstendidasDesde_Hasta_(rutas(empresa),destinoAExtender, nuevoDestino)\n            )\n        )\n}",
        "rutas_EstendidasDesde_Hasta_": "function rutas_EstendidasDesde_Hasta_(rutas, destinoAExtender, nuevoDestino){\n    /*\n        PROPOSITO: describe las rutas extendidas si corresponde con el 'destinoAExtender'\n            hasta su 'nuevoDestino'\n        PARAMETROS: \n            - rutas: [Ruta]\n            - destinoAExtender: String\n            - nuevoDestino: String\n        PRECONDICIONES:\n            - El nuevoDestino no debe ser un string vac\u00edo\n        TIPO: [Ruta]\n        OBSERVACIONES: Recorrido de transformaci\u00f3n\n    */\n    rutasActualizadas := []\n    foreach ruta in rutas{\n        rutasActualizadas := rutasActualizadas ++ ruta_ActualidaCon_SiLLegaA_(ruta,nuevoDestino, destinoAExtender)\n    }\n    return(rutasActualizadas)\n\n}",
        "ruta_ActualidaCon_SiLLegaA_": "function ruta_ActualidaCon_SiLLegaA_(ruta, nuevoDestino, destinoACambiar){\n    choose  Ruta(ruta | destino <- nuevoDestino) when (destino(ruta) == destinoACambiar && origen(ruta) /= nuevoDestino)\n            ruta otherwise\n}"
    }
}


function get_library_elements(){
    return (biblioteca)
}


const libraryElementSelectedEvent = new Event("LibraryElementSelected");
document.addEventListener("LibraryElementSelected", () => {console.log("Library element selected")});


/* Initialize the library element selector.
 TODO: 
    1. Use the library element selected event for this shit.
    2. Refactor into proper OOP and not this garbage.
 */
const codigo = document.getElementById("codigo");
const element_type_tabs = document.getElementById("element-type-tabs");
for (tab of element_type_tabs.getElementsByClassName("tab"))
{
    tab.addEventListener("click", function() {active_library_selector = get_active_library_selector() } );
}
const active_library_selector = get_active_library_selector();
const library_selectors = document.getElementsByClassName("library-element-selector");
for (selector of library_selectors)
{
    for(item of selector.getElementsByClassName("collection-item"))
    {
        item.addEventListener("click", function (event) {
            let selected_element = get_selected_library_element(event.target.parentElement);
            document.dispatchEvent(libraryElementSelectedEvent);
            codigo.innerText = event.target.innerText;
            if (selected_element !== null) selected_element.classList.remove("active");
            event.target.classList.add("active");
            selected_element = event.target;
        });
    }
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


// Initialize materialize framework elements.
M.AutoInit();