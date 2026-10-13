from flask import Flask, jsonify , request
import random  # ספרייה שמייצרת מספרים אקראיים
# אתחול השרת שלנו
app = Flask(__name__)

# זה ה"דאטה-בייס" שלנו! מילון שיזכור את המשתמשים כל עוד השרת פועל
users_db = {}

# 4. שליפת כל המשתמשים במערכת (GET All)
@app.route('/api/users', methods=['GET'])
def get_all_users():
    # list(users_db.values()) לוקח את כל המשתמשים מהמילון שלנו והופך אותם לרשימה מסודרת
    return jsonify({
        "status": "success",
        "total_users": len(users_db), # מראה לנו כמה משתמשים יש כרגע
        "users": list(users_db.values())
    }), 200

# שליפת משתמש בודד לפי ID (GET Single)
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    # שוב בדיקת ה-QA שלנו: האם ה-ID הזה בכלל קיים?
    if user_id not in users_db:
        return jsonify({"status": "error", "message": "User not found!"}), 404
        
    # אם הוא קיים, נחזיר רק אותו
    return jsonify({
        "status": "success",
        "user_data": users_db[user_id]
    }), 200


#  הגדרת נתיב POST - מיועד ליצירת משתמש
@app.route('/api/users', methods=['POST'])
def create_user():
    # שולפים את הנתונים ששלחת מפוסטמן
    incoming_data = request.get_json()

    # השרת "ממציא" מזהה ייחודי (מספר בין 1000 ל-9999)
    new_user_id = random.randint(1000, 9999)
    
    # שומרים את המשתמש החדש במילון שלנו
    users_db[new_user_id] = {
        "id": new_user_id,
        "name": incoming_data.get("name", "אורח"),
        "role": incoming_data.get("role", "No role")
    }
    
    # השרת מחזיר לך תשובה אישית שמוכיחה שהוא קרא את הנתונים!
    return jsonify({
        "status": "success",
        "message": "User created!",
        "user_data": users_db[new_user_id]
    }), 201

# 2. עדכון משתמש (PUT) - שימי לב לסוגריים המשולשים בנתיב!
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # קודם כל, כבודקות QA, אנחנו תמיד בודקות מקרי קצה: האם ה-ID בכלל קיים?
    if user_id not in users_db:
        return jsonify({"status": "error", "message": "User not found!"}), 404
        
    incoming_data = request.get_json()
    
    # אם הוא קיים, מעדכנים את הנתונים שלו במילון
    users_db[user_id]["name"] = incoming_data.get("name", users_db[user_id]["name"])
    users_db[user_id]["role"] = incoming_data.get("role", users_db[user_id]["role"])
    
    return jsonify({
        "status": "success",
        "message": f"User {user_id} updated!",
        "user_data": users_db[user_id]
    }), 200

# 3. מחיקת משתמש (DELETE)
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users_db:
        return jsonify({"status": "error", "message": "User not found!"}), 404
        
    # מוחקים לחלוטין את המשתמש מהמערכת
    del users_db[user_id]
    
    return jsonify({
        "status": "success",
        "message": f"User {user_id} was successfully deleted!"
    }), 200

# הפעלת השרת על המחשב שלך
if __name__ == '__main__':
    print("The Server is ready!, Start do CRUD requests")
    app.run(port=5000)


#כתובות API:
# GET ALL & POST- http://127.0.0.1:5000/api/users
# GET SINGLE, PUT & DELETE - http://127.0.0.1:5000/api/users/<user_id>

#BODY EXAMPLES:

# POST - http://127.0.0.1:5000/api/users
{
    "name": "John Doe",
    "role": "Admin"
}

# PUT - http://127.0.0.1:5000/api/users/1234
{
    "name": "Jane Doe",
    "role": "User"
}

