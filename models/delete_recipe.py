import pyodbc


# מתחבר למסד הנתונים של SQL Server באמצעות מחרוזת החיבור שסופקה.
def connect_to_database():
    connection_string = "DRIVER={SQL Server};SERVER=DESKTOP-1VUANBN;DATABASE=RecipeManagement"
    return pyodbc.connect(connection_string)


# מוחק מתכון מהטבלה Recipes לפי מזהה מתכון (RecipeID).
def delete_recipe(connection, RecipeID):
    with connection.cursor() as cursor:
        # מחיקת כל התגובות שקשורות למתכון
        cursor.execute("DELETE FROM Comments WHERE RecipeID = ?", (RecipeID,))

        # מחיקת המתכון עצמו
        cursor.execute("DELETE FROM Recipes WHERE RecipeID = ?", (RecipeID,))

        connection.commit()

    print("Recipe and related comments deleted successfully!")
