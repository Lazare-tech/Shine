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

// step page form register 
// function nextStep(step){
//     ["step1","step2","step3","step4"].forEach(s=>document.getElementById(s).classList.add("hidden"));
//     document.getElementById("step"+step).classList.remove("hidden");

//     ["s1","s2","s3","s4"].forEach((id,i)=>{
//         let el=document.getElementById(id), index=i+1;
//         el.className="progress-step"+(index<step?" done":index==step?" active":"");
//     });
//     document.getElementById("l1").className="step-line"+(step>=2?" done":"");
//     document.getElementById("l2").className="step-line"+(step>=3?" done":"");
//     document.getElementById("l3").className="step-line"+(step>=4?" done":"");
// }
// function prevStep(step){ nextStep(step); }
// //Message success formulaire
// function showSuccessMessage(message) {
//     Swal.fire({
//         title: 'Félicitations !',
//         text: message,
//         icon: 'success',
//         confirmButtonColor: '#004aad' // Ta couleur primaire
//     });
// }
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
