import pyodbc

# מתחבר למסד הנתונים של SQL Server באמצעות מחרוזת החיבור שסופקה.
def connect_to_database():
    connection_string = "DRIVER={SQL Server};SERVER=DESKTOP-1VUANBN;DATABASE=RecipeManagement"
    return pyodbc.connect(connection_string)

# מוחק מתכון מהטבלה Recipes לפי מזהה מתכון (RecipeID).
def delete_recipe(connection,RecipeID):

    query = "DELETE FROM Recipes WHERE RecipeID = ?"
    with connection.cursor() as cursor:
        cursor.execute(query, (RecipeID,))
        connection.commit()
    print("Recipe deleted successfully!")
