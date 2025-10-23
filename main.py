from flask import Flask, render_template, request, redirect, url_for
from database import * 

app = Flask(__name__)

# Ensure the table exists
create_table()

@app.route('/')
def index_page():
    return render_template("index.html")

@app.route("/set_owner", methods=["POST"])
def set_owner():
    owner_name = request.form.get("ownerName", "").strip().upper()
    
    if owner_name:
        # Get or create user (avoids duplicate key errors)
        user_id = get_or_create_user(owner_name)
        return redirect(url_for("todo", username=owner_name))
    
    return redirect(url_for("index_page"))

@app.route("/todo/<username>", methods=["GET", "POST"])
def todo(username):
    user_tasks = []
    if request.method == "POST":
        task_name = request.form.get("task", "").strip()
        task_info = request.form.get("info", "").strip()
        task_date = request.form.get("due", "").strip()
        task_status = False

        if task_name:
            user_tasks.append({
            "username":username,
            "task_name": task_name,
            "task_info": task_info,
            "task_date": task_date,
            "task_status": task_status
            })
            add_users_task(user_tasks[0])


        return redirect(url_for("todo", username=username))

       
    print(get_users_task(username))


    return render_template("todo.html", username=username)


if __name__ == "__main__":
    app.run(debug=True)
