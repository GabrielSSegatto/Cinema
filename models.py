from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# as pk integer são auto incrementais por padrão

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique= True, nullable=False)

class Filme(db.Model):
    __tablename__ = 'filmes'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)

class Sessao(db.Model):
    __tablename__ = 'sessoes'
    id = db.Column(db.Integer, primary_key=True)
    horario_data = db.Column(db.DateTime, nullable=False)
    is_dub = db.Column(db.Boolean, nullable=False) ## True para dublado, False para legendado

    filme_id = db.Column(db.Integer, db.ForeignKey('filmes.id'), nullable=False)
    sala_id = db.Column(db.Integer, db.ForeignKey('salas.id'), nullable=False)


class Assento(db.Model):
    __tablename__ = 'assentos'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), nullable=False)

    sala_id = db.Column(db.Integer, db.ForeignKey('salas.id'), nullable=False)
    
    
class Sala(db.Model):
    __tablename__ = 'salas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    tipo = db.Column(db.String(20), nullable=False) ## Ex: 2D, 3D, IMAX
    capacidade = db.Column(db.Integer, nullable=False)

    
class Reserva(db.Model):
    __tablename__ = 'reservas'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sessao_id = db.Column(db.Integer, db.ForeignKey('sessoes.id'), nullable=False)
    assento_id = db.Column(db.Integer, db.ForeignKey('assentos.id'), nullable=False)
    data_reserva = db.Column(db.DateTime, default=datetime.now, nullable=False)

