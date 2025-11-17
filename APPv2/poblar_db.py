from app import app
from models import *

def poblar_tablas():
    with app.app_context():
        print("Poblando tablas con datos")
        dispositivos = [
            Dispositivos(
                id_modelo="BFUA-6044",
                name="GoodLock", 
            ),
            Dispositivos(
                id_modelo="HKFA-3040", 
                name="SeC2000",
            ),
            Dispositivos(
                id_modelo="GEWF-6738",
                name="DobermanLock",
            ),
            Dispositivos(
                id_modelo="AAAA-0000",
                name="SmartLock2001",
            )
        ]
        
        for dispositivo in dispositivos:
            db.session.add(dispositivo)
        db.session.commit()
        print(f"{len(dispositivos)} dispositivos creados")
        
        # 2. Poblar Usuarios
        usuarios = [
            Usuarios(
                email="ana.garcia@example.com",
                nombre="Ana",
                apellido="García",
                telefono="+17879244706",
                password_hash="scrypt:32768:8:1$BBGFaOk5iORnOZpN$95407822abca166a6d0283a24459c3ad6b785d78e7721f080bd473d184a744b96376439819e414ce66891adf54a827f642fd6a4131a553df1558a216ae38a8e9" #pizza
            ),
            Usuarios(
                email="carlos.lopez@example.com", 
                nombre="Carlos",
                apellido="López",
                telefono="+17879339771",
                password_hash="scrypt:32768:8:1$yxygOa30qdx59rpg$908161939fd54cc51e7e07501421af380dfe874b67a49c9962871c3be1b5dd6ebcb617dfc9213241816e35984a424858b149d35398e0282c474510509df885cd" #hola
            ),
            Usuarios(
                email="maria.rodriguez@example.com",
                nombre="María",
                apellido="Rodríguez", 
                telefono="+19398141712",
                password_hash="scrypt:32768:8:1$noesunhash"
            )
        ]
        
        for usuario in usuarios:
            db.session.add(usuario)
        db.session.commit()
        print(f"{len(usuarios)} usuarios creados")
        
        # 3. Poblar Relaciones iot_usuario
        # Obtener IDs de dispositivos y usuarios recién creados
        dispositivo1 = Dispositivos.query.filter_by(id_modelo="BFUA-6044").first()
        dispositivo2 = Dispositivos.query.filter_by(id_modelo="HKFA-3040").first()
        usuario1 = Usuarios.query.filter_by(email="ana.garcia@example.com").first()
        usuario2 = Usuarios.query.filter_by(email="carlos.lopez@example.com").first()
        
        relaciones = [
            iot_usuario(
                iot_id=dispositivo1.id, 
                usuario_id=usuario1.id, 
                codigo="48248648",
                encendido=True,
                estado="Bloqueado", 
                alias="Puerta Pricipal",
                bateria=89
            ),
            iot_usuario(
                iot_id=dispositivo2.id, 
                usuario_id=usuario1.id, 
                codigo="58948744", 
                encendido=True,
                estado="Desbloqueado",
                alias="Patio",
                bateria=90  
            ),
            iot_usuario(
                iot_id=dispositivo1.id, 
                usuario_id=usuario2.id, 
                codigo="26284686",
                encendido=True,
                estado="Bloqueado", 
                alias="Oficina de Jorge",
                bateria=100
            ),
        ]
        
        for relacion in relaciones:
            db.session.add(relacion)
        db.session.commit()
        print(f"{len(relaciones)} relaciones creadas")

        print(f"Dispositivos: {Dispositivos.query.count()}")
        print(f"Usuarios: {Usuarios.query.count()}") 
        print(f"Relaciones: {iot_usuario.query.count()}")

if __name__ == '__main__':
    poblar_tablas()
