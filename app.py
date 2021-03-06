"""
File principale, gestisce le ridirezioni delle pagine
"""

from flask import Flask, render_template, redirect, url_for, request, jsonify
import util
import db_inter
from flask_cors import CORS

app = Flask(__name__)
# Imposta la cartella di destinazione per le immagini inviate dall'utente
app.config['IMAGE_UPLOADS'] = "static/immagini"
CORS(app)

"""
Legenda Tag Primari:
    Antipasti
    Primi
    Secondi
    Piatti unici
    Contorni
    Dolci
"""

"""
Formato degli array generati automaticamente:
[1, 2, 3, 4, 5, 6, 7, 8, 9]
"""

"""
# Adattamento formato array per invio a javascript
    tag_sec_scelti=str(tag_sec_scelti_array)[1:-1].replace(" ", "")
    
    ((103, 'IIIIIIIIIIII'), (104, 'sertyuj'))
    (103,'IIIIIIIIIIII'),(104,'sertyuj')
"""

@app.route("/")
def root():
    return render_template("root.html")

@app.route("/elenco/<flag>")
def elenco(flag):
    lista = db_inter.all_ricette()
    num_ricette = len(lista)
    tag_primari=["Antipasti", "Primi", "Secondi", "Piatti unici", "Contorni", "Dolci"]
    tag_secondari=db_inter.all_tag_sec()

    lista_id=[]
    for ricetta in lista:
        lista_id.append(ricetta[0])
    lista_str=str(lista_id)[1:-1].replace(" ", "")

    return render_template("elenco.html", flag=int(flag), lista=lista, lista_str=lista_str, num_ricette=num_ricette, tag_primari=tag_primari, tag_secondari=tag_secondari)

@app.route("/elenco/ricetta/<id>")
def ricetta(id):
    nome = db_inter.id_to_nome(id)
    tag_primario = db_inter.id_to_tag_primario(id)

    leggi_tmp = util.leggi(id)
    testo = leggi_tmp[0]
    ingredienti = leggi_tmp[1]

    tag_secondari_str=db_inter.id_ricetta_to_tag_secondari(id)
    tag_secondari_id=eval(tag_secondari_str)
    tag_secondari=[]
    for tag_id in tag_secondari_id:
        tag_secondari.append(db_inter.id_to_tag_sec(tag_id))

    estensione = db_inter.id_to_img(id)
    src_immagine=util.id_to_immagine(id, estensione)

    return render_template("ricetta.html", nome=nome, tag_primario=tag_primario, tag_secondari=tag_secondari, num_tag_secondari=len(tag_secondari), testo=testo, id=id, ingredienti=ingredienti, num_ingredienti=len(ingredienti), src_immagine=src_immagine)

@app.route("/nuova_ricetta/<flag>")
def nuova_ricetta(flag):
    tag_secondari=util.tuple_to_array(db_inter.all_tag_sec())
    id_tag=tag_secondari[0]
    tag=tag_secondari[1]

    return render_template("nuova_ricetta.html", flag=int(flag), id_tag=id_tag, tag=tag, num=len(tag))

