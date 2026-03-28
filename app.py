import os
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv

# carregando as variáveis de ambiente do arquivo .env
load_dotenv()

# importa a instancia do banco
from models import db

# criando a aplicação Flask
app = Flask(__name__)

# configurando a string de conexão com o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Conecta o bd e as migrations com a aplicação
db.init_app(app)
migrate = Migrate(app, db)

# importando as rotas
from routes import bp
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)