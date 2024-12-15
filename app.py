import main
# save this as app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    main.main()
    return "Hello, World!"