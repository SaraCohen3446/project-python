import pyodbc

# מתחבר למסד הנתונים של SQL Server באמצעות מחרוזת החיבור שסופקה.
def connect_to_database():
    connection_string = "DRIVER={SQL Server};SERVER=DESKTOP-1VUANBN;DATABASE=RecipeManagement"
    return pyodbc.connect(connection_string)

# רושם משתמש חדש על ידי הוספת פרטיו לטבלת המשתמשים (Users).
def sign_in(connection, username, email, password):
    query = "INSERT INTO Users (Username, Email, Password) VALUES (?, ?, ?)"
    with connection.cursor() as cursor:
        cursor.execute(query, (username, email, password))
        connection.commit()

