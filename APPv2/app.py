from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm, CSRFProtect
from flask_wtf.csrf import generate_csrf
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import *
import phonenumbers

#CORE 
app = Flask(__name__)
#cargar configuraciones
app.config.from_object(Config)
# Inicializar y crear la base de datos
crear_bd(app)
login_manager = LoginManager(app)

#para formularios
csrf = CSRFProtect(app)
#FORMULARIOS
#Inicio de seccion
class ValidarUsuario(FlaskForm):
    email = StringField(label="Email", render_kw={"placeholder":"Ingrese su correo electronico"},validators=[Email(), InputRequired(), Length(10, 50)])
    passw = PasswordField(label="Contraseña", render_kw={"placeholder":"Ingrese su contraseña"})

class CrearUsuario(FlaskForm):
    email = StringField(label="Email", validators=[Email(), InputRequired(), Length(10, 50)])
    nombre = StringField(label="Nombre")
    apellido =StringField(label="Apellido")
    telefono =StringField(label="Telefono")
    passw = PasswordField(label="Contraseña")
    
    def validate_telefono(self, telefono):
        try:
            tel = phonenumbers.parse(telefono.data)
            if not phonenumbers.is_valid_number(tel):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')
                  

#ENDPOINTS
@login_manager.user_loader
def load_user(id_usuario):
    return Usuarios.query.get(id_usuario)

@app.route('/crear-cuenta/', methods=['GET', 'POST'])
def Crear_Cuenta():
    form = CrearUsuario()

    if request.method == "POST":
        if form.validate_on_submit():
            exists = db.session.query(db.exists().where(Usuarios.email==form.email.data)).scalar()
            if not exists:
                nuevo_usuario = Usuarios(
                    email=form.email.data,
                    nombre=form.nombre.data,
                    apellido=form.apellido.data,
                    telefono=form.telefono.data,
                    password_hash=generate_password_hash(form.passw.data)
                )
                db.session.add(nuevo_usuario)
                db.session.commit()
                return redirect(url_for('Inicio'))
            else:
                print("este email ya existe")
                return redirect(url_for('Crear_Cuenta'))
        else:
            print("form invalido")
            
    return render_template('crear_cuenta.html', form=form)

@app.route('/inicio/', methods=['GET', 'POST'])
def Inicio():
    #para request POST
    form = ValidarUsuario()
    if request.method == 'POST':
        if form.validate_on_submit():
            #verificar si el usuario existe en la BD
            #variable bool para saber
            exists = db.session.query(db.exists().where(Usuarios.email==form.email.data)).scalar()
            if exists:
                info_usuario = Usuarios.query.filter_by(email=form.email.data).first()

                # autenticar el usuario
                if check_password_hash(info_usuario.password_hash, form.passw.data):
                    login_user(info_usuario)
                    return redirect(url_for('Panel_Control'))

                else:
                    print("mala contraseña")
                    return redirect(url_for('Inicio'))
            else:
                print("Usted no tiene una cuenta")
        else:
            print("form invalido")
    #para request GET
    return render_template('inicio.html', form=form)

#Panel principal para manejar los dispositivos
@app.route('/panel-principal/', methods=['GET'])
@login_required
def Panel_Control():
    # conseguir los dispositivos del usuario
    try:
        info_IoT = iot_usuario.query.filter_by(usuario_id=current_user.id).all()
    except Exception as err:
        print("Error general:", err)

    mycsrf=generate_csrf()

    if info_IoT:
        context = [{
            'id':info.id,
            'nombre':info.alias if info.alias else info.name,
            # 'encendido':info.encendido,
            'estado':info.estado.value,
            'carga':info.bateria,
        } for info in info_IoT]
    else:
        context= []
        
    return render_template('panel_principal.html', context=context, csrf=mycsrf)

@app.route('/panel-principal/lock/<int:rel_id>/', methods=['POST'])
@login_required
def Bloquear_Dispositivo(rel_id):
    if request.method == "POST":
        #conseguir el id del record iot-usuario
        try:
            dispositivo = iot_usuario.query.get(rel_id) 
        except Exception as err:
            print("Error general:", err)

        #actualizar el estado del dispositivo de desbloqueado a bloqueado
        dispositivo.estado = "Bloqueado"
        db.session.commit()

        #volver al panel principal
        return redirect(url_for('Panel_Control'))
    else:
        print("metodo incorrecto")
        return redirect(url_for('Panel_Control'))
    
@app.route('/panel-principal/unlock/<int:rel_id>/', methods=['POST'])
@login_required
def Desbloquear_Dispositivo(rel_id):
    if request.method == "POST":
        #conseguir el id del record iot-usuario
        try:
            dispositivo = iot_usuario.query.get(rel_id) 
        except Exception as err:
            print("Error general:", err)

        #actualizar el estado del dispositivo de bloqueado a desbloqueado
        dispositivo.estado = "Desbloqueado"
        db.session.commit()
        
        #volver al panel principal
        return redirect(url_for('Panel_Control'))
    else:
        print("metodo incorrecto")
        return redirect(url_for('Panel_Control'))


if __name__ == "__main__":
    app.run(debug=True)