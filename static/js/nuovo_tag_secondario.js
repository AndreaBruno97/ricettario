$('#btn_tag_sec').click(function () {
   tag=$("#text_tag_sec").val();

   //Chiama la REST API per l'inserimento di un nuovo tag secondario
    $.ajax({
        type: "GET",
        url: "http://localhost:5000/nuovo_tag/"+ tag,

        error: function () {
            alert("Errore inserimento tag secondario");
        },

        success: function (id) {
            if (id>0){
                $('#div_tag_sec').append("<input type=\"checkbox\" id=\"tag_"+ id +"\" name=\"tag_" + id + "\" value=\"" + id + "\" /> " + tag + "");
                alert("Successo inserimento tag secondario");
            }
            else{
                alert("Tag secondario già esistente");
            }
        }
    });
});
