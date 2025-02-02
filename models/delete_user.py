import pyodbc

# מתחבר למסד הנתונים של SQL Server באמצעות מחרוזת החיבור שסופקה.
def connect_to_database():
    connection_string = "DRIVER={SQL Server};SERVER=DESKTOP-1VUANBN;DATABASE=RecipeManagement"
    return pyodbc.connect(connection_string)

# מוחק משתמש מהטבלה Users לפי מזהה משתמש (UserID).
def delete_user(connection, UserID):
    query1 = "DELETE FROM Recipes WHERE UserID = ?"
    query2 = "DELETE FROM Comments WHERE UserID = ?"
    query3 = "DELETE FROM Users WHERE UserID = ?"
    with connection.cursor() as cursor:
        cursor.execute(query1, (UserID,))
        cursor.execute(query2, (UserID,))
        cursor.execute(query3, (UserID,))
        connection.commit()
    print("User deleted successfully!")