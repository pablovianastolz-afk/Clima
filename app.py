from flask import Flask, render_template
import requests

app = Flask(__name__)

LAT = -23.55
LON = -46.63

def get_clima():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
        "&timezone=auto"
    )
    return requests.get(url).json()

@app.route("/")
def index():
    clima = get_clima()
    return render_template("index.html", clima=clima)

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/privacidade")
def privacidade():
    return render_template("privacidade.html")


    if __name__ == "__main__":
    app.run(host="0.0.0.0")
app.run(host="0.0.0.0", port=8080)
