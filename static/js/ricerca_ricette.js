//Gestisce la ricerca di ricette, date le informazioni fornite dall'utente

//Inizializzazione: elenco degli id delle ricette
lista_ricette=$("#lista_ricette").val();
var lista_id=[];
for(ricetta of lista_ricette.split(",")){
    lista_id.push(ricetta);
}

//Funzione che mostra solo le ricette nella lista passata come parametro
function mostra_ricette_lista(lista){
    for (id_ric of lista_id){
        if (lista.includes( parseInt(id_ric, 10))){
            $(".elenco_ricette#"+id_ric).show();
        }
        else{
            $(".elenco_ricette#"+id_ric).hide();
        }
    }
}

//Bottone per reinserire tutte le ricette
$("#btn_reset").click(function () {
   for (id_ric of lista_id){
       $(".elenco_ricette#"+id_ric).show();
   }
});

//Bottone per la ricerca delle ricette, data una parte del nome
$("#btn_nome").click(function () {
   var nome = $("#text_nome").val();
   if(nome !==""){
       $.ajax({
           type: "GET",
           url: "http://localhost:5000/ricette_match_nome/"+ nome,

           error: function () {
                alert("Errore ricerca ricette");
           },

           success: function (lista) {
                mostra_ricette_lista(lista[0]);
           }
       });
   }
});

//Bottone per la ricerca delle ricette, data una parte degli ingredienti
$("#btn_ingredienti").click(function () {
   var nome = $("#text_ingredienti").val();
   if(nome !==""){
       $.ajax({
           type: "GET",
           url: "http://localhost:5000/ricette_match_ingredienti/"+ nome,

           error: function () {
                alert("Errore ricerca ricette");
           },

           success: function (lista) {
                mostra_ricette_lista(lista[0]);
           }
       });
   }
});

//Bottone per la ricerca delle ricette, data la ricerca completa
$("#btn_completo").click(function () {
   var nome = $("#text_completo_nome").val();
   var ingr = $("#text_completo_ingr").val();
   var tag_prim = $("#text_completo_tag_prim :selected").val();
   var tag_sec = $("#text_completo_tag_sec :selected").val();

   $.ajax({
       type: "POST",
       url: "http://localhost:5000/ricette_match_completo",
       data: {
           "nome":nome,
           "ingr":ingr,
           "tag_prim":tag_prim,
           "tag_sec":tag_sec
       },

       error: function () {
            alert("Errore ricerca ricette");
        },

       success: function (lista) {
            mostra_ricette_lista(lista);
       }
   });
});