import pymysql
# import json
# import updata
from flask import Flask,request,jsonify,json
from flask_cors import CORS
import datetime

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='assingment_todo'
)





app= Flask(__name__)


CORS(app)
@app.route('/')
def home():
    return 'Hello, World!!!!'

@app.route('/addUser', methods=['GET','POST'])
def user_add():
    data=request.get_json()
    email=data.get('userName')
    uname=data.get('name')
    password=data.get('password')

    # print(email)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username,email,password) VALUES (%s,%s,%s)",(uname,email,password))
    conn.commit()
    return jsonify({"data":200})
    # conn.close()

@app.route('/login', methods=['GET','POST'])
def user_login():
    data=request.get_json()
    email=data.get('email')
    password=data.get('password')
    cursor = conn.cursor()
    cursor.execute("SELECT userID,username FROM users WHERE email=%s AND password=%s",(email,password))
    user = cursor.fetchall()
    print(user)
    if user:
        return jsonify({"status":user[0][0]})
    else:
        return jsonify({"error":"invalid user."})
    
@app.route('/api/data', methods=['GET','POST'])
def get_data():
    # return {"data":"data1"}
    # cursor = conn.cursor()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM task')
    data=cursor.fetchall()
    columns = [column[0] for column in cursor.description]

# Build list of dictionaries
    json_data = []
    for row in data:
     json_data.append(dict(zip(columns, row)))
     if data:
         return jsonify(json_data)
    else:
        return jsonify(json_data)

@app.route('/createTodo', methods=['GET','POST'])
def create_todo():
    data=request.get_json()
    title=data.get('title')
    status=data.get('st')
    des=data.get('des')
    edate=data.get('ddate')
    uid=data.get('userID')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO task (taskTitle,description,dueDate,userID,status) VALUES (%s,%s,%s,%s,%s)",(title,des,edate,uid,status))
    conn.commit()
    if cursor.rowcount > 0:
        return jsonify({"status":200})
    else:
        return jsonify({"status": "Data is not stored" })


@app.route('/gettodo', methods=['GET','POST'])
def get_todo():
    data=request.get_json()
    uid=data.get('userID')
    # print(uid)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM task WHERE userID=%s",(uid))
    list_data=cursor.fetchall()
    # print(list_data)

    # Fetch column names
    # if(cursor.rowcount > 0):
    columns = [column[0] for column in cursor.description]

        # Build list of dictionaries
    json_list = []
    for row in list_data:
            json_list.append(dict(zip(columns, row)))

    return jsonify(json_list)
    # else:
    #     return jsonify({"status":'no data'})




@app.route('/deletetodo', methods=['GET','POST'])
def delete_todo():
    data=request.get_json()
    tid=data.get('taskId')
    uid=data.get('userID')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM task WHERE userID=%s AND TaskID=%s",(uid,tid))
    conn.commit()
    # conn.close()
    if cursor.rowcount > 0:
        return jsonify({"status":200})
    else:
        return jsonify({"status": "Data is not deleted" })


@app.route('/updatetodo', methods=['PUT','POST'])
def update_todo():
    data = request.get_json()
    tid = data.get('taskId')
    uid = data.get('userID')
    title = data.get('title')
    status = data.get('st')
    des = data.get('des')
    edate = data.get('ddate')
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE task SET taskTitle=%s, description=%s, dueDate=%s, status=%s WHERE userID=%s AND TaskID=%s",
        (title, des, edate, status, uid, tid)
    )
    conn.commit()

    if cursor.rowcount > 0:
        return jsonify({"status": 200})
    else:
        return jsonify({"status": "Data is not updated"})




if __name__=='__main__':

    app.run(debug=True)