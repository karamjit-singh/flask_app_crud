import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

# create Student			
@app.route('/create', methods=['POST'])
def create_student():
    _json = request.json
    _first_name = _json['first_name']
    _last_name = _json['last_name']
    _dob = _json['dob']
    _amount_due = _json['amount_due']
    
    # insert record in database
    sqlQuery = "INSERT INTO student(first_name, last_name, dob, amount_due) VALUES (%s, %s, %s, %s)"
    
    data = (_first_name, _last_name, _dob, _amount_due)
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sqlQuery, data)
    conn.commit()
    
    res = jsonify('Student created successfully.')
    res.status_code = 200

    return res
    
        
@app.route('/student')
def student():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM student")
    rows = cursor.fetchall()
    res = jsonify(rows)
    res.status_code = 200

    return res
    
        
@app.route('/student/<int:student_id>')
def get_student(student_id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM student WHERE student_id=%s", student_id)
    row = cursor.fetchone()
    res = jsonify(row)
    res.status_code = 200

    return res
   

@app.route('/update', methods=['PUT'])
def update_student():
    _json = request.json
    _student_id = _json['student_id']
    _first_name = _json['first_name']
    _last_name = _json['last_name']
    _dob = _json['dob']
    _amount_due = _json['amount_due']

        
    # update record in database
    sql = "UPDATE student SET first_name=%s, last_name=%s, dob=%s, amount_due=%s WHERE student_id=%s"
    data = (_first_name, _last_name, _dob, _amount_due, _student_id,)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, data)
    conn.commit()
    res = jsonify('Student updated successfully.')
    res.status_code = 200

    return res


# delete student record from database		
@app.route('/delete/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student WHERE student_id=%s", (student_id,))
    conn.commit()
    
    res = jsonify('Student deleted successfully.')
    res.status_code = 200
    
    return res
     
     
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'There is no record: ' + request.url,
    }
    res = jsonify(message)
    res.status_code = 404

    return res
   
   
if __name__ == "__main__":
    app.run(debug=True)