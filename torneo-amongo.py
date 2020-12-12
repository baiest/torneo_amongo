import json
import gspread
from google.oauth2.service_account import Credentials

from flask import Flask
from flask import request, jsonify, render_template
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
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
    i = 11
    participante = {}
    datos = worksheet.get_all_values()
    print(datos[12][0])
    while flag:
        try:
            participante.update({datos[i][0] : int(datos[i][8])})
        except:
            flag = False
        i+=1
    print(participante)

    i=11 # numero en el excel
    if request.method == "POST":
        name = request.form['name']
        print(name)
        while datos[i][0] != name:
            i+=1    
        datos[i][1] = str(int(datos[i][1]) + 1)
        participante[name] +=1
        worksheet.update_cell(i+1, 2, str(int(datos[i][1])))
    
    listaLetra = datos[10][1:6]
    print(listaLetra)
    return render_template('index.html', tabla= participante, lista = list(participante.keys()), listaLetra = listaLetra)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5000)
