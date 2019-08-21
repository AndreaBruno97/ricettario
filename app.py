"""
File principale, gestisce le ridirezioni delle pagine
"""

from flask import Flask, render_template, redirect, url_for, request, jsonify
import util
import db_inter
from flask_cors import CORS

app = Flask(__name__)
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

@app.route("/")
def root():
    return render_template("root.html")

@app.route("/elenco/<flag>")
def elenco(flag):
    lista = db_inter.all_ricette()
    num = len(lista)
    return render_template("elenco.html", flag=int(flag), lista=lista, num=num)

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

    return render_template("ricetta.html", nome=nome, tag_primario=tag_primario, tag_secondari=tag_secondari, num_tag_secondari=len(tag_secondari), testo=testo, id=id, ingredienti=ingredienti, num_ingredienti=len(ingredienti))

@app.route("/nuova_ricetta/<flag>")
def nuova_ricetta(flag):
    tag_secondari=db_inter.all_tag_sec()
    id_tag=[]
    tag=[]
    for coppia_tag in tag_secondari:
        id_tag.append(coppia_tag[0])
        tag.append(coppia_tag[1])
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

    if (len(nome) != 0 and db_inter.elimina_ricetta(id) != -1):
        util.elimina(id)
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

    tag_secondari=db_inter.all_tag_sec()
    id_tag=[]
    tag=[]
    for coppia_tag in tag_secondari:
        id_tag.append(coppia_tag[0])
        tag.append(coppia_tag[1])

    tag_sec_scelti_array=eval(db_inter.id_ricetta_to_tag_secondari(id))
    # Adattamento formato array per invio a javascript
    tag_sec_scelti=str(tag_sec_scelti_array)[1:-1].replace(" ", "")

    return render_template("modifica_ricetta.html", id=id, flag=flag, nome=nome, tag_primario=tag_primario, testo=testo, ingredienti=ingredienti, num_ingr=len(ingredienti), id_tag=id_tag, tag=tag, num_tag=len(tag), tag_sec_scelti=tag_sec_scelti)

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
            db_inter.elimina_ricetta(id_num)
            util.elimina(id_num)
            id_num = db_inter.nome_to_id(nome)
            flag = 1
        else:
            # ricetta già esistente con il nuovo titolo
            flag = -2
    else:
        flag = 1

    if flag == 1:
        util.scrivi(id_num, ingredienti, testo)
        db_inter.cambia_tag_primario(id_num, tag_primario)
        db_inter.cambia_tag_secondari(id_num, str(tag_secondari))
        flag = 1

    tag_secondari = db_inter.all_tag_sec()
    id_tag = []
    tag = []
    for coppia_tag in tag_secondari:
        id_tag.append(coppia_tag[0])
        tag.append(coppia_tag[1])

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
    """

    db_inter.new_tag_sec(tag)
    return jsonify(db_inter.tag_sec_to_id(tag))

# REST API per eliminare un tag secondario
@app.route("/elimina_tag/<id>", methods=["GET"])
def elimina_tag(id):
    """
    Riceve l'id di un tag secondario,
    lo elimina dal database e restituisce
    -1 in caso di errore
    """

    return jsonify(db_inter.elimina_tag_sec(id))

if __name__ == '__main__':
    app.run()
