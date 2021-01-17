from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/write', methods=['GET', 'POST'])
def write():
    return render_template('write.html')

@app.route('/modify', methods=['GET', 'POST'])
def modify():
    return render_template('modify.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    return render_template('delete.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
    return render_template('query.html')

@app.route('/query_result', methods=['GET', 'POST'])
def query_result():
    p_name = request.args.get('p_name_input')
    t_name = request.args.get('t_name_input')
    c_name = request.args.get('c_name_input')

    name_attribute = ""
    if p_name != "":
        name_attribute += f"p_name='{p_name}' AND "
    if t_name != "":
        name_attribute += f"t_name='{t_name}' AND "
    if c_name != "":
        name_attribute += f"c_name='{c_name}' AND "
    name_attribute = name_attribute[:-4]

    all_attribute_list = ['p_name', 't_name', 'c_name', 'height', 'weight', 'pos', 'city', 'year', 'win', 'lose']
    selected_attribute_list = []
    for attribute in all_attribute_list:
        if request.args.get(attribute):
            print("attribute:", attribute)
            selected_attribute_list.append(attribute)

    print("selected_attribute_list:", selected_attribute_list)
    query_attribute = ""
    for attribute in selected_attribute_list:
        query_attribute += ", " + attribute 
    query_attribute = query_attribute[2:]
    print(query_attribute)
    
    db = sqlite3.connect('nba_database.db')
    cursor = db.cursor()

    param = []
    # query = f"SELECT * FROM T_PLAYER NATURAL JOIN T_TEAM NATURAL JOIN T_COACH NATURAL JOIN T_COACH_IN_TEAM"
    # cursor.execute(query)
    # res = cursor.fetchall()
    # print("res:", res)
    query = f"SELECT {query_attribute} FROM T_PLAYER NATURAL JOIN T_TEAM NATURAL JOIN T_COACH NATURAL JOIN T_COACH_IN_TEAM WHERE {name_attribute}"
    print("query:", query)
    cursor.execute(query)
    res = cursor.fetchall()
    print("res:", res)

    return render_template('query_result.html', param={ 'attr_list': selected_attribute_list, 'result': res })