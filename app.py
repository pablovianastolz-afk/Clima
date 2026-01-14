from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def buscar_clima(cidade):
    geo = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={cidade}&count=1"
    ).json()

    if "results" not in geo:
        return None, None

    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]

    clima = requests.get(
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
        f"&timezone=auto"
    ).json()

    elev = requests.get(
        f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    ).json()

    elevacao = elev["results"][0]["elevation"]

    return clima, elevacao


@app.route("/", methods=["GET", "POST"])
def index():
    clima = None
    elevacao = None

    if request.method == "POST":
        cidade = request.form["cidade"]
        clima, elevacao = buscar_clima(cidade)

    return render_template("index.html", clima=clima, elevacao=elevacao)


@app.route("/clima/<cidade>")
def clima_cidade(cidade):
    clima, elevacao = buscar_clima(cidade)
    return render_template("index.html", clima=clima, elevacao=elevacao)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
