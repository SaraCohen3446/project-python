import pyodbc

# מתחבר למסד הנתונים של SQL Server באמצעות מחרוזת החיבור שסופקה.
def connect_to_database():
    connection_string = "DRIVER={SQL Server};SERVER=DESKTOP-1VUANBN;DATABASE=RecipeManagement"
    return pyodbc.connect(connection_string)

# מבצע התחברות של משתמש קיים על ידי אימות שם המשתמש והסיסמה.
def login_user(connection, Username, Password):
    query = "SELECT UserID FROM Users WHERE Username = ? AND Password = ?"
    with connection.cursor() as cursor:
        cursor.execute(query, (Username, Password))
        result = cursor.fetchone()
    if result:
        print("Login successful!")
        return result[0]
    else:
        return print("Invalid username or password.")
