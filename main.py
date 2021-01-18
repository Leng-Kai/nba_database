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

@app.route('/write_done', methods=['GET', 'POST'])
def write_done():
    p_name = request.args.get('p_name_input')
    t_name = request.args.get('t_name_input')
    height = request.args.get('height_input')
    weight = request.args.get('weight_input')
    pos = request.args.get('pos_input')

    if p_name == "":
        return render_template('error.html', err="Player name cannot be left blank.")
    if t_name == "":
        return render_template('error.html', err="Team name cannot be left blank.")
    if height == "":
        return render_template('error.html', err="Height cannot be left blank.")
    if weight == "":
        return render_template('error.html', err="Weight cannot be left blank.")
    if pos == "":
        return render_template('error.html', err="Position cannot be left blank.")
    
    db = sqlite3.connect('nba_database.db')
    cursor = db.cursor()

    query = f"INSERT INTO T_PLAYER(p_name, t_name, height, weight, pos) VALUES ('{p_name}', '{t_name}', {height}, {weight}, '{pos}')"
    print("query:", query)
    cursor.execute(query)
    db.commit()
    return render_template('done.html')

@app.route('/delete_done', methods=['GET', 'POST'])
def delete_done():
    p_name = request.args.get('p_name_input')

    if p_name == "":
        return render_template('error.html', err="Player name cannot be left blank.")
    
    db = sqlite3.connect('nba_database.db')
    cursor = db.cursor()

    query = f"DELETE FROM T_PLAYER WHERE p_name='{p_name}'"
    print("query:", query)
    cursor.execute(query)
    db.commit()
    return render_template('done.html')

@app.route('/modify_done', methods=['GET', 'POST'])
def modify_done():
    p_name = request.args.get('p_name_input')
    t_name = request.args.get('t_name_input')
    height = request.args.get('height_input')
    weight = request.args.get('weight_input')
    pos = request.args.get('pos_input')

    if p_name == "":
        return render_template('error.html', err="Player name cannot be left blank.")

    if t_name == "" and height == "" and weight == "" and pos == "":
        return render_template('error.html', err="Please fill in at least one attribute.")

    modify_attribute = ""
    if t_name != "":
        modify_attribute += f"t_name='{t_name}', "
    if height != "":
        modify_attribute += f"height={height}, "
    if weight != "":
        modify_attribute += f"weight={weight}, "
    if pos != "":
        modify_attribute += f"pos='{pos}', "

    modify_attribute = modify_attribute[:-2]
    
    db = sqlite3.connect('nba_database.db')
    cursor = db.cursor()

    query = f"UPDATE T_PLAYER SET {modify_attribute} WHERE p_name='{p_name}'"
    print("query:", query)
    cursor.execute(query)
    db.commit()
    return render_template('done.html')