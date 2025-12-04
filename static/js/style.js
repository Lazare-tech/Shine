// faq page party 
document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('#faq-filters .btn-faq-filter');
    const faqItems = document.querySelectorAll('.faq-item');

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // 1. Gérer la classe active sur les boutons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            // 2. Récupérer le filtre sélectionné
            const filterValue = this.getAttribute('data-filter');

            // 3. Filtrer les éléments FAQ
            faqItems.forEach(item => {
                const itemCategory = item.getAttribute('data-category');
                
                if (filterValue === 'all' || itemCategory === filterValue) {
                    item.style.display = 'block'; // Afficher
                } else {
                    item.style.display = 'none'; // Masquer
                }
            });
        });
    });
});