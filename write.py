import sqlite3
import csv

conn = sqlite3.connect('nba_database.db')
c = conn.cursor()

#a1 = input("a1: ")
#a2 = input("a2: ")
#a2 = "BOS"
#a3 = input("a3: ")
#weight = input("weight: ")
#t_name = input("t_name: ")
#pos = input("pos: ")

for i in range(2020, 2021):
    a1 = i
    a2 = "CHI"
    a3 = "Billy Donovan"
    query = f'insert into T_COACH_IN_TEAM(year, t_name, c_name) values ({a1}, "{a2}", "{a3}")'

    print(query)

    c.execute(query)
    conn.commit()
