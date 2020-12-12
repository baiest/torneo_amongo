import json
import gspread
from google.oauth2.service_account import Credentials

from flask import Flask
from flask import request, jsonify, render_template

import operator
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

    # OBTENER TABLA DE DATOS
    datos = worksheet.get_all_values() 

    flag = True
    i = 12
    participante = {}
    while flag:
        try:
            participante.update({datos[i][0] : int(datos[i][9])})
        except:
            flag = False
        i+=1
    listaLetra = datos[11][1:6]

    info = []
    for a in range (1, 9):
        info.append(datos[a][1])

    i=12 # numero en el excel
    if request.method == "POST":
        name = request.form['name']
        punto = int(request.form['punto'])
        celda = int(request.form['celda'])
        while datos[i][0] != name:
            i+=1 
            print(datos[i][0],name)   
        datos[i][celda-1] = str(int(datos[i][celda-1]) + punto)
        participante[datos[i][0]] += punto
        worksheet.update_cell(i+1, celda, str(int(datos[i][celda-1])))
    
    ##ORDENAR PUESTOS
    orden = dict(sorted(participante.items(), key=operator.itemgetter(1), reverse=True))

    return render_template('index.html', tabla= participante, 
    lista = list(orden.keys()), listaLetra = listaLetra,
    info = info, orden= orden)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5000)
