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


function nextStep(step) {
    const currentStepDiv = document.querySelector(`#step${step - 1}`);
    
    // Validation des champs requis avant de continuer
    const inputs = currentStepDiv.querySelectorAll("[required]");
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.checkValidity()) {
            input.reportValidity(); // Affiche l'erreur native du navigateur
            input.classList.add("is-invalid");
            isValid = false;
        } else {
            input.classList.remove("is-invalid");
        }
    });

    if (isValid) {
        // Masquage et affichage avec animation
        document.querySelectorAll('[id^="step"]').forEach(div => {
            div.classList.add('hidden');
            div.classList.remove('fade-in');
        });
        
        const nextDiv = document.getElementById(`step${step}`);
        nextDiv.classList.remove('hidden');
        nextDiv.classList.add('fade-in');

        // Mise à jour de la barre de progression
        updateProgress(step);
    }
}

function prevStep(step) {
    document.querySelectorAll('[id^="step"]').forEach(div => div.classList.add('hidden'));
    const prevDiv = document.getElementById(`step${step}`);
    prevDiv.classList.remove('hidden');
    prevDiv.classList.add('fade-in');

    updateProgress(step, true);
}

function updateProgress(step, goingBack = false) {
    if (!goingBack) {
        // En avançant
        document.getElementById(`s${step}`).classList.add('active');
        document.getElementById(`l${step - 1}`).classList.add('active');
        document.getElementById(`s${step - 1}`).classList.replace('active', 'completed');
        document.getElementById(`s${step - 1}`).innerHTML = '✓'; // Petit effet "terminé"
    } else {
        // En reculant
        document.getElementById(`s${step + 1}`).classList.remove('active');
        document.getElementById(`l${step}`).classList.remove('active');
        document.getElementById(`s${step}`).classList.replace('completed', 'active');
        document.getElementById(`s${step}`).innerHTML = step;
    }
}

//

document.addEventListener('DOMContentLoaded', function() {
    
    /**
     * Fonction universelle pour traiter les formulaires AJAX
     * @param {string} formSelector - Le sélecteur du/des formulaire(s)
     * @param {string} messageSelector - Le sélecteur de la div de réponse (optionnel si interne au form)
     */
    const setupAjaxForm = (formSelector, messageSelector) => {
        const forms = document.querySelectorAll(formSelector);

        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                e.preventDefault();

                // 1. Récupération dynamique des éléments
                // On cherche le message-container spécifié ou un par défaut dans le formulaire
                const responseDiv = messageSelector ? document.querySelector(messageSelector) : form.querySelector('.ajax-response');
                const submitBtn = form.querySelector('[type="submit"]');
                const formData = new FormData(this);
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

                // 2. UI : Etat de chargement
                if (submitBtn) submitBtn.disabled = true;
                if (responseDiv) responseDiv.innerHTML = '<span class="text-muted small">Traitement en cours...</span>';

                // 3. Envoi
                fetch(this.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrftoken
                    }
                })
                .then(response => {
                    if (!response.ok && response.status !== 400) throw new Error('Network error');
                    return response.json();
                })
                .then(data => {
                    const isSuccess = data.status === 'success';
                    const icon = isSuccess ? 'fa-check-circle' : 'fa-exclamation-circle';
                    const textClass = isSuccess ? 'text-success' : 'text-danger';

                    if (responseDiv) {
                        responseDiv.innerHTML = `<span class="${textClass} small fw-bold"><i class="fas ${icon} me-1"></i> ${data.message}</span>`;
                    }

                    if (isSuccess) form.reset();
                })
                .catch(error => {
                    console.error('AJAX Error:', error);
                    if (responseDiv) responseDiv.innerHTML = `<span class="text-danger small fw-bold">Une erreur technique est survenue.</span>`;
                })
                .finally(() => {
                    if (submitBtn) submitBtn.disabled = false;
                });
            });
        });
    };

    // --- INITIALISATION ---
    // Vous pouvez maintenant gérer tous vos formulaires ici :
    setupAjaxForm('#newsletter-form', '#newsletter-message');
    setupAjaxForm('#ajax-devis-form', '#response-message');
});
///
document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.btn-faq-filter');
    const faqItems = document.querySelectorAll('.faq-item');

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // 1. Gestion de l'état actif des boutons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            const filterValue = this.getAttribute('data-filter');

            // 2. Logique de filtrage
            faqItems.forEach(item => {
                if (filterValue === 'all' || item.getAttribute('data-category') === filterValue) {
                    item.style.display = 'block';
                    // Animation optionnelle
                    item.style.opacity = '0';
                    setTimeout(() => { item.style.opacity = '1'; item.style.transition = '0.4s'; }, 10);
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
});