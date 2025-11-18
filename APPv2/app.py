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
    apellido = StringField(label="Apellido")
    telefono = StringField(label="Telefono")
    passw = PasswordField(label="Contraseña")
    
    def validate_telefono(self, telefono):
        try:
            tel = phonenumbers.parse(telefono.data)
            if not phonenumbers.is_valid_number(tel):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Numero de telefono invalido')
                  
class NuevoDispositivo(FlaskForm):
    id_modelo = StringField(label="Modelo")
    codigo = StringField(label="Codigo_Master")
    nombre = StringField(label="Nombre")

    def validate_id_modelo(self, id_modelo):
        #verificar que tenga -
        mitad = len(id_modelo.data)//2
        if id_modelo.data[mitad] != "-":
            raise ValidationError('El formato del id es: AAAA-1234')
        
        #separa el texto y lo numerico
        texto, numero = id_modelo.data.split("-")

        if not texto.isupper():
            raise ValidationError('Deben ser mayusculas')
        
        if len(texto) != 4 or len(numero) != 4:
            raise ValidationError('El id debe ser de 8 carcateres')
    
        if not texto.isalpha():
            raise ValidationError('los primeros 4 caracteres deben ser letras')
        
        if not numero.isdigit():
            raise ValidationError('los ultimos 4 caracteres deben ser numeros')
    
    def validate_codigo(self, codigo):
        if not codigo.data.isdigit():
            raise ValidationError('El codigo debe ser numerico')
        
        if len(codigo.data) < 4:
            raise ValidationError('Minimo 5 digitos')

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
        print("Error en Panel_Control:", err)

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
            print("Error en Bloquear_Dispositivo:", err)

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
            print("Error en Desbloquear_Dispositivo:", err)

        #actualizar el estado del dispositivo de bloqueado a desbloqueado
        dispositivo.estado = "Desbloqueado"
        db.session.commit()
        
        #volver al panel principal
        return redirect(url_for('Panel_Control'))
    else:
        print("metodo incorrecto")
        return redirect(url_for('Panel_Control'))

@app.route('/panel-principal/nuevo-dispositivo/', methods=['GET', 'POST'])
def Nuevo_Dispositivo():
    form = NuevoDispositivo()

    if request.method == "POST":
        if form.validate_on_submit():
            #conseguir al usuario y el dispositivo
            try:    
                u_id = Usuarios.query.get(current_user.id)
                d_id = Dispositivos.query.filter_by(id_modelo=form.id_modelo.data).first()
            except Exception as err:
                print("Error al buscar data de usuario o dispositivo:", err)
            
            print(":", u_id, d_id)
            relacion = iot_usuario.query.filter_by(usuario_id=u_id.id, iot_id=d_id.id).all()
            if not relacion:
                nuevo_dispositivo = iot_usuario(
                    iot_id=d_id.id, 
                    usuario_id=u_id.id, 
                    codigo=form.codigo.data,
                    encendido=True,
                    estado="Desbloqueado", 
                    alias=form.nombre.data,
                    bateria=100
                )
                db.session.add(nuevo_dispositivo)
                db.session.commit()
                return redirect(url_for('Panel_Control'))
            else:
                print("ya tiene conectado este dispositivo")
                return redirect(url_for('Nuevo_Dispositivo'))
        else:
            print("error en Nuevo_Dispositivo:",form.errors)
            
    return render_template('nuevo_dispositivo.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)