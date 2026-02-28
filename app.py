from flask import Flask, render_template, request
import random
import string
from zxcvbn import zxcvbn

app = Flask(__name__)

def generate_password(length, upper, lower, digits, symbols):
    characters = ""
    if upper:
        characters += string.ascii_uppercase
    if lower:
        characters += string.ascii_lowercase
    if digits:
        characters += string.digits
    if symbols:
        characters += string.punctuation

    if not characters:
        return ""

    return ''.join(random.choice(characters) for _ in range(length))

@app.route("/", methods=["GET", "POST"])
def index():
    password = ""
    strength_score = None

    if request.method == "POST":
        length = int(request.form.get("length", 12))
        upper = "upper" in request.form
        lower = "lower" in request.form
        digits = "digits" in request.form
        symbols = "symbols" in request.form

        password = generate_password(length, upper, lower, digits, symbols)

        if password:
            result = zxcvbn(password)
            strength_score = result["score"]

    return render_template("index.html",
                           password=password,
                           strength_score=strength_score)

if __name__ == "__main__":
    app.run(debug=True)
