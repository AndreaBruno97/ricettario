/* Genera la condizione iniziale per lavorare:
 * Nel caso di nuova ricetta, id=0, quindi l'array elenco è vuoto
 * Nel caso di modifica, l'id è pari al numero di ingredienti di partenza
 * e viene generato un array di interi [0, ... , id-1]
 */

var id=$("#count").val();
var elenco=[];
var i=0;
while (i<id){
    elenco[i]=i;
    i++;
}
$("#elenco_ingr").val(Object.values(elenco));

$("#ingr_btn").click(function(){
	$("#ingredienti").append("<div class='ingr' id='" + id + "'><input type='text' name = 'id_" + id + "'>" +
        "<button class='ingr' id='" +id + "' type='button'>Cancella</button></div>");
	elenco[id]=id;
	id++;
	$("#elenco_ingr").val(Object.values(elenco));
});

$(document).on("click", "button.ingr",  function(){
    var old_id=this.id;
	$("div.ingr#"+old_id).remove();
	delete elenco[old_id];
	$("#elenco_ingr").val(Object.values(elenco));
});