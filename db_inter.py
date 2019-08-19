"""
Funzioni che permettono l'interazione col database
"""

import pymysql

"""
Formato degli array generati automaticamente:
[1, 2, 3, 4, 5, 6, 7, 8, 9]
"""

def ricerca_tag_regex(tag):
    #"[num," oppure ", num," oppure ", num]"
    return "\[" + tag + ",%|%, " + tag + ",%|%, " + tag + "\]"

# Funzioni generali

def connetti():
    return pymysql.connect(user='root', password='root',
                           host='localhost', database='')

def esegui_query_ricerca(query, param):
    # Esegue una query fornita come parametro (tupla di stringhe da inserire)
    conn = connetti()
    cursor = conn.cursor()
    if param == None:
        cursor.execute(query)
    else:
        cursor.execute(query, param)
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return result

def esegui_query_modifica(query, param):
    # Esegue una modifica sul db fornita come parametro (tupla di stringhe da inserire)
    conn = connetti()
    cursor = conn.cursor()
    if param == None:
        cursor.execute(query)
    else:
        cursor.execute(query, param)
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


# Funzioni relative alla tabella "ricettario"

def all_ricette():
    # Ritorna id e nome di tutte le ricette nel database
    return esegui_query_ricerca("select id, nome from ricettario.ricettario", None)

def new_ricetta(nome, tag_primario, tag_secondari):
    # Inserisce nel database una nuova ricetta, se possibile

    # Controllo se la ricetta esiste già
    id=nome_to_id(nome)

    if(id<0):
        esegui_query_modifica("insert into ricettario.ricettario(nome, tag_primario, tag_secondari) values (%s, %s, %s)", (nome, tag_primario, tag_secondari))
    else:
        return -1

def elimina_ricetta(id):
    # Elimina dal database una ricetta

    # Controllo se la ricetta esiste
    result=id_to_nome(id)

    if len(result)!= 0:
        esegui_query_modifica("delete from ricettario.ricettario where id=%s", (id, ))
    else:
        return -1

def id_to_nome(id):
    # Ritorna il nome della ricetta dato l'id
    result = esegui_query_ricerca("select nome from ricettario.ricettario where id=%s", (id, ))

    return controllo_risultato_mono(result)

def nome_to_id(nome):
    #Ritorna l'id di una ricetta dato il nome
    result = esegui_query_ricerca("select id from ricettario.ricettario where binary nome=%s", (nome, ))

    return controllo_risultato_mono(result)

def nome_to_tag_primario(nome):
    # Ritorna il tag primario dato il nome della ricetta
    result = esegui_query_ricerca("select tag_primario from ricettario.ricettario where binary nome=%s", (nome, ))

    return controllo_risultato_mono(result)

def id_to_tag_primario(id):
    # Ritorna il tag primario dato l'id della ricetta
    result = esegui_query_ricerca("select tag_primario from ricettario.ricettario where id=%s", (id, ))

    return controllo_risultato_mono(result)

def tag_primario_to_nome(tag):
    # Ritorna tutti i nomi di ricette con il dato tag primario
    result = esegui_query_ricerca("select nome from ricettario.ricettario where tag_primario=%s", (tag, ))

    return controllo_risultato_pluri(result)

def tag_primario_to_id(tag):
    # Ritorna tutti gli id di ricette con il dato tag primario
    result = esegui_query_ricerca("select id from ricettario.ricettario where tag_primario=%s", (tag, ))

    return controllo_risultato_pluri(result)

def nome_to_tag_secondari(nome):
    # Ritorna un array con i tag secondari dato il nome della ricetta
    result = esegui_query_ricerca("select tag_secondari from ricettario.ricettario where binary nome=%s", (nome, ))

    return controllo_risultato_mono(result)

def id_ricetta_to_tag_secondari(id):
    # Ritorna un array con i tag secondari dato l'id della ricetta
    result = esegui_query_ricerca("select tag_secondari from ricettario.ricettario where id=%s", (id, ))

    return controllo_risultato_mono(result)

def tag_secondario_to_nome(tag):
    # Ritorna tutti i nomi di ricette con il dato tag secondario
    regex_tag = ricerca_tag_regex(tag)
    result = esegui_query_ricerca("select nome from ricettario.ricettario where tag_secondario regexp " + regex_tag, None)

    return controllo_risultato_pluri(result)

def tag_secondario_to_id(tag):
    # Ritorna tutti gli id di ricette con il dato tag secondario
    regex_tag = ricerca_tag_regex(tag)
    result = esegui_query_ricerca("select id from ricettario.ricettario where tag_secondario regexp " + regex_tag, None)

    return controllo_risultato_pluri(result)

def cambia_tag_primario(id, tag):
    # Modifica il tag primario di una ricetta dato il suo id
    esegui_query_modifica("update ricettario.ricettario set tag_primario=%s where id=%s", (tag, id))

def cambia_tag_secondari(id, tag):
    # Modifica i tag secondari di una ricetta dato il suo id
    esegui_query_modifica("update ricettario.ricettario set tag_secondari=%s where id=%s", (tag, id))


#Funzioni relative alla tabella "tag_sec"

def all_tag_sec():
    # Ritorna id e nome di tutti i tag secondari nel database
    return esegui_query_ricerca("select id, tag from ricettario.tag_sec", None)

def new_tag_sec(tag):
    # Inserisce nel database un nuovo tag secondario, se possibile

    # Controllo se lil tag secondario esiste già
    id=tag_sec_to_id(tag)

    if(id<0):
        esegui_query_modifica("insert into ricettario.tag_sec(tag) values (%s)", (tag, ))
    else:
        return -1

def elimina_tag_sec(id):
    # Elimina dal database un tag secondario

    # Controllo se la ricetta esiste
    result=id_to_tag_sec(id)

    if len(result)!= 0:
        esegui_query_modifica("delete from ricettario.tag_sec where id=%s", (id, ))
    else:
        return -1

def id_to_tag_sec(id):
    # Ritorna il tag secondario dato l'id
    result = esegui_query_ricerca("select tag from ricettario.tag_sec where id=%s", (id,))

    return controllo_risultato_mono(result)

def tag_sec_to_id(tag):
    # Ritorna l'id di una ricetta dato il tag secondario
    result = esegui_query_ricerca("select id from ricettario.tag_sec where binary tag=%s", (tag,))

    return controllo_risultato_mono(result)