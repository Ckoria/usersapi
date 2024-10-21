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
    try:
        is_duplicate = avoid_duplicates(email, cell)
    except Exception as e:
        flash(e, "error")
        is_duplicate = True
    if is_duplicate:
        return render_template("index.html", error= 400)
    # Hash the password
    hashed_password = generate_password_hash(password, method='sha256')
    # Create a new user and add to database
    new_user = User(name=name, email=email, password=hashed_password, cell=cell)
    db.session.add(new_user)
    db.session.commit()

    flash(f"Account created for {name}!", "success")
    return render_template("landing.html")

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
            return render_template("landing.html", user= user.name)
        else:
            flash("Login failed. Check your email or password.", "error")
            return render_template("index.html")
    else:
        flash("Login failed. Account does not exist", "error")
        return render_template("index.html")
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