@app.route("/nuova_ricetta/insert", methods=["POST"])
def nuova_ricetta_insert():
    """
    flag:
         0 -> inserimento
         1 -> successo
        -1 -> fallimento: no testo
        -2 -> fallimento: ricetta esistente
        -3 -> fallimento: no titolo
        -4 -> fallimento: no ingredienti
    """

    nome = request.form["nome"]
    testo = request.form["testo"]
    tag_primario = request.form.get("tag_primario", None)
    immagine = request.files["immagine"]

    tag_secondari_db = db_inter.all_tag_sec()
    tag_secondari = []
    for coppia_tag in tag_secondari_db:
        i=coppia_tag[0]
        tag_sec_scelta= request.form.get("tag_"+str(i), None)
        if tag_sec_scelta != None:
            tag_secondari.append(i)

    ingredienti = []
    list_id = request.form["elenco_ingr"].split(',')
    if list_id[0] != '':
        for i in list_id:
            ingredienti.append(request.form["id_" + i])

    if len(testo) == 0:
        # non c'è testo
        flag = -1
    elif len(nome) == 0:
        # non c'è nome
        flag = -3
    elif list_id[0] == '':
        # non ci sono ingredienti
        flag = -4
    elif tag_primario == None:
        # non c'è tag primario
        flag = -5
    elif db_inter.new_ricetta(nome, tag_primario, str(tag_secondari)) != -1:
        new_id = db_inter.nome_to_id(nome)
        util.scrivi(new_id, ingredienti, testo)

        # Per l'immagine, di default inserisco 0 nel database, altrimenti
        # salvo l'immagine col nome desiderato e salvo nel database
        # l'estensione dell'immagine

        if immagine.filename != "":
            estensione = immagine.filename.split(".")[-1]
            immagine.filename="/immagine_" + str(new_id) + "." + estensione
            immagine.save(app.config["IMAGE_UPLOADS"] + immagine.filename)
            db_inter.cambia_img(new_id, estensione)

        flag = 1
    else:
        flag = -2
    return redirect(url_for("nuova_ricetta", flag=flag))

@app.route("/elimina_ricetta/<id>")
def elimina_ricetta(id):
    """
        flag =  0: Pagina standard
        flag =  1: Successo eliminazione
        flag = -1: Successo eliminazione
    """

    nome = db_inter.id_to_nome(id)
    estensione = db_inter.id_to_img(id)
    if (len(nome) != 0 and db_inter.elimina_ricetta(id) != -1):
        util.elimina(id, estensione)
        flag=1
    else:
        flag=-1
    return redirect(url_for("elenco", flag=int(flag)))

@app.route("/modifica_ricetta", methods=['GET'])
def modifica_ricetta():
    id = request.args.get('id')
    flag = request.args.get('flag')

    nome = db_inter.id_to_nome(id)
    tag_primario = db_inter.id_to_tag_primario(id)
    leggi_tmp = util.leggi(id)
    testo = leggi_tmp[0]
    ingredienti = leggi_tmp[1]

    tag_secondari=util.tuple_to_array(db_inter.all_tag_sec())
    id_tag=tag_secondari[0]
    tag=tag_secondari[1]

    tag_sec_scelti_array=eval(db_inter.id_ricetta_to_tag_secondari(id))
    # Adattamento formato array per invio a javascript
    tag_sec_scelti=str(tag_sec_scelti_array)[1:-1].replace(" ", "")

    estensione = db_inter.id_to_img(id)
    src_immagine=util.id_to_immagine(id, estensione)

    return render_template("modifica_ricetta.html", id=id, flag=flag, nome=nome, tag_primario=tag_primario, testo=testo, ingredienti=ingredienti, num_ingr=len(ingredienti), id_tag=id_tag, tag=tag, num_tag=len(tag), tag_sec_scelti=tag_sec_scelti, src_immagine=src_immagine)

