from app import app
from models import db, User, Filme, Sessao, Assento, Sala, Reserva
from datetime import datetime, timedelta

def popular_banco():
    with app.app_context():
        # Verificação de segurança: se já tiver usuário, não roda de novo para não dar erro de CPF duplicado
        if User.query.first():
            print("⚠️ O banco já possui dados! Limpe o banco antes de rodar o seed novamente.")
            return

        print("Enchendo o tanque do banco de dados...")

        # 1. Criando as Salas
        sala1 = Sala(nome="Sala 01", tipo="IMAX", capacidade=10)
        sala2 = Sala(nome="Sala 02", tipo="3D", capacidade=10)
        db.session.add_all([sala1, sala2])
        db.session.commit() # Precisa commitar aqui para as salas ganharem um ID (sala1.id)

        # 2. Criando os Assentos (Gerando A1 até A10 para a Sala 1 e B1 a B10 para Sala 2)
        print("Instalando os assentos...")
        assentos = []
        for i in range(1, 11):
            assentos.append(Assento(numero=f"A{i}", sala_id=sala1.id))
            assentos.append(Assento(numero=f"B{i}", sala_id=sala2.id))
        db.session.add_all(assentos)

        # 3. Criando os Filmes
        filme1 = Filme(titulo="Matrix")
        filme2 = Filme(titulo="O Senhor dos Anéis")
        db.session.add_all([filme1, filme2])
        db.session.commit()

        # 4. Criando as Sessões (Jogando as datas para amanhã e depois de amanhã)
        hoje = datetime.now()
        sessao1 = Sessao(
            horario_data=hoje + timedelta(days=1, hours=2), 
            is_dub=False, 
            filme_id=filme1.id, 
            sala_id=sala1.id
        )
        sessao2 = Sessao(
            horario_data=hoje + timedelta(days=2, hours=5), 
            is_dub=True, 
            filme_id=filme2.id, 
            sala_id=sala2.id
        )
        db.session.add_all([sessao1, sessao2])
        db.session.commit()

        # 5. Criando os Usuários
        user1 = User(name="João Gabriel", cpf="12345678901")
        user2 = User(name="Gabriel Soares", cpf="10987654321")
        db.session.add_all([user1, user2])
        db.session.commit()

        # 6. Criando uma Reserva (O João vai reservar o Assento A1 para Matrix)
        primeiro_assento = Assento.query.filter_by(sala_id=sala1.id).first()
        reserva1 = Reserva(user_id=user1.id, sessao_id=sessao1.id, assento_id=primeiro_assento.id)
        db.session.add(reserva1)
        db.session.commit()

        print("✅ Banco populado com sucesso! ")

if __name__ == '__main__':
    popular_banco()