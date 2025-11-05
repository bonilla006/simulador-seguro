from flask import Flask, render_template

app = Flask(__name__)
@app.route('/cliente/inicio/')
def InicioSeccion():
    #Post

    return render_template('inicio_seccion.html')

@app.route('/cliente/demo')
def crear_CodigoMaestro():
    codigo_maestro = "6416245"
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003, debug=True)