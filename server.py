from flask import Flask, render_template, request, redirect, url_for, session
from models import sign_in, add_comment, add_recipe, log_in, get_recipe, delete_comment, delete_recipe, delete_user
import pyodbc

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management

# Home page
@app.route('/')
def root():
    return render_template('Server.html')

# Sign up
@app.route('/sign_in', methods=['GET', 'POST'])
def add_new_user():
    if request.method == 'POST':
        username = request.form.get('username', '')
        email = request.form.get('email', '')
        password = request.form.get('password', '')

        connection = sign_in.connect_to_database()
        sign_in.sign_in(connection, username, email, password)
        connection.close()
        return redirect(url_for('login'))
    return render_template('SignIn.html')

# Log in
@app.route('/log_in', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        connection = log_in.connect_to_database()
        user_id = log_in.login_user(connection, username, password)
        connection.close()

        if user_id:
            session['user_id'] = user_id  # Store user ID in session
            return redirect(url_for('dashboard'))
        else:
            return "Invalid username or password.", 401
    return render_template('LogIn.html')

# User dashboard
@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    return render_template('UserDashboard.html')

# Add recipe
@app.route('/add_recipe', methods=['GET', 'POST'])
def add_new_recipe():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title', '')
        description = request.form.get('description', '')
        ingredients = request.form.get('ingredients', '')
        instructions = request.form.get('instructions', '')

        connection = add_recipe.connect_to_database()
        add_recipe.add_recipe(connection, user_id, title, description, ingredients, instructions)
        connection.close()
        return redirect(url_for('dashboard'))
    return render_template('AddRecipe.html')

#show comment


# Add comment
@app.route('/add_ccomment', methods=['GET', 'POST'])
def add_new_comment():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    if request.method == 'POST':
        content = request.form.get('Content', '')
        recipe_id = request.form.get('RecipeID', '')

        connection = add_comment.connect_to_database()
        add_comment.add_comment(connection, recipe_id, user_id, content)
        connection.close()
        return redirect(url_for('dashboard'))
    return render_template('AddComment.html')

# Get recipes
@app.route('/get_recipe_by_title', methods=['GET', 'POST'])
def view_recipe():
    if request.method == 'POST':
        title = request.form.get('Title', '')  # קבלת כותרת המתכון
        connection = get_recipe.connect_to_database()
        recipe = get_recipe.get_recipe_by_title(connection, title)
        connection.close()

        if recipe:
            return render_template('RecipeDetails.html', recipe=recipe)
        else:
            return "Recipe not found", 404
    return render_template('GetRecipeByTitle.html')




# Delete comment
@app.route('/delete_comment', methods=['GET', 'POST'])
def delete_comment_by_id():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    if request.method == 'POST':
        comment_id = request.form.get('CommentID', '')
        if not comment_id.isdigit():
            return "Invalid CommentID", 400
        connection = delete_comment.connect_to_database()
        delete_comment.delete_comment(connection, comment_id)
        connection.close()
        return redirect(url_for('dashboard'))
    return render_template('DeleteComment.html')

# Delete user
@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user_by_id():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    if request.method == 'POST':
        connection = delete_user.connect_to_database()
        delete_user.delete_user(connection, user_id)
        connection.close()
        return redirect(url_for('root'))
    return render_template('DeleteUser.html')

# Delete recipe
@app.route('/delete_recipe', methods=['GET', 'POST'])
def delete_recipe_by_id():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    if request.method == 'POST':
        recipe_id = request.form.get('RecipeID', '')
        if not recipe_id.isdigit():
            return "Invalid RecipeID", 400
        connection = delete_recipe.connect_to_database()
        delete_recipe.delete_recipe(connection, recipe_id)
        connection.close()
        return redirect(url_for('dashboard'))
    return render_template('DeleteRecipe.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    return redirect(url_for('root'))

if __name__ == '__main__':
    app.run(debug=True, port=3000)