@app.route("/modifica_ricetta/risultato", methods=["POST"])
def modifica_ricetta_risultato():
    """
    flag:
         0 -> modifica
         1 -> successo
        -1 -> fallimento: no testo
        -2 -> fallimento: ricetta esistente
        -3 -> fallimento: no titolo
        -4 -> fallimento: no ingredienti
        -5 -> fallimento: no tag primario
    """
    nome = request.form["nome"]
    id_num = request.form["id"]
    testo = request.form["testo"]
    tag_primario = request.form.get("tag_primario", None)
    immagine = request.files["new_immagine"]
    flag_immagine = request.form.get("elimina_immagine", None)

    ingredienti = []
    list_id = request.form["elenco_ingr"].split(',')
    if list_id[0] != '':
        for i in list_id:
            ingredienti.append(request.form["id_"+i])

    tag_secondari_db = db_inter.all_tag_sec()
    tag_secondari = []
    for coppia_tag in tag_secondari_db:
        i = coppia_tag[0]
        tag_sec_scelta = request.form.get("tag_" + str(i), None)
        if tag_sec_scelta != None:
            tag_secondari.append(i)

    old_nome = db_inter.id_to_nome(id_num)
    old_id = id_num
    old_estensione=db_inter.id_to_img(id_num)

    if len(testo) == 0:
        # non c'è testo
        flag= -1
    elif len(nome) == 0:
        # non c'è nome
        flag= -3
    elif list_id[0] == '':
        # non ci sono ingredienti
        flag = -4
    elif tag_primario == None:
        # non c'è tag primario
        flag = -5
    elif nome != old_nome:
        # Nuova ricetta inserita con successo nel database
        if db_inter.new_ricetta(nome, tag_primario, str(tag_secondari)) != -1:
            # modificato anche il titolo
            util.elimina_testo(id_num)
            id_num = db_inter.nome_to_id(nome)

            if old_estensione!= "0":
                # Cambia il nome dell'immagine, visto che è cambiato l'id della ricetta
                util.cambia_nome_img(old_id, id_num, old_estensione)

            db_inter.elimina_ricetta(id_num)
            flag = 1
        else:
            # ricetta già esistente con il nuovo titolo
            flag = -2
    else:
        flag = 1

    if flag == 1:
        if immagine.filename != "":
            # L'utente ha cambiato l'immagine
            estensione = immagine.filename.split(".")[-1]
            immagine.filename = "/immagine_" + str(id_num) + "." + estensione
            immagine.save(app.config["IMAGE_UPLOADS"] + immagine.filename)

        elif flag_immagine != None :
            # L'utente ha eliminato l'immagine
            util.elimina_img(id_num, old_estensione)
            estensione="0"
        else:
            estensione=old_estensione

        util.scrivi(id_num, ingredienti, testo)
        db_inter.cambia_tag_primario(id_num, tag_primario)
        db_inter.cambia_tag_secondari(id_num, str(tag_secondari))
        db_inter.cambia_img(id_num, estensione)
        flag = 1

    tag_secondari=util.tuple_to_array(db_inter.all_tag_sec())
    id_tag=tag_secondari[0]
    tag=tag_secondari[1]

    tag_sec_scelti_array = eval(db_inter.id_ricetta_to_tag_secondari(id_num))
    # Adattamento formato array per invio a javascript
    tag_sec_scelti = str(tag_sec_scelti_array)[1:-1].replace(" ", "")

    return render_template("modifica_ricetta.html", id=id_num, flag=flag, nome=nome, tag_primario=tag_primario, testo=testo, ingredienti=ingredienti, num_ingr=len(ingredienti), id_tag=id_tag, tag=tag, num_tag=len(tag), tag_sec_scelti=tag_sec_scelti)

@app.route("/tag_secondari/<flag>")
def tag_secondari(flag):
    lista = db_inter.all_tag_sec()
    num = len(lista)
    return render_template("tag_secondari.html", lista=lista, num=num, flag=int(flag))

@app.route("/nuovo_tag_secondario/insert", methods=["POST"])
def nuovo_tag_secondario_insert():
    """
    flag:
         0 -> pagina standard
         1 -> successo inserimento
        -1 -> fallimento inserimento: no tag secondario
        -2 -> fallimento inserimento: tag secondario esistente
    """

    tag = request.form["tag"]

    if len(tag) == 0:
        # Non c'è tag secondario
        flag = -1
    elif db_inter.new_tag_sec(tag) != -1:
        # Operazione completata
        flag = 1
    else:
        # Tag secondario esistente
        flag = -2
    return redirect(url_for("tag_secondari", flag=flag))

@app.route("/elimina_tag_secondario/<id>")
def elimina_tag_secondario(id):
    """
    flag:
         0 -> pagina standard
         2 -> successo eliminazione
        -3 -> fallimento eliminazione: no tag secondario
    """
    tag = db_inter.id_to_tag_sec(id)
    if (len(tag) != 0 and db_inter.elimina_tag_sec(id) != -1):
        flag=2
    else:
        flag=-3
    return redirect(url_for("tag_secondari", flag=flag))

