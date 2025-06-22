from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def love_letter():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # default to 5000 for local
    app.run(host='0.0.0.0', port=port)    
 
