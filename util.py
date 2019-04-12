"""
Funzioni di utilità
"""
from pathlib import Path

#Qui va il nome della cartella che contiene le ricette
ricette="ricette\\"
#Qui va l'estensione del file da creare per le ricette
ext=".txt"

def nome_to_link(nome):
    nome=nome_to_underscore(nome) + ext
    return ricette + nome

def nome_to_underscore(nome):
    for c in [" ", "'", ",", "."]:
        nome=nome.replace(c, "_")
    return nome