# 🍳 Recipe Ideas Web App

A full-stack web application built using Python (Flask) for the backend, SQLite as the database, and HTML/CSS (TailwindCSS) for the frontend. It allows users to browse, add, and favorite recipes with authentication.

---

## ✅ Features

* User Registration & Login System (Authentication using Flask-Login)
* Browse Recipes (Veg, Non-Veg, Starters, Dessert, Main Course)
* Add Your Own Recipes (Stored with Title, Ingredients, Instructions, Category)
* Mark Recipes as Favorite
* View Favorite Recipes Separately
* Responsive, Simple UI using TailwindCSS
* SQLite Database Integration

---

## 🛠️ Technologies Used

* **Backend**: Python, Flask, Flask-Login
* **Frontend**: HTML, TailwindCSS, Jinja2 (Flask templating engine)
* **Database**: SQLite (managed via Python’s `sqlite3` library)

---

## ⚙️ Installation & Setup Instructions


1. Install Dependencies
   Make sure Python is installed on your system.
   Then install required packages:

```bash
pip install flask flask-login werkzeug
```

2. Setup Database
   Run the following Python script to create the database and sample data:

```bash
python db_setup.py
```

3. Run the App

```bash
python app.py
```

Flask development server will start, usually on:
`http://127.0.0.1:5000/`

4. Access the App

* Open your browser and go to: `http://127.0.0.1:5000/`
* Register as a new user.
* Log in using your credentials.
* Add, browse, and favorite recipes.

---

## 🔒 User Authentication Flow

* User Registration (`/register`): Stores hashed passwords in `users` table.
* User Login (`/login`): Verifies credentials using hashed password checking.
* Protected Routes: Only logged-in users can access recipes, add recipes, and favorites.
* Logout (`/logout`): Ends user session securely.

---

## 📂 Project Structure

```
recipe-ideas-app/
│
├── app.py                # Main Flask application  
├── db_setup.py           # Script for creating and populating the SQLite database  
├── recipes.db            # SQLite database file  
├── templates/            # HTML templates with Jinja2 + Tailwind  
│   ├── home.html  
│   ├── recipes.html  
│   ├── add_recipe.html  
│   ├── favorites.html  
│   ├── login.html  
│   └── register.html  
├── static/               # (Optional) Static assets like images/icons if used  
└── README.md             # Project instructions
```

---

## ✅ Important Notes

* Database:
  We used SQLite for simplicity. No external database like MongoDB was required.

* Backend:
  Python + Flask handle all business logic, routing, and authentication.

* Frontend:
  HTML + TailwindCSS for clean and responsive UI. No separate frontend framework.

---

## 🌟 Future Improvements (Optional Ideas)

* Add image upload support for recipes.
* Integrate pagination or search autocomplete.
* Host the app online (Heroku, Vercel, or PythonAnywhere).

---

## 🤝 Acknowledgments

This project was structured and built as a learning exercise for full-stack development using Python Flask and SQLite.
