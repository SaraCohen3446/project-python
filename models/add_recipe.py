import pyodbc

# מתחבר למסד הנתונים של SQL Server באמצעות מחרוזת החיבור שסופקה.
def connect_to_database():
    connection_string = "DRIVER={SQL Server};SERVER=DESKTOP-1VUANBN;DATABASE=RecipeManagement"
    return pyodbc.connect(connection_string)

# מוסיף מתכון חדש לטבלת המתכונים (Recipes), מקשר אותו למשתמש המחובר.
def add_recipe(connection, UserId, title, description, ingredients, instructions, image_filename=None):
    query = "INSERT INTO Recipes (UserID, Title, Description, Ingredients, Instructions, Image) VALUES (?, ?, ?, ?, ?, ?)"
    with connection.cursor() as cursor:
        cursor.execute(query, (UserId, title, description, ingredients, instructions, image_filename))
        connection.commit()
    print("Recipe added successfully!")




