document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('myInput');
    const options = document.getElementById('options-search');

    // Muestra las opciones al hacer clic en el input
    // input.addEventListener('focus', function() {
    //     options.style.display = 'block';
    // });
    if (input && options) {
        input.addEventListener('focus', function() {
            options.style.display = 'block';
        });
        // Oculta las opciones al hacer clic fuera
        document.addEventListener('click', function(event) {
            if (!input.contains(event.target) && !options.contains(event.target)) {
                options.style.display = 'none';
            }
        });

        // Filtra las opciones según el input
        input.addEventListener('input', function() {
            const filter = input.value.toLowerCase();
            const items = options.getElementsByClassName('dropdown-item');

            for (let i = 0; i < items.length; i++) {
                const text = items[i].textContent.toLowerCase();
                items[i].style.display = text.includes(filter) ? 'block' : 'none';
            }
        });

        // Al hacer clic en una opción, llena el input y oculta el dropdown
        options.addEventListener('click', function(event) {
            if (event.target.classList.contains('dropdown-item')) {
                input.value = event.target.getAttribute('data-value');
                options.style.display = 'none';
            }
        });
    }
});


/////////////// Manejo de búsqueda ///////////////
function searchClean(title){
    // Limpia el valor del input
    document.getElementById('myInput').value = '';
    const baseUrl = window.location.origin + window.location.pathname; // URL base
    // Devuelta a la página de la que se viene
    if( title === 'Especies Excluidas' || title === 'Glosario' || title === 'Literatura'){
        if (title === 'Especies Excluidas') {
            title = 'EspeciesExcluidas';
        }
        window.location.href = `${baseUrl}?item=Recursos&recurso=${encodeURIComponent(title)}`;
    }
    else if( title === 'Colectores' || title === 'Códigos' || title === 'Divisiones' || title === 'Géneros'){
        window.location.href = `${baseUrl}?item=Manejo&recurso=${encodeURIComponent(title)}`;
    }
    else{
        window.location.href = `${baseUrl}?item=${encodeURIComponent(title)}`;
    }
}

//////////////////////////
function searchIt(title) {
    const word = document.getElementById('myInput').value;
    const baseUrl = window.location.origin + window.location.pathname; // URL base
    if (word != ''){
        if( title === 'Especies Excluidas' || title === 'Glosario' || title === 'Literatura'){
            if (title === 'Especies Excluidas') {
                title = 'EspeciesExcluidas';
            }
            window.location.href = `${baseUrl}?item=Recursos&recurso=${encodeURIComponent(title)}&searched=${encodeURIComponent(word)}`;
        }
        else if( title === 'Colectores' || title === 'Códigos' || title === 'Divisiones' || title === 'Géneros'){
            window.location.href = `${baseUrl}?item=Manejo&recurso=${encodeURIComponent(title)}&searched=${encodeURIComponent(word)}`;
        }
        else{
            window.location.href = `${baseUrl}?item=${encodeURIComponent(title)}&searched=${encodeURIComponent(word)}`;
        }
    }

    else{
        if( title === 'Especies Excluidas' || title === 'Glosario' || title === 'Literatura'){
            if (title === 'Especies Excluidas') {
                title = 'EspeciesExcluidas';
            }
            window.location.href = `${baseUrl}?item=Recursos&recurso=${encodeURIComponent(title)}`;
        }
        else if( title === 'Colectores' || title === 'Códigos' || title === 'Divisiones' || title == 'Géneros'){
            window.location.href = `${baseUrl}?item=Manejo&recurso=${encodeURIComponent(title)}`;
        }
        else{
            window.location.href = `${baseUrl}?item=${encodeURIComponent(title)}`;
        }
    }
}
/////////////// Manejo de búsqueda ///////////////



/////////////// Búsqueda en el searchbar ///////////////
$(document).ready(function() {
    // console.log("jQuery listo");
    $("#myInput").on("keyup", function() {
        //console.log("Filtrando...");
        var value = $(this).val().toLowerCase();
        var found = false; // Variable para verificar si se encontraron resultados

        $("#myTable tr").filter(function() {
            // Filtrar solo por el texto de la columna "Familia"
            var familyText = $(this).find('td').eq(1).text().toLowerCase();
            var isMatch = familyText.indexOf(value) > -1;
            $(this).toggle(isMatch);
            if (isMatch) {
                found = true; // Si hay un resultado, marcar como encontrado
            }
        });

        // Mostrar u ocultar el mensaje de no resultados
        if (found) {
            $("#noResults").hide();
            $("#no-Results").hide();
        } else {
            $("#noResults").show();
            $("#no-Results").show();
        }
    });
});
/////////////// Búsqueda en el searchbar ///////////////