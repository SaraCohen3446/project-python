import pyodbc

# מתחבר למסד הנתונים של SQL Server באמצעות מחרוזת החיבור שסופקה.
def connect_to_database():
    connection_string = "DRIVER={SQL Server};SERVER=DESKTOP-1VUANBN;DATABASE=RecipeManagement"
    return pyodbc.connect(connection_string)

# מוחק תגובה מהטבלה Comments לפי מזהה תגובה (CommentID).
def delete_comment(connection,CommentID):

    query = "DELETE FROM Comments WHERE CommentID = ?"
    with connection.cursor() as cursor:
        cursor.execute(query, (CommentID,))
        connection.commit()
    print("Comment deleted successfully!")