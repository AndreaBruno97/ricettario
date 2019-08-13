"""
Funzioni di utilità
"""
from pathlib import Path
import os

#Nome della cartella che contiene le ricette
ricette="ricette\\"
#Eestensione del file da creare per le ricette
ext=".txt"
#Separatore nel testo interno tra ingredienti e testo
separatore="#############"


def nome_to_underscore(nome):
    for c in [" ", "'", ",", "."]:
        nome=nome.replace(c, "_")
    return nome

def nome_to_link(nome):
    nome=nome_to_underscore(nome) + ext
    return ricette + nome

def leggi(nome):
    link=nome_to_link(nome)
    f=open(link, "r")
    testo_completo=f.read()
    f.close()

    # Rimozione \n per una corretta lettura del file
    lista=testo_completo.split(separatore)
    testo=lista[1][1:]
    ingredienti=lista[0][:-1].split("\n")

    # Ritorna un array con primo elemento la stringa col testo
    # e come secondo elemento un array di stringhe che
    # rappresentano gli ingredienti
    return [testo, ingredienti]

def scrivi(nome, ingredienti, testo):
    link=nome_to_link(nome)
    f=open(link, "w+")

    for elem in ingredienti:
        f.write(elem+"\n")

    f.write(separatore+"\n")

    for riga in testo.split("\n"):
        # rstrip("\n") elimina il newline finale, visto che la write lo mette di suo
        f.write(riga.rstrip("/n"))
    f.close()

def elimina(nome):
    link = nome_to_link(nome)
    os.remove(link)