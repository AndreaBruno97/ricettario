var num=0;
var id=0;

$("#ingr_btn").click(function(){
	$("#ingredienti").append("<div class='ingr' id='" + id + "'><input type='text' name = '" + id + "'>" +
        "<button class='ingr' id='" +id + "' type='button'>Cancella</button></div>");
	num++;
	id++;
	$("#count").val(num);
});

$(document).on("click", "button.ingr",  function(){
    var a=this.id;
	$("div.ingr#"+a).remove();
	num--;
	$("#count").val(num);
});