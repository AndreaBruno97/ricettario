"""
Funzioni di utilità
"""
from pathlib import Path
import os

#Qui va il nome della cartella che contiene le ricette
ricette="ricette\\"
#Qui va l'estensione del file da creare per le ricette
ext=".txt"

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
    testo=f.read()
    f.close()
    return testo

def scrivi(nome, testo):
    link=nome_to_link(nome)
    f=open(link, "w+")
    for riga in testo.split("\n"):
        # rstrip("\n") elimina il newline finale, visto che la write lo mette di suo
        f.write(riga.rstrip("/n"))
    f.close()

def elimina(nome):
    link = nome_to_link(nome)
    os.remove(link)