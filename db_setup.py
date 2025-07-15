import sqlite3

# Connect (or create) a database file
conn = sqlite3.connect('recipes.db')
cursor = conn.cursor()

# Create the recipes table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        ingredients TEXT NOT NULL,
        instructions TEXT NOT NULL,
        category TEXT NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
''')


# Add sample recipes (optional but helpful for testing)
sample_data = [
    ("Tomato Pasta", "tomato, pasta, garlic", "Boil pasta, sauté garlic, add tomatoes.", "veg"),
    ("Chicken Curry", "chicken, onion, spices", "Cook onions, add chicken and spices.", "nonveg"),
    ("Chocolate Cake", "flour, cocoa, sugar, eggs", "Mix, bake at 180C for 30 mins.", "dessert")
]

cursor.executemany('''
    INSERT INTO recipes (title, ingredients, instructions, category)
    VALUES (?, ?, ?, ?)
''', sample_data)

# Save changes and close connection
conn.commit()
conn.close()

print("✅ recipes.db created and populated with sample recipes!")
