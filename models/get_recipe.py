import pyodbc

# מתחבר למסד הנתונים של SQL Server באמצעות מחרוזת החיבור שסופקה.
def connect_to_database():
    connection_string = "DRIVER={SQL Server};SERVER=DESKTOP-1VUANBN;DATABASE=RecipeManagement"
    return pyodbc.connect(connection_string)

# שולף מתכון לפי כותרת ומציג את פרטיו.
def get_recipe_by_title(connection, title):
    query = "SELECT * FROM Recipes WHERE Title = ?"
    with connection.cursor() as cursor:
        cursor.execute(query, (title,))
        result = cursor.fetchone()

    if result:
        return {
            'title': result.Title,
            'description': result.Description,
            'ingredients': result.Ingredients,
            'instructions': result.Instructions,
            'date_created': result.DateCreated
        }
    return None

def get_comments_by_recipe_id(connection, recipe_id):
    query = "SELECT CommentID, Content, DateCreated FROM Comments WHERE RecipeID = ?"
    with connection.cursor() as cursor:
        cursor.execute(query, (recipe_id,))
        return cursor.fetchall()  # מחזיר את כל התגובות של המתכון


