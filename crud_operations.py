from config import *
from functools import wraps


# verify API key
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('api-key')  # Check API key in headers
        if not api_key:
            return jsonify({"msg": "API key is missing"}), 401
        
        key = os.getenv("APIKEY")
        if key != api_key:
            return jsonify({"msg": "Invalid API key"}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def avoid_duplicates(email, cell):
    # Check if user already exists
    existing_cell = User.query.filter_by(cell=cell).first()
    if existing_cell:
        flash("An account with this cell number already exists. Please try to log in.", "error")
        return jsonify({"msg": "Cell number already exists"}), 400
        
    
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        flash("An account with this email already exists. Please log in.", "error")
        return jsonify({"msg": "Email already exists"}), 400
    
    return False


@app.route('/get_users', methods=['GET'])
# @require_api_key
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "name": user.name, "email": user.email, 
                     "cell": user.cell, "Date Created": user.Date_Created,
                     "Last Login": user.Date_Updated} for user in users]), 200
    
@app.route('/get_user/<int:id>', methods=['GET'])
@require_api_key
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
@require_api_key
def delete_user(id):
    user = User.query.get_or_404(id)
    if user:
        db.session.delete(user) 
        db.session.commit()
        return jsonify({"msg": "User deleted"}), 200
    else:
        return jsonify({"msg": "User does not exist"}), 400
    
@app.route('/update_user/<int:id>', methods=['PUT'])
@require_api_key
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
@require_api_key
def add_user():
    data = request.get_json()
    if data:
        is_duplicate = avoid_duplicates(data["email"], data["cell"])
        if is_duplicate:
            return is_duplicate
        data['password'] = generate_password_hash(data['password'], method='sha256')
        db.session.add(User(name=data["name"], email=data["email"],
                            password=data['password'], cell=data["cell"])) 
        db.session.commit()
        return jsonify({"msg": "New User Added"}), 200
    else:
        return jsonify({"msg": "Check your input"}), 400
    
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Page not found"}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "Internal server error"}), 500


