import json
import gspread
from google.oauth2.service_account import Credentials

from flask import Flask
from flask import request, jsonify, render_template
app = Flask(__name__)


def tabla():
    scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]

    credentials = Credentials.from_service_account_file(
        './Torneo amongo-fd9d4659f7dd.json',
        scopes=scopes
    )

    gc = gspread.authorize(credentials)

    sh = gc.open("Torneo Amongo")
    worksheet = sh.get_worksheet(0)


    flag = True
    i = 12
    participantes = []
    while flag:
        nombre = worksheet.cell(i, 1).value
        punto = worksheet.cell(i, 9).value
        if nombre != "":
            persona = {nombre : punto}
            participantes.append(persona)
            print(persona)
        else:
            flag = False
        i+=1
    print(participantes)
    return jsonify(participantes)

@app.route('/')
def index():
    participantes = tabla()
    return render_template('./public/index.html')
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5000)
