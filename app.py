from Flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def love_letter():
    return render_template("index.html")
    
if __name__ == "__main__"
app.run()