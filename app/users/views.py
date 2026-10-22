from flask import request, redirect, url_for, render_template
from app.users import user_bp

@user_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, type=int)
    return render_template("users/hi.html", name=name, age=age)

@user_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    print(f"Redirecting to: {to_url}")
    return redirect(to_url)