// Agisce su link/bottoni con classe "conferma_elim_ricette" o "conferma_elim_tag"

$(".conferma_elim_ricette").click(function(e){

	if(!confirm("Vuoi eliminare questa ricetta?")){
        e.preventDefault();
    }

});

$(".conferma_elim_tag").click(function(e){

	if(!confirm("Vuoi eliminare questo tag secondario?")){
        e.preventDefault();
    }

});