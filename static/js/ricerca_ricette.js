//Gestisce la ricerca di ricette, date le informazioni fornite dall'utente

//Inizializzazione: elenco degli id delle ricette
lista_ricette=document.getElementById("lista_ricette").value;
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
   var nome = document.getElementById("text_nome").value;
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
   var nome = document.getElementById("text_ingredienti").value;
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