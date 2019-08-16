"""
File principale, gestisce le ridirezioni delle pagine
"""

from flask import Flask, render_template, redirect, url_for, request
import util
import db_inter

app = Flask(__name__)

"""
Legenda Tag Primari:
    Antipasti
    Primi
    Secondi
    Piatti unici
    Contorni
    Dolci
"""

@app.route("/")
def root():
    return render_template("root.html")

@app.route("/elenco")
def elenco():
    lista = db_inter.all_ricette()
    num = len(lista)
    return render_template("elenco.html", lista=lista, num=num)

@app.route("/elenco/<id>")
def ricetta(id):
    nome = db_inter.id_to_nome(id)
    tag_primario = db_inter.id_to_tag_primario(id)
    leggi_tmp = util.leggi(id)
    testo = leggi_tmp[0]
    ingredienti = leggi_tmp[1]
    return render_template("ricetta.html", nome=nome, tag_primario=tag_primario, testo=testo, id=id, ingredienti=ingredienti, num=len(ingredienti))

@app.route("/nuova_ricetta/<flag>")
def nuova_ricetta(flag):
    return render_template("nuova_ricetta.html", flag=int(flag))

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
    elif db_inter.new_ricetta(nome, tag_primario) != -1:
        new_id = db_inter.nome_to_id(nome)
        util.scrivi(new_id, ingredienti, testo)
        flag = 1
    else:
        flag = -2
    return redirect(url_for("nuova_ricetta", flag=flag))

@app.route("/elimina_ricetta/<id>")
def elimina_ricetta(id):
    nome = db_inter.id_to_nome(id)
    if (len(nome) != 0 and db_inter.elimina_ricetta(id) != -1):
        util.elimina(id)
        flag=0
    else:
        flag=1
    return render_template("elimina_ricetta.html", flag=int(flag))

@app.route("/conferma_eliminazione/<id>")
def conferma_eliminazione(id):
    return render_template("conferma_eliminazione.html", id=id)

@app.route("/modifica_ricetta", methods=['GET'])
def modifica_ricetta():
    id = request.args.get('id')
    flag = request.args.get('flag')

    nome = db_inter.id_to_nome(id)
    tag_primario = db_inter.id_to_tag_primario(id)
    leggi_tmp = util.leggi(id)
    testo = leggi_tmp[0]
    ingredienti = leggi_tmp[1]
    return render_template("modifica_ricetta.html", id=id, flag=flag, nome=nome, tag_primario=tag_primario, testo=testo, ingredienti=ingredienti, num=len(ingredienti))

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
        if db_inter.new_ricetta(nome, tag_primario) != -1:
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
        flag = 1

    return render_template("modifica_ricetta.html", id_num=id_num, flag=flag, nome=nome, tag_primario=tag_primario, testo=testo, ingredienti=ingredienti, num=len(ingredienti))

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

if __name__ == '__main__':
    app.run()
