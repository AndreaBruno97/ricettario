"""
Funzioni di utilità
"""
import os
import db_inter

#Nome della cartella che contiene le ricette
ricette="ricette/"
#Nome della cartella che contiene le immagini delle ricette
immagini="/static/immagini"
#Nome dell'immagine di default
img_default=immagini+"/default.jpg"
# Eestensione del file da creare per le ricette
ext=".txt"
# Separatore nel testo interno tra ingredienti e testo
separatore="#############"

def id_to_link(id_num):
    nome = "ricetta_" + str(id_num) + ext
    return ricette + nome

def id_to_immagine(id_num, estensione):
    # id_to_img ritorna l'estensione dell'immagine da usare,
    # o 0 se l'immagine non c'è

    if estensione != "0":
        nome = "immagine_" + str(id_num) + "." + estensione
        return immagini + "/" + nome
    else:
        return  img_default

def leggi(id_num):
    link=id_to_link(id_num)
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

def scrivi(id_num, ingredienti, testo):
    link = id_to_link(id_num)
    f = open(link, "w+")

    for elem in ingredienti:
        f.write(elem+"\n")

    f.write(separatore+"\n")

    for riga in testo.split("\n"):
        # rstrip("\n") elimina il newline finale, visto che la write lo mette di suo
        f.write(riga.rstrip("/n"))
    f.close()

def elimina(id_num, estensione):
    elimina_testo(id_num)
    elimina_img(id_num, estensione)

def elimina_testo(id_num):
    link = id_to_link(id_num)
    os.remove(link)

def elimina_img(id_num, estensione):
    immagine = id_to_immagine(id_num, estensione)[1:]
    os.remove(immagine)

def tuple_to_array(tupla):
    """
    Trasforma una tupla di coppie in un array di due elementi,
    a loro volta array
    """
    a = []
    b = []
    for coppia in tupla:
        a.append(coppia[0])
        b.append(coppia[1])

    return [a, b]

def match_ingredienti(nome):
    """
    Riceve parte degli ingredienti delle ricette,
    restituisce  gli id e i nomi di tutte le ricette che fanno match.

    Rendo minuscoli tutti gli ingredienti e la stringa da matchare
    per ottenere una ricerca case insensitive.
    """
    nome_lower=nome.lower()
    tutte_ricette=db_inter.all_ricette()
    list_id=[]
    list_nomi=[]
    for ric in tutte_ricette:
        id_ric=ric[0]
        nome_ric=ric[1]
        ingredienti=leggi(id_ric)[1]
        # flag:
        # 0 -> ingrediente non presente
        # 1 -> ingrediente presente

        flag=0
        for ing in ingredienti:
            if nome_lower in ing.lower():
                flag =1

        if flag==1:
            list_id.append(id_ric)
            list_nomi.append(nome_ric)
    return [list_id,list_nomi]

def cambia_nome_img(old_id, new_id, old_estensione):
    old_link=id_to_immagine(old_id, old_estensione)
    new_link=id_to_immagine(new_id, old_estensione)
    os.replace(old_link,new_link)