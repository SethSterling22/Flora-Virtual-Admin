// Configuración inicial de los enlaces de navegación - Cargar las páginas sin redirección
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(event) {
        // if (this.id !== 'logout') {
        //     event.preventDefault(); 
        // }

        // Remover la clase 'active' de los enlaces
        document.querySelectorAll('.nav-link').forEach(nav => {
            nav.classList.remove('active');
        });
        

        // Añadir la clase 'active'
        this.classList.add('active');

        const url = this.getAttribute('data-url');
        const item = this.getAttribute('data-item');
    });
});

