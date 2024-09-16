from config import *


def avoid_duplicates(email, cell):
    # Check if user already exists
    existing_email = User.query.filter_by(email=email).first()
    existing_cell = User.query.filter_by(cell=cell).first()

    if existing_email:
        flash("An account with this email already exists. Please log in.", "error")
        return jsonify({"msg": "Email already exists"}), 400

    if existing_cell:
        flash("An account with this cell number already exists. Please try to log in.", "error")
        return jsonify({"msg": "Cell number already exists"}), 400


@app.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "name": user.name, "email": user.email, 
                     "cell": user.cell, "Date Created": user.Date_Created,
                     "Last Login": user.Date_Updated} for user in users]), 200
    
@app.route('/get_user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.filter(User.id == id).first()
    if user:
        user = user.__dict__
        # del user["password"]
        del user["_sa_instance_state"]
        return jsonify([user]), 200
    else:
        return jsonify({"msg": "User does not exist"}), 400
    
@app.route('/del_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    if user:
        db.session.delete(user) 
        db.session.commit()
        return jsonify({"msg": "User deleted"}), 200
    else:
        return jsonify({"msg": "User does not exist"}), 400
    
@app.route('/update_user/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    if user:
        data = request.get_json()
        for key, value in data.items():
            user.key = value
        db.session.commit()
        return jsonify({"msg": "User updated"}), 200
    else:
        return jsonify({"msg": "User does not exist"}), 400

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    if data:
        avoid_duplicates(data['email'], data['cell'])
        data['password'] = generate_password_hash(data['password'], method='sha256')
        db.session.add(User(name=data["name"], email=data["email"],
                            password=data['password'], cell=data["cell"])) 
        db.session.commit()
        return jsonify({"msg": "New User Added"}), 200
    else:
        return jsonify({"msg": "Check your input"}), 400
    


