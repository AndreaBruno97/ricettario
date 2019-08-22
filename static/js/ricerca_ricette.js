//Gestisce la ricerca di ricette, date le informazioni fornite dall'utente

function genera_elenco_ricette(lista) {
               $(".elenco_ricette").remove();
               lista_id=lista[0];
               lista_nomi=lista[1];
               for (i=0; i<lista_id.length; i++){
                   $("#elenco_ul").append("<li class=\"elenco_ricette\">\n" +
                       "<a href=\"{{ url_for(\"ricetta\", id="+lista_id[i]+") }}\">"+lista_nomi[i]+"</a>\n" +
                       "<a href=\"{{ url_for(\"modifica_ricetta\", id="+lista_id[i]+")}}\">Modifica</a>\n" +
                       "<a href=\"{{ url_for(\"elimina_ricetta\", id="+lista_id[i]+") }}\", class=\"conferma_elim_ricette\" id=\"id_"+lista_id[i]+"\">Elimina</a>\n" +
                       "</li>");
               }
            }

//Bottone per la ricerca delle ricette, data una parte del nome
$("#btn_nome").click(function () {
   var nome = document.getElementById("ricerca_nome").value;
   if(nome !==""){
       $.ajax({
           type: "GET",
            url: "http://localhost:5000/ricette_match_nome/"+ nome,

           error: function () {
                alert("Errore ricerca ricette");
            },

            success: function (lista) {
                genera_elenco_ricette(lista);
            }
       });
   }
});

//Bottone per reinserire tutte le ricette
$("#btn_reset").click(function () {
   $.ajax({
       type: "GET",
        url: "http://localhost:5000/api_all_ricette",

       error: function () {
            alert("Errore ricerca ricette");
        },

        success: function (lista) {
            genera_elenco_ricette(lista);
        }
   });
});