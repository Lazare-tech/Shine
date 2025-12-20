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
function nextStep(step){
    ["step1","step2","step3","step4"].forEach(s=>document.getElementById(s).classList.add("hidden"));
    document.getElementById("step"+step).classList.remove("hidden");

    ["s1","s2","s3","s4"].forEach((id,i)=>{
        let el=document.getElementById(id), index=i+1;
        el.className="progress-step"+(index<step?" done":index==step?" active":"");
    });
    document.getElementById("l1").className="step-line"+(step>=2?" done":"");
    document.getElementById("l2").className="step-line"+(step>=3?" done":"");
    document.getElementById("l3").className="step-line"+(step>=4?" done":"");
}
function prevStep(step){ nextStep(step); }
//Message success formulaire
function showSuccessMessage(message) {
    Swal.fire({
        title: 'Félicitations !',
        text: message,
        icon: 'success',
        confirmButtonColor: '#004aad' // Ta couleur primaire
    });
}

//  <script>
//     {% if messages %}
//         {% for message in messages %}
//             Swal.fire({
//                 title: 'Félicitations !',
//                 text: "{{ message }}",
//                 icon: "{% if message.tags == 'success' %}success{% else %}info{% endif %}",
//                 confirmButtonColor: '#004aad' // Ta couleur primaire
//             });
//         {% endfor %}
//     {% endif %}
// </script>