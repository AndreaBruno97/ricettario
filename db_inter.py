"""
Funzioni che permettono l'interazione col database
"""

import pymysql

def connetti():
    return pymysql.connect(user='root', password='root',
                           host='localhost', database='')

def all_ricette():
    #Restituisce id e nome di tutte le ricette nel database
    conn = connetti()
    cursor = conn.cursor()
    sql = "select id, nome from ricettario.ricettario"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def id_to_nome(id):
    """
    :param id: intero positivo da cercare
    :return: stringa se esiste, stringa vuota altrimenti
    """
    conn = connetti()
    cursor = conn.cursor()
    sql = "select nome from ricettario.ricettario where id=%s"
    cursor.execute(sql, (id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    if len(result)==0:
        return -1
    else:
        return result[0][0]

def nome_to_id(nome):
    """
    :param nome: stringa da cercare
    :return: intero positivo se esiste, -1 altrimenti
    """
    conn = connetti()
    cursor = conn.cursor()
    sql = "select id from ricettario.ricettario where binary nome=%s"
    cursor.execute(sql, (nome,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    if len(result)==0:
        return -1
    else:
        return result[0][0]

def new_ricetta(nome):
    #Controllo se la ricetta esiste già
    id=nome_to_id(nome)

    if(id<0):
        conn = connetti()
        cursor = conn.cursor()
        sql = "insert into ricettario.ricettario(nome) values (%s)"
        cursor.execute(sql, (nome,))
        conn.commit()
        cursor.close()
        conn.close()
    else:
        return -1

def elimina_ricetta(id):
    #Controllo se la ricetta esiste#
    result=id_to_nome(id)
    if(len(result)!=0):
        conn = connetti()
        sql = "delete from ricettario.ricettario where id=%s"
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        conn.commit()
        cursor.close()
        conn.close()
    else:
        return -1