# REST API per ricevere nuovi tag secondari
@app.route("/nuovo_tag/<tag>", methods=["GET"])
def nuovo_tag(tag):
    """
    Riceve il nome del nuovo tag secondario,
    lo inserisce nel database e restituisce
    l'id del tag secondario

    -1 se il tag esiste già
    """

    if db_inter.new_tag_sec(tag)!= -1:
        return jsonify(db_inter.tag_sec_to_id(tag))
    else:
        return jsonify("-1")

# REST API per ricevere tutte le ricette che contengono la stringa inviata nel nome
@app.route("/ricette_match_nome/<nome>", methods=["GET"])
def ricerca_match_nome(nome):
    """
    Riceve parte del nome delle ricette,
    restituisce  gli id e i nomi di tutte le ricette che fanno match
    """
    list_ricette=util.tuple_to_array(db_inter.ricette_match_nome(nome))

    return jsonify(list_ricette)

# REST API per ricevere tutte le ricette
@app.route("/api_all_ricette", methods=["GET"])
def api_all_ricette():
    """
    Riceve parte del nome delle ricette,
    restituisce  gli id e i nomi di tutte le ricette che fanno match
    """
    list_ricette=util.tuple_to_array(db_inter.all_ricette())

    return jsonify(list_ricette)

# REST API per ricevere tutte le ricette che contengono la stringa inviata negli ingredienti
@app.route("/ricette_match_ingredienti/<nome>", methods=["GET"])
def ricette_match_ingredienti(nome):
    """
    Riceve parte degli ingredienti delle ricette,
    restituisce  gli id e i nomi di tutte le ricette che fanno match
    """
    lista=util.match_ingredienti(nome)

    return jsonify(lista)

# REST API per ricevere tutte le ricette che corrispondono a tutti i criteri di ricerca
@app.route("/ricette_match_completo", methods=["POST"])
def ricette_match_completo():
    """
    La REST API riceve parte del nome, parte degli ingredienti, un
    tag primario e un tag secondario, e ritorna l'elenco di id di ricette
    che matchano con  le richieste.
    """
    nome=request.form["nome"]
    ingr=request.form["ingr"]
    tag_prim=request.form["tag_prim"]
    tag_sec=request.form["tag_sec"]

    # Javascript manda "Piatti" invece di "Piatti unici"
    if tag_prim=="Piatti":
        tag_prim="Piatti unici"

    # Elenco completo di id ricette
    list_all_con_nomi=db_inter.all_ricette()
    set_all=set()
    for coppia in list_all_con_nomi:
        set_all.add(coppia[0])

    # Controllo nome
    set_ricette=set()
    if nome!="" :
        result=db_inter.ricette_match_nome(nome)
        if result!=-1:
            tmp=util.tuple_to_array(result)[0]
            set_ricette.update(tmp)
    else:
        set_ricette=set_all.copy()

    # Controllo ingredienti
    set_ingredienti=set()
    if ingr!="" :
        result=util.match_ingredienti(ingr)[0]
        set_ingredienti.update(result)
    else:
        set_ingredienti=set_all.copy()

    # Controllo tag primario
    set_tag_prim=set()
    if tag_prim!="":
        result=db_inter.tag_primario_to_id(tag_prim)
        if result !=-1:
            set_tag_prim.update(result)
    else:
        set_tag_prim=set_all.copy()

    # Controllo tag secondario
    set_tag_sec = set()
    if tag_sec != "":
        result=db_inter.tag_secondario_to_id_ricette(tag_sec)
        if result!=-1:
            set_tag_sec.update(result)
    else:
        set_tag_sec = set_all.copy()

    # Intersezione set: invio solo gli id che
    # risultano da tutti i filtri
    lista= list(set_ricette.intersection(set_ingredienti, set_tag_prim, set_tag_sec))
    return jsonify(lista)

if __name__ == '__main__':
    app.run()