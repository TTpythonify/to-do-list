from flask import Flask, render_template, request, redirect, url_for,jsonify
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
    if request.method == "POST":
        task_name = request.form.get("task", "").strip()
        task_info = request.form.get("info", "").strip()
        task_date = request.form.get("due", "").strip()
        task_status = False

        if task_name:
            task_data = {
                "username": username,
                "task_name": task_name,
                "task_info": task_info,
                "task_date": task_date,
                "task_status": task_status
            }

            new_task = add_users_task(task_data)  
            print(new_task)
            # IMPORTANT: Make sure add_users_task returns the row tuple
            # (id, username, task_name, description, date, status)

            # Return JSON instead of redirect
            return jsonify({
                "task": new_task[2],
                "description": new_task[3],
                "due": new_task[4].strftime("%d %b %Y %H:%M")
            })

    users_tasks = get_users_task(username)
    return render_template("todo.html", username=username, users_tasks=users_tasks)


if __name__ == "__main__": 
    app.run(debug=True)
