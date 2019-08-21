$('#btn_tag_sec').click(function () {
   tag=document.getElementById("text_tag_sec").value;

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
                alert("Errore inserimento tag secondario");
            }
        }
    });
    /*
    $.get("http://localhost:5000/nuovo_tag/"+ tag,
        function (data, status, xhr) {
            //flag = 0 -> tag secondario non inserito
            //flag = 1 -> tag secondario inserito
            var flag = 0;
            if (status >= 200 && status < 400){
                var id = parseInt(data[0], 10);
                if (id>0){
                    $('#div_tag_sec').append("<input type=\"checkbox\" id=\"tag_"+ id +"\" name=\"tag_" + id + "\" value=\"" + id + "\" /> " + tag + "");
                    flag = 1;
                }
            }
            if (flag === 0){
                alert("Errore inserimento tag secondario");
            }
            else {
                alert("Successo inserimento tag secondario");
            }
        });
       */
});
