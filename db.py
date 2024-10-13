import mysql.connector
from flask import Flask, request, jsonify
from mysql.connector import Error

def database():
    return mysql.connector.connect(
        host= 'localhost',
        user= 'root',
        password= '',
        database= 'mis602_ass2'
    )

app= Flask(__name__)

@app.route('/registros', methods= ['GET'])
def get_registros():
    try:
        db= database()
        cursor= db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patient")
        registros= cursor.fetchall()
        return jsonify(registros)
    
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
    
@app.route('/registros', methods=['POST'])
def add_registro():
    data = request.get_json()
    
    # Verifica si los campos requeridos están en la solicitud
    if not all(key in data for key in ("name", "dob", "gender", "phone_number", "address", "state_code")):
        return jsonify({'error': 'Faltan datos necesarios.'}), 400

    try:
        db = database()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO patient (name, dob, gender, phone_number, address, state_code) VALUES (%s, %s, %s, %s, %s, %s)",
            (data["name"], data["dob"], data["gender"], data["phone_number"], data["address"], data["state_code"])
        )
        db.commit()
        return jsonify({'message': 'Registro agregado'}), 201

    except Error as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if db.is_connected():
            cursor.close()
            db.close()

@app.route('/registros/<int:id>', methods=['PUT'])
def actualizar_registro(id):
    data= request.json
    db= database()
    cursor= db.cursor()
    cursor.execute("UPDATE patient SET name=%s, dob=%s, gender=%s, phone_number=%s, address=%s, state_code=%s WHERE patient_id= %s",
                (data["name"], data["dob"], data["gender"], data["phone_number"], data["address"], data["state_code"], id))
    
    db.commit()
    cursor.close()
    db.close()
    return jsonify({'message': 'Registro actualizado'}), 200

@app.route('/registros/<int:id>', methods=['DELETE'])
def borrar_registro(id):
    db= database()
    cursor= db.cursor()
    cursor.execute("DELETE FROM patient WHERE patient_id= %s", (id,))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({'message': 'Registro eliminado'}), 200

if __name__ == '__main__':
    app.run(debug=True)