"""
File principale, gestisce le ridirezioni delle pagine
"""

from flask import Flask, render_template, redirect, url_for, request, session
import util
import db_inter
import os

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

@app.route("/elenco/<nome>")
def ricetta(nome):
    link=util.nome_to_link(nome)
    f = open(link, "r")
    contenuto=f.read()
    f.close()
    return render_template("ricetta.html", nome=nome, contenuto=contenuto)

@app.route("/nuova_ricetta/<flag>")
def nuova_ricetta(flag):
    return render_template("nuova_ricetta.html", flag=int(flag))

@app.route("/elimina_ricetta/<id>")
def elimina_ricetta(id):
    nome=db_inter.id_to_nome(id)
    if (len(nome)!=0 and db_inter.elimina_ricetta(id)!=-1):
        link=util.nome_to_link(nome)
        os.remove(link)
        flag=0
    else:
        flag=1
    return render_template("elimina_ricetta.html", flag=int(flag))

@app.route("/nuova_ricetta/insert", methods=["POST"])
def nuova_ricetta_insert():
    nome = request.form["nome"]
    testo = request.form["testo"]
    """
    flag:
         0 -> inserimento
         1 -> successo
        -1 -> falliemnto: no testo
        -2 -> fallimento: ricetta esistente
    """
    if len(testo)==0:
        flag=-1
    elif (db_inter.new_ricetta(nome)!=-1):
        link=util.nome_to_link(nome)
        f=open(link, "w+")
        f.write(testo)
        f.close()
        flag=1
    else:
        flag=-2
    return redirect(url_for("nuova_ricetta", flag=flag))



if __name__ == '__main__':
    app.run()
