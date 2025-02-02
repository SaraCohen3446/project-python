import pyodbc

# מתחבר למסד הנתונים של SQL Server באמצעות מחרוזת החיבור שסופקה.
def connect_to_database():
    connection_string = "DRIVER={SQL Server};SERVER=DESKTOP-1VUANBN;DATABASE=RecipeManagement"
    return pyodbc.connect(connection_string)

# מוסיף תגובה חדשה למתכון.
def add_comment(connection,RecipeID, UserID, Content):

    query = "INSERT INTO Comments (RecipeID, UserID, Content) VALUES (?, ?, ?)"
    with connection.cursor() as cursor:
        cursor.execute(query, (RecipeID, UserID, Content))
        connection.commit()
    print("Comment added successfully!")

