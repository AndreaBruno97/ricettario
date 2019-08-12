"""
File principale, gestisce le ridirezioni delle pagine
"""

from flask import Flask, render_template, redirect, url_for, request, session
import util
import db_inter

app = Flask(__name__)


@app.route("/")
def root():
    nome=db_inter.id_to_nome(2)
    return render_template("root.html")

@app.route("/elenco")
def elenco():
    lista=db_inter.all_ricette()
    num=len(lista)
    return render_template("elenco.html", lista=lista, num=num)

@app.route("/elenco/<id>")
def ricetta(id):
    nome=db_inter.id_to_nome(id)
    testo=util.leggi(nome)
    return render_template("ricetta.html", nome=nome, testo=testo, id=id)

@app.route("/nuova_ricetta/<flag>")
def nuova_ricetta(flag):
    return render_template("nuova_ricetta.html", flag=int(flag))

@app.route("/conferma_eliminazione/<id>")
def conferma_eliminazione(id):
    return render_template("conferma_eliminazione.html", id=id)

@app.route("/elimina_ricetta/<id>")
def elimina_ricetta(id):
    nome=db_inter.id_to_nome(id)
    if (len(nome)!=0 and db_inter.elimina_ricetta(id)!=-1):
        util.elimina(nome)
        flag=0
    else:
        flag=1
    return render_template("elimina_ricetta.html", flag=int(flag))

@app.route("/nuova_ricetta/insert", methods=["POST"])
def nuova_ricetta_insert():
    """
    flag:
         0 -> inserimento
         1 -> successo
        -1 -> fallimento: no testo
        -2 -> fallimento: ricetta esistente
        -3 -> fallimento: no titolo
    """

    nome = request.form["nome"]
    testo = request.form["testo"]

    ingredienti=[]
    list_id=request.form["count"].split(',')
    for i in list_id:
        ingredienti.append(request.form["id_"+i])

    if len(testo)==0:
        flag= -1
    elif len(nome)==0:
        flag= -3
    elif (db_inter.new_ricetta(nome)!=-1):
        util.scrivi(nome, ingredienti, testo)
        flag=1
    else:
        flag= -2
    return redirect(url_for("nuova_ricetta", flag=flag))

@app.route("/modifica_ricetta/<id>")
def modifica_ricetta(id):
    nome=db_inter.id_to_nome(id)
    testo = util.leggi(nome)
    return render_template("modifica_ricetta.html", id=id, nome=nome, testo=testo)

@app.route("/modifica_ricetta/risultato", methods=["POST"])
def modifica_ricetta_risultato():
    """
    flag:
         0 -> modifica
         1 -> successo
        -1 -> fallimento: no testo
        -2 -> fallimento: ricetta esistente
        -3 -> fallimento: no titolo
    """
    nome = request.form["nome"]
    id = request.form["id"]
    testo = request.form["testo"]

    ingredienti=[]
    list_id=request.form["count"].split(',')
    for i in list_id:
        ingredienti.append(request.form[i])

    old_nome=db_inter.id_to_nome(id)

    if len(testo)==0:
        #non c'è testo
        flag= -1
    elif len(nome)==0:
        #non c'è nome
        flag= -3
    elif(db_inter.new_ricetta(nome)!=-1):
        if (nome!=old_nome):
            #modificato anche il titolo
            db_inter.elimina_ricetta(id)
            util.elimina(old_nome)
        util.scrivi(nome, ingredienti, testo)
        flag=1
    else:
        #ricetta già esistente con il nuovo titolo
        flag= -2
    return render_template("modifica_ricetta_risultato.html", flag=flag)



if __name__ == '__main__':
    app.run()
