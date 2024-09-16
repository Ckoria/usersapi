from config import *
from crud_operations import *
 
# Route for home (with forms)
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle Sign Up
@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    cell = request.form['cell']
    password = request.form['password']
    avoid_duplicates(email, cell)
    # Hash the password
    hashed_password = generate_password_hash(password, method='sha256')
    # Create a new user and add to database
    new_user = User(name=name, email=email, password=hashed_password, cell=cell)
    db.session.add(new_user)
    db.session.commit()

    flash(f"Account created for {name}!", "success")
    return jsonify({"msg": f"Account created for {name}"}), 201

# Route to handle Login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Query user from database
    user = User.query.filter_by(email=email).first()

    if user: 
        if check_password_hash(user.password, password):
            flash("Login successful!", "success")
            user.Date_Updated = datetime.now()
            db.session.commit()
            return jsonify({"msg": f"Succesfully logged in as {user.name}"}), 200
        else:
            flash("Login failed. Check your email or password.", "error")
            return jsonify({"msg": "Login failed. Check email or password"}), 401
    else:
        return jsonify({"msg": "Login failed. Account does not exist"}), 401


