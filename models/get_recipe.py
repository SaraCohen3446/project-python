import pyodbc

# מתחבר למסד הנתונים של SQL Server

def connect_to_database():
    connection_string = "DRIVER={SQL Server};SERVER=DESKTOP-1VUANBN;DATABASE=RecipeManagement"
    return pyodbc.connect(connection_string)

# שולף את המתכון לפי ID

def get_recipe_by_id(connection, recipe_id):
    query = "SELECT RecipeID, Title, Description, Ingredients, Instructions, Image, DateCreated FROM Recipes WHERE RecipeID = ?"
    cursor = connection.cursor()
    cursor.execute(query, (recipe_id,))
    result = cursor.fetchone()

    if result:
        return {
            'recipe_id': result.RecipeID,
            'title': result.Title,
            'description': result.Description,
            'ingredients': result.Ingredients,
            'instructions': result.Instructions,
            'image': result.Image,  # Add this line to get the image filename
            'date_created': result.DateCreated
        }
    return None


# שולף את כל המתכונים של המשתמש

def get_user_recipes(connection, user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT RecipeID, Title, Description FROM Recipes WHERE UserId = ?", (user_id,))
    recipes = cursor.fetchall()
    return [{'recipe_id': row.RecipeID, 'title': row.Title, 'description': row.Description} for row in recipes]

# שולף מתכון לפי כותרת

def get_recipe_by_title(connection, title):
    query = "SELECT RecipeID, Title, Description, Ingredients, Instructions, DateCreated FROM Recipes WHERE Title LIKE ?"
    cursor = connection.cursor()
    cursor.execute(query, ('%' + title + '%',))  # חיפוש חלקי
    results = cursor.fetchall()

    return [
        {
            'recipe_id': row.RecipeID,
            'title': row.Title,
            'description': row.Description,
            'ingredients': row.Ingredients,
            'instructions': row.Instructions,
            'image': row.Image,
            'date_created': row.DateCreated
        }
        for row in results
    ]


# שולף את כל התגובות למתכון
def get_comments_by_recipe_id(connection, recipe_id):
    query = "SELECT CommentID, Content, DateCreated FROM Comments WHERE RecipeID = ?"
    cursor = connection.cursor()
    cursor.execute(query, (recipe_id,))
    return [{'comment_id': row.CommentID, 'content': row.Content, 'date_created': row.DateCreated} for row in cursor.fetchall()]

# שולף את כל המתכונים
def get_all_recipes(connection):
    query = "SELECT RecipeID, Title, Description FROM Recipes"
    cursor = connection.cursor()
    cursor.execute(query)
    recipes = cursor.fetchall()
    return [{'recipe_id': row.RecipeID, 'title': row.Title, 'description': row.Description} for row in recipes]
