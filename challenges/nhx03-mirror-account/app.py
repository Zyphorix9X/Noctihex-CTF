import os

from flask import (
    Flask,
    request,
    redirect,
    url_for,
    session,
    render_template,
    abort
)

from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)

# Read private values from environment variables
app.secret_key = os.environ["NHX03_SECRET_KEY"]

FLAG = os.environ["NHX03_FLAG"]
EVIDENCE = os.environ["NHX03_EVIDENCE"]

# Allows Flask to respect the Nginx path prefix:
# /labs/nhx03/
app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_prefix=1
)


# Fictional challenge users only
USERS = {
    "tester": {
        "password": "noctihex123",
        "profile_id": 1
    }
}


# Fictional profile records
PROFILES = {
    1: {
        "username": "tester",
        "role": "Junior Analyst",
        "note": "Standard NoctiHex test account."
    },

    2: {
        "username": "archive",
        "role": "Incident Analyst",
        "note": (
            "Recovered HEX-SHADOW record. "
            f"Flag: {FLAG} | "
            f"Evidence fragment: {EVIDENCE}"
        )
    },

    3: {
        "username": "nightwatch",
        "role": "Monitoring",
        "note": "Routine monitoring profile."
    }
}


@app.route("/")
def index():
    if "username" not in session:
        return redirect(url_for("login"))

    return redirect(
        url_for(
            "profile",
            profile_id=session["profile_id"]
        )
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        user = USERS.get(username)

        if user and user["password"] == password:
            session["username"] = username
            session["profile_id"] = user["profile_id"]

            return redirect(
                url_for(
                    "profile",
                    profile_id=user["profile_id"]
                )
            )

        error = "Invalid username or password"

    return render_template(
        "login.html",
        error=error
    )


@app.route("/profile/<int:profile_id>")
def profile(profile_id):

    if "username" not in session:
        return redirect(url_for("login"))

    profile_data = PROFILES.get(profile_id)

    if profile_data is None:
        abort(404)

    # INTENTIONALLY VULNERABLE:
    # The application checks whether the user is logged in,
    # but does NOT check whether they are authorized
    # to access the requested profile_id.

    return render_template(
        "profile.html",
        profile=profile_data,
        profile_id=profile_id
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )