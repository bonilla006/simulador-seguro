from flask import Flask, render_template
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', num=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)