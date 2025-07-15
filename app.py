from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id_, username, password_hash):
        self.id = id_
        self.username = username
        self.password_hash = password_hash

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password_hash FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return User(*user)
    return None

# Routes for authentication
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        conn = sqlite3.connect('recipes.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password))
            conn.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.')
        conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('show_recipes'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('recipes.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        if user and check_password_hash(user[2], password):
            login_user(User(*user))
            return redirect(url_for('show_recipes'))
        else:
            flash('Invalid credentials.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Home page
@app.route('/')
@login_required
def home():
    return render_template('home.html')

# Recipes page with search and category filter
@app.route('/recipes', methods=['GET'])
@login_required
def show_recipes():
    query = request.args.get('search')
    category = request.args.get('category')

    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()

    if query:
        cursor.execute("SELECT * FROM recipes WHERE ingredients LIKE ?", ('%' + query + '%',))
    elif category:
        cursor.execute("SELECT * FROM recipes WHERE LOWER(category) = LOWER(?)", (category,))
    else:
        cursor.execute("SELECT * FROM recipes")

    recipes = cursor.fetchall()
    conn.close()

    return render_template(
        'recipes.html',
        recipes=recipes,
        search=query,
        active_category=category,
        favorites=session.get('favorites', [])
    )

# Favorite recipe route
@app.route('/favorite/<int:recipe_id>')
@login_required
def favorite_recipe(recipe_id):
    favorites = session.get('favorites', [])
    if recipe_id not in favorites:
        favorites.append(recipe_id)
    session['favorites'] = favorites
    return redirect(request.referrer or url_for('show_recipes'))

# Unfavorite recipe route
@app.route('/unfavorite/<int:recipe_id>')
@login_required
def unfavorite_recipe(recipe_id):
    favorites = session.get('favorites', [])
    if recipe_id in favorites:
        favorites.remove(recipe_id)
    session['favorites'] = favorites
    return redirect(request.referrer or url_for('show_recipes'))

@app.route('/favorites')
@login_required
def show_favorites():
    favorites = session.get('favorites', [])
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()

    if favorites:
        placeholders = ','.join(['?'] * len(favorites))
        cursor.execute(f"SELECT * FROM recipes WHERE id IN ({placeholders})", favorites)
        recipes = cursor.fetchall()
    else:
        recipes = []

    conn.close()
    return render_template('favorites.html', recipes=recipes)

# Add new recipe
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        category = request.form['category']

        conn = sqlite3.connect('recipes.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO recipes (title, ingredients, instructions, category) VALUES (?, ?, ?, ?)",
                       (title, ingredients, instructions, category))
        conn.commit()
        conn.close()

        return redirect(url_for('show_recipes'))
    return render_template('add_recipe.html')
@app.route('/test-login-page')
def test_login_page():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
