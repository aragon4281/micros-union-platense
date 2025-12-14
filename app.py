from flask import Flask, render_template
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import re

app = Flask(__name__)

URL = "https://cuandollega.smartmovepro.net/unionplatense"

def obtener_datos():
    resultado = {
        "hora": datetime.now().strftime("%H:%M"),
        "273": None,
        "520": None
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, timeout=60000)
        page.wait_for_timeout(8000)

        texto = page.inner_text("body").lower()
        browser.close()

    mins = re.findall(r"(\d+)\s*min", texto)

    if mins:
        ahora = datetime.now()
        resultado["273"] = {
            "min": mins[0],
            "llega": (ahora + timedelta(minutes=int(mins[0]))).strftime("%H:%M")
        }

        if len(mins) > 1:
            resultado["520"] = {
                "min": mins[1],
                "llega": (ahora + timedelta(minutes=int(mins[1]))).strftime("%H:%M")
            }

    return resultado


@app.route("/")
def index():
    datos = obtener_datos()
    return render_template("index.html", datos=datos)


if __name__ == "__main__":
    app.run()
