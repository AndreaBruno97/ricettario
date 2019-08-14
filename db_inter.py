"""
Funzioni che permettono l'interazione col database
"""

import pymysql

def connetti():
    return pymysql.connect(user='root', password='root',
                           host='localhost', database='')

def esegui_query_0(query):
    # Esegue una query fornita come parametro
    conn = connetti()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return result

def esegui_query_1(query, param):
    # Esegue una query fornita come parametro (un elemento da inserire)
    conn = connetti()
    cursor = conn.cursor()
    cursor.execute(query, (param,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return result

def esegui_query_1_commit(query, param):
    # Esegue una query fornita come parametro (due elementi da inserire), compreso commit
    conn = connetti()
    cursor = conn.cursor()
    cursor.execute(query, (param, ))
    conn.commit()
    cursor.close()
    conn.close()

def esegui_query_2_commit(query, param1, param2):
    # Esegue una query fornita come parametro (due elementi da inserire), compreso commit
    conn = connetti()
    cursor = conn.cursor()
    cursor.execute(query, (param1, param2, ))
    conn.commit()
    cursor.close()
    conn.close()

def controllo_risultato_mono(result):
    # Esegue il controllo del risultato:
    # ritorna -1 se non è tornato nulla
    # ritorna un unico elemento in caso di successo
    if len(result) == 0:
        return -1
    else:
        return result[0][0]

def controllo_risultato_pluri(result):
    # Esegue il controllo del risultato:
    # ritorna -1 se non è tornato nulla
    # ritorna tutti gli elementi in caso di successo
    if len(result) == 0:
        return -1
    else:
        return result



def all_ricette():
    # Ritorna id e nome di tutte le ricette nel database
    return esegui_query_0("select id, nome from ricettario.ricettario")

def new_ricetta(nome, tag_primario):
    # Inserisce nel database una nuova ricetta, se possibile

    # Controllo se la ricetta esiste già
    id=nome_to_id(nome)

    if(id<0):
        esegui_query_2_commit("insert into ricettario.ricettario(nome, tag_primario) values (%s, %s)", nome, tag_primario)
    else:
        return -1

def elimina_ricetta(id):
    # Elimina dal database una nuova ricetta

    # Controllo se la ricetta esiste
    result=id_to_nome(id)

    if len(result)!= 0:
        esegui_query_1_commit("delete from ricettario.ricettario where id=%s", id)
    else:
        return -1

def id_to_nome(id):
    # Ritorna il nome della ricetta dato l'id
    result = esegui_query_1("select nome from ricettario.ricettario where id=%s", id)

    return controllo_risultato_mono(result)

def nome_to_id(nome):
    #Ritorna l'id di una ricetta dato il nome
    result = esegui_query_1("select id from ricettario.ricettario where binary nome=%s", nome)

    return controllo_risultato_mono(result)

def nome_to_tag_primario(nome):
    # Ritorna il tag primario dato il nome della ricetta
    result = esegui_query_1("select tag_primario from ricettario.ricettario where binary nome=%s", nome)

    return controllo_risultato_mono(result)

def id_to_tag_primario(id):
    # Ritorna il tag primario dato l'id della ricetta
    result = esegui_query_1("select tag_primario from ricettario.ricettario where id=%s", id)

    return controllo_risultato_mono(result)

def tag_primario_to_nome(tag):
    # Ritorna tutti i nomi di ricette con il dato tag primario
    result = esegui_query_1("select nome from ricettario.ricettario where tag_primario=%s", tag)

    return controllo_risultato_pluri(result)

def tag_primario_to_id(tag):
    # Ritorna tutti gli id di ricette con il dato tag primario
    result = esegui_query_1("select id from ricettario.ricettario where tag_primario=%s", tag)

    return controllo_risultato_pluri(result)

def cambia_tag_primario(id, tag):
    # Modifica il tag primario di una ricetta dato il suo id
    esegui_query_2_commit("update ricettario.ricettario set tag_primario=%s where id=%s", tag, id)