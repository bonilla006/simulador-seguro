## Simulador IoT
**Simular un dispositivo IoT y su comunicacion con el servidor (y el mobile app?? maybe) implementado con python**
1. Importancia:
    - Actualmente son muchas las personas que utilizan IoT
    - Poca consiencia sobre las vulnerabilidades
    - ABUNDAR MAS
    - Interes personal

2. que necito saber?
    - como funciona un IoT
    - comunicacion entre IoT y Servidor/BD y Mobile app
    - como funciona el protocolo MQTT
    - referencias:
        - Software
            - https://upkeep.com/learning/how-iot-works/
            - https://www.leverege.com/iot-ebook/how-iot-systems-work
            - https://www.leverege.com/iot-ebook/iot-gateways
            - https://www.leverege.com/iot-ebook/iot-cloud-explained
            - https://stackoverflow.com/questions/32091826/how-iot-devices-connect-to-servers
            - http://www.steves-internet-guide.com/mqtt-python-beginners-course/
            - https://wtforms.readthedocs.io/en/3.0.x/
            - https://stackoverflow.com/questions/22084886/add-a-css-class-to-a-field-in-wtform
            - https://stackoverflow.com/questions/6262943/sqlalchemy-how-to-make-django-choices-using-sqlalchemy
            - https://stackoverflow.com/questions/10059345/sqlalchemy-unique-across-multiple-columns
            - https://www.emqx.com/en/blog/how-to-use-mqtt-in-flask
            - https://docs.python.org/3/library/hashlib.html#hashlib.sha256
            - https://stackoverflow.com/questions/49032927/how-to-exit-mqtt-forever-loop
            - https://iot.stackexchange.com/questions/5897/publish-mqtt-message-via-http-get
            - https://codepen.io/raubaca/pen/PZzpVe
            - https://stackoverflow.com/questions/13855111/how-can-i-convert-24-hour-time-to-12-hour-time

        - Hardware-Simulado
            - https://www.youtube.com/watch?v=ZLt_BqmmKKE&t=5s, DoorLock system
            - https://docs.wokwi.com/parts/wokwi-arduino-uno
            - https://docs.wokwi.com/parts/wokwi-membrane-keypad
            - https://arduinogetstarted.com/reference/library/servo-write
            - https://arduinogetstarted.com/reference/library/lcd-setcursor
            - https://docs.oyoclass.com/unoeditor/Libraries/keypad/
            - https://codebender.cc/library/Keypad#utility%2FKey.h, def de NO_KEY 
            - https://playground.arduino.cc/Code/Password/
            - https://www.youtube.com/watch?v=lEXQ9w1z7Aw, simulacion IoT en wokwi
            - https://iotbyhvm.ooo/how-to-simulate-an-iot-project-on-wokwi-with-mqtt-and-esp32/
            - http://pubsubclient.knolleary.net/api
            - http://pubsubclient.knolleary.net/api#setCallback
            - http://www.steves-internet-guide.com/using-arduino-pubsub-mqtt-client/
            - https://hackaday.io/project/159183-esp32-arduino-tutorial-mbed-tls-using-the-sha-256/details
            - https://mbed-tls.readthedocs.io/projects/api/en/development/api/file/md_8h/#_CPPv417mbedtls_md_updateP20mbedtls_md_context_tPKh6size_t
            - https://arduinojson.org/v7/tutorial/deserialization/

        - ataques
            - https://securitycafe.ro/2022/04/08/iot-pentesting-101-how-to-hack-mqtt-the-standard-for-iot-messaging/
            
        - CUANDO TERMINE APLICAR BLUEPRINT
            - https://medium.com/@technicalpanchayat18/modularize-your-flask-app-with-flask-blueprints-c27109e8e8cf



3. Implementacion:
    1. Estructura de BD
        - Tablas
            - Dispositivos (iot)
            - Usuarios (u)
            - iot_u
        - Relaciones
            - iot #--# u
    2. python para comunicacion entre IoT <-> Servidor <-> mobile app
    3. protocolo de comunicacion MQTT
    4. Simular cerradura_inteligente (GoodLock)
        - Funciones:
            - Registro:
                - si no has registrado tu email con un dispositivo
                - estos dispositivos estan creados previamente, debes ingresar un ID de dispositivo correcto
            - Make 2FA
            - ValidateCode
            - MakeMasterCode
            - MakeTempCode
                - guardar en un dicc tipo: {id_dispositivo:codigo_temp}
            - AdminMode: 
                - mande un comando o señal por el mobile app?
            - validar intentos:
                - var global y verificacion por intentos que me deje saber si\
                ya paso el limite de intentos
            -  PanicMode: 
                - si se paso el limite de intentos; se cierra la cerradura y se manda mensaje al servidor\
                    - solo puede descbloquear 
                        1. poner el master code
                        2. entrar a AdminMode
                        3. 
                - si se trata de apagar y prender la cerradura
            - enviar estados de la cerradura de forma periodica
            - enviar eventos:
                - fallido, pasar limite de eventos, bateria baja
    5. Simular comunicacion 
        - 


## Referencias Extras:
- Que es un IoT: <https://www.ibm.com/think/topics/internet-of-things>
- IoT en la medicina: <https://opensistemas.com/dispositivos-iot-en-medicina-ejemplos/>
- Comunicacion sincronica o asincronica: <https://www.geeksforgeeks.org/system-design/communication-protocols-in-system-design/>
- IoT gateway: <https://www.einfochips.com/blog/securing-iot-gateways/>
- https://www.reddit.com/r/flask/comments/etajkg/how_to_make_an_api_gateway_in_flask/
- https://python-adv-web-apps.readthedocs.io/en/latest/flask_forms.html
- http://www.steves-internet-guide.com/mqtt-python-beginners-course/
