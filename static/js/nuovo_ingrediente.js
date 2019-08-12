var id=0;
var elenco={};

$("#ingr_btn").click(function(){
	$("#ingredienti").append("<div class='ingr' id='" + id + "'><input type='text' name = 'id_" + id + "'>" +
        "<button class='ingr' id='" +id + "' type='button'>Cancella</button></div>");
	elenco[id]=id;
	id++;
	$("#count").val(Object.values(elenco));
});

$(document).on("click", "button.ingr",  function(){
    var old_id=this.id;
	$("div.ingr#"+old_id).remove();
	delete elenco[old_id];
	$("#count").val(Object.values(elenco));
});