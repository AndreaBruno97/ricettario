"""
Funzioni che permettono l'interazione col database
"""

import pymysql

def all_ricette():
    #Restituisce id e nome di tutte le ricette nel database
    conn = pymysql.connect(user='root', password='root',
                           host='localhost', database='')
    cursor = conn.cursor()
    sql = "select id, nome from ricettario.ricettario"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def id_to_nome(id):
    conn = pymysql.connect(user='root', password='root',
                           host='localhost', database='')
    cursor = conn.cursor()
    sql = "select nome from ricettario.ricettario where id=%s"
    cursor.execute(sql, (id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def nome_to_id(nome):
    conn = pymysql.connect(user='root', password='root',
                           host='localhost', database='')
    cursor = conn.cursor()
    sql = "select id from ricettario.ricettario where nome=%s"
    cursor.execute(sql, (nome,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def new_ricetta(nome):
    #Controllo se la ricetta esiste già
    result=nome_to_id(nome)
    if(len(result)==0):
        conn = pymysql.connect(user='root', password='root',
                               host='localhost', database='')
        cursor = conn.cursor()
        sql = "insert into ricettario.ricettario(nome) values (%s)"
        cursor.execute(sql, (nome,))
        conn.commit()
        cursor.close()
        conn.close()
    else:
        return -1