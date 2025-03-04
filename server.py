from flask import Flask, render_template, request, redirect, url_for, session
from models import sign_in, add_comment, add_recipe, log_in, get_recipe, delete_recipe, delete_user
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

#לשמירת USERID נוכחי
app.secret_key = 'your_secret_key_here'
#משתנה לשמירת מחרוזת הניתוב לשמירת התמונה
UPLOAD_FOLDER = 'static/uploads'
#משתנה לשמירת סוגי הקבצים המותרים לעלות
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
#משתנה שמכיל את הניתוב ממש של התיקייה בה יישמרו הקבצים
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# פונקציה לבדיקה אם הקובץ הנבחר לעלות הוא מסוג הקבצים המותרים לעלות
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Home page
@app.route('/', methods=['GET', 'POST'])
def root():
    user_id = session.get('user_id')

    # אם מתבצע חיפוש, נעביר את השאילתה למסלול get_recipe_by_title
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        return redirect(url_for('get_recipe_by_title', title=title))

    # אם אין חיפוש, נשלוף את כל המתכונים
    with get_recipe.connect_to_database() as connection:
        recipes = get_recipe.get_all_recipes(connection)

    return render_template('Server.html', user_id=user_id, recipes=recipes)



# View comments for a specific recipe
@app.route('/recipe/<int:recipe_id>/comments')
def view_recipe_comments(recipe_id):
    with get_recipe.connect_to_database() as connection:
        recipe = get_recipe.get_recipe_by_id(connection, recipe_id)  # נוסיף שליפת מתכון
        comments = get_recipe.get_comments_by_recipe_id(connection, recipe_id)

    if not recipe:
        return "Recipe not found", 404  # אם המתכון לא נמצא, נשלח שגיאה

    return render_template('RecipeComments.html', comments=comments, recipe=recipe)

# Sign up new user
@app.route('/sign_in', methods=['GET', 'POST'])
def add_new_user():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not email or not password:
            return "All fields are required", 400

        with sign_in.connect_to_database() as connection:
            sign_in.sign_in(connection, username, email, password)

        return redirect(url_for('login'))
    return render_template('SignIn.html')


# Login user
@app.route('/log_in', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        with log_in.connect_to_database() as connection:
            user_id = log_in.login_user(connection, username, password)

        if user_id:
            session['user_id'] = user_id  # Save user_id in session
            return redirect(url_for('root'))  # Redirect to home page
        else:
            return render_template('LogIn.html', error="Invalid username or password.")
    return render_template('LogIn.html')


# User Dashboard - Display user recipes
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    with get_recipe.connect_to_database() as connection:
        user_recipes = get_recipe.get_user_recipes(connection, session['user_id'])

    return render_template('UserDashboard.html', user_recipes=user_recipes)


# View a specific recipe by ID
@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    with get_recipe.connect_to_database() as connection:
        recipe = get_recipe.get_recipe_by_id(connection, recipe_id)

    if recipe:
        return render_template('RecipeDetails.html', recipe=recipe)
    return "Recipe not found", 404


# Add comment to a recipe
@app.route('/recipe/<int:recipe_id>/comments', methods=['POST'])
def add_recipe_comment(recipe_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    content = request.form.get('content', '').strip()

    if not content:
        return "Comment content is required.", 400

    with add_comment.connect_to_database() as connection:
        add_comment.add_comment(connection, recipe_id, session['user_id'], content)

    return redirect(url_for('view_recipe', recipe_id=recipe_id))

# Delete a recipe
@app.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
def delete_recipe_route(recipe_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    with delete_recipe.connect_to_database() as connection:
        delete_recipe.delete_recipe(connection, recipe_id)

    return redirect(url_for('dashboard'))


# הוספת מתכון חדש
@app.route('/add_new_recipe', methods=['GET', 'POST'])
def add_new_recipe():
    # אם המשתמש לא מחובר, להפנות אותו לדף ההתחברות
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # שליפת הנתונים מהטופס והסרת רווחים מיותרים
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        ingredients = request.form.get('ingredients', '').strip()
        instructions = request.form.get('instructions', '').strip()

        # קבלת תמונה מהמשתמש
        image = request.files.get('image')

        # בדיקה שכל השדות חובה מולאו
        if not title or not description or not ingredients or not instructions:
            return "All fields (title, description, ingredients, instructions) are required", 400

        image_filename = None
        if image and allowed_file(image.filename):
            # יצירת שם קובץ מאובטח ושמירת התמונה
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path)

        # הוספת המתכון למסד הנתונים כולל נתיב התמונה אם קיים
        with add_recipe.connect_to_database() as connection:
            add_recipe.add_recipe(connection, session['user_id'], title, description, ingredients, instructions,
                                  image_filename)

        # הפניה ללוח הבקרה לאחר ההוספה
        return redirect(url_for('dashboard'))

    # הצגת טופס הוספת מתכון במקרה של בקשת GET
    return render_template('AddRecipe.html')


# צפייה במתכון לפי כותרת
@app.route('/get_recipe_by_title', methods=['GET'])
def get_recipe_by_title():
    title = request.args.get('title', '').strip()

    if not title:
        return "Title is required", 400

    with get_recipe.connect_to_database() as connection:
        recipe = get_recipe.get_recipe_by_title(connection, title)

    if recipe:
        return render_template('RecipeDetails.html', recipe=recipe)

    return "Recipe not found", 404


# מחיקת משתמש
@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user_by_id():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        with delete_user.connect_to_database() as connection:
            delete_user.delete_user(connection, session['user_id'])

        session.pop('user_id', None)  # מחיקת המשתמש גם מה-session
        return redirect(url_for('root'))
    return render_template('DeleteUser.html')


# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user from session
    return redirect(url_for('root'))


if __name__ == '__main__':
    app.run(debug=True, port=3000)
