import pymysql
from flask import Flask,request,jsonify,json
from flask_cors import CORS

# connection with pythonanywhere MySQL database.
# conn = pymysql.connect(
#     host='Rajatkumar.mysql.pythonanywhere-services.com',
#     user='Rajatkumar',
#     password='todo@123',
#     database='Rajatkumar@todo'
# )


# local batabase connection with MySQL.
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


# Api method for add user Or user SignUP.
@app.route('/addUser', methods=['GET','POST'])
def user_add():
    # collecting data form front-End
    data=request.get_json()
    email=data.get('userName')
    uname=data.get('name')
    password=data.get('password')

    # Creating Connection
    cursor = conn.cursor()
    # Executing Insert Statement.
    cursor.execute("INSERT INTO userstest (username,email,password) VALUES (%s,%s,%s)",(uname,email,password))
    # Commit the transaction.
    conn.commit()
    # return data to front-end.
    return jsonify({"data":200})


# Api method Validate Login.
@app.route('/login', methods=['GET','POST'])
def user_login():
    # collecting data form front-End.
    data=request.get_json()
    email=data.get('email')
    password=data.get('password')

    # Creating Connection
    cursor = conn.cursor()

    # Executing SELECT Statement.
    cursor.execute("SELECT userID,username FROM userstest WHERE email=%s AND password=%s",(email,password))

    # Fetching data
    user = cursor.fetchall()

    # validating data and sending response.
    if user:
        return jsonify({"status":user[0][0]})
    else:
        return jsonify({"error":"invalid user."})
    


# Api method Validate Login.
# @app.route('/api/data', methods=['GET','POST'])
# def get_data():
#     # return {"data":"data1"}
#     # cursor = conn.cursor()
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM userstest')
#     data=cursor.fetchall()
#     columns = [column[0] for column in cursor.description]

# # Build list of dictionaries
#     json_data = []
#     for row in data:
#      json_data.append(dict(zip(columns, row)))
#      if data:
#         return jsonify(json_data)
#     else:
#         return jsonify(json_data)


# Api method for creating todo.
@app.route('/createTodo', methods=['GET','POST'])
def create_todo():
    # collecting data form front-End.
    data=request.get_json()
    title=data.get('title')
    status=data.get('st')
    des=data.get('des')
    edate=data.get('ddate')
    uid=data.get('userID')

    # Creating Connection
    cursor = conn.cursor()

    # Executing INSERT Statement.
    cursor.execute("INSERT INTO task (taskTitle,description,dueDate,userID,status) VALUES (%s,%s,%s,%s,%s)",(title,des,edate,uid,status))

    # Commit the transaction.
    conn.commit()

    # validating data and sending response.
    if cursor.rowcount > 0:
        return jsonify({"status":200})
    else:
        return jsonify({"status": "Data is not stored" })




# Api method for getting todo list of perticular user.
@app.route('/gettodo', methods=['GET','POST'])
def get_todo():

    # collecting data form front-End.
    data=request.get_json()
    uid=data.get('userID')

    # Creating Connection
    cursor = conn.cursor()

    # Executing SELET Statement on task table.
    cursor.execute("SELECT * FROM task WHERE userID=%s",(uid))
    list_data=cursor.fetchall()

    # Fetch column names
    # if(cursor.rowcount > 0):
    columns = [column[0] for column in cursor.description]

    # Build list of dictionaries
    json_list = []
    for row in list_data:
            json_list.append(dict(zip(columns, row)))


    # sending response.
    return jsonify(json_list)
    



# Api method for delete todo of perticular user.
@app.route('/deletetodo', methods=['GET','POST'])
def delete_todo():

    # collecting data form front-End.
    data=request.get_json()
    tid=data.get('taskId')
    uid=data.get('userID')

    # Creating Connection
    cursor = conn.cursor()

     # Executing DELETE Statement on task table.
    cursor.execute("DELETE FROM task WHERE userID=%s AND TaskID=%s",(uid,tid))

    # Commit the transaction.
    conn.commit()


    # Validating response and sending to fornt-end.
    if cursor.rowcount > 0:
        return jsonify({"status":200})
    else:
        return jsonify({"status": "Data is not deleted" })



# Api method for Update/Edit todo of perticular user.
@app.route('/updatetodo', methods=['PUT','POST'])
def update_todo():

     # collecting data form front-End.
    data = request.get_json()
    tid = data.get('taskId')
    uid = data.get('userID')
    title = data.get('title')
    status = data.get('st')
    des = data.get('des')
    edate = data.get('ddate')


    # Creating Connection
    cursor = conn.cursor()


    # Executing UPDATE Statement on task table.
    cursor.execute(
        "UPDATE task SET taskTitle=%s, description=%s, dueDate=%s, status=%s WHERE userID=%s AND TaskID=%s",
        (title, des, edate, status, uid, tid)
    )

    # Commit the transaction.
    conn.commit()

    # Validating response and sending to fornt-end.
    if cursor.rowcount > 0:
        return jsonify({"status": 200})
    else:
        return jsonify({"status": "Data is not updated"})




if __name__=='__main__':

    app.run(debug=True)