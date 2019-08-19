// Agisce su link/bottoni con id "conferma_elim"

flag = 0;

$(".conferma_elim").click(function(e){

	if(!confirm("Vuoi eliminare questa ricetta?")){
        e.preventDefault();
    }

});