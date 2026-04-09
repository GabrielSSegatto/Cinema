from models import Sala, db, User, Sessao, Assento, Reserva, Filme

# ========== USUARIO ===========
class UserService:

    # Função para criar um novo usuário
    @staticmethod 
    def create_user(name, cpf):
        if not name or not cpf:
            raise ValueError("Nome e CPF são obrigatórios")
        
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("CPF deve conter exatamente 11 dígitos numéricos")
        
        existing_user = User.query.filter_by(cpf=cpf).first()
        if existing_user:
            raise ValueError("CPF já cadastrado")
        
        novo_usuario = User(name=name, cpf=cpf)
        db.session.add(novo_usuario)
        db.session.commit()
        return novo_usuario
    
    # Função para obter um usuário por ID
    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("Usuário não encontrado")
        return user
    
    # Função para obter todos os usuários
    @staticmethod
    def get_all_users():
        return User.query.all()
    
    # Função para deletar um usuário por ID e suas reservas associadas
    @staticmethod 
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("Usuário não encontrado")
        
        # Deletar reservas associadas ao usuário
        reservas = Reserva.query.filter_by(user_id=user_id).all()
        for reserva in reservas:
            db.session.delete(reserva)
        
        db.session.delete(user)
        db.session.commit()
        return True
    
    # Função para atualizar um usuário por ID
    @staticmethod
    def update_user(user_id, name=None, cpf=None):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("Usuário não encontrado")
        
        if name:
            user.name = name
        
        if cpf:
            if len(cpf) != 11 or not cpf.isdigit():
                raise ValueError("CPF deve conter exatamente 11 dígitos numéricos")
            
            existing_user = User.query.filter_by(cpf=cpf).first()
            if existing_user and existing_user.id != user_id:
                raise ValueError("CPF já cadastrado para outro usuário")
            
            user.cpf = cpf
        
        db.session.commit()
        return user

# ========== FILME ===========
class FilmeService:
    # Função para criar um novo filme
    @staticmethod
    def create_filme(titulo):
        if not titulo:
            raise ValueError("Título é obrigatório")
        
        novo_filme = Filme(titulo=titulo)
        db.session.add(novo_filme)
        db.session.commit()
        return novo_filme
    
    # Função para obter um filme por ID
    @staticmethod
    def get_filme_by_id(filme_id):
        filme = Filme.query.get(filme_id)
        if not filme:
            raise ValueError("Filme não encontrado")
        return filme
    
    # Função para obter todos os filmes
    @staticmethod
    def get_all_filmes():
        return Filme.query.all()
    
    # Função para deletar um filme por ID e suas sessões associadas
    @staticmethod
    def delete_filme(filme_id):
        filme = Filme.query.get(filme_id)
        if not filme:
            raise ValueError("Filme não encontrado")
        
        # Deletar sessões associadas ao filme
        sessoes = Sessao.query.filter_by(filme_id=filme_id).all()
        for sessao in sessoes:
            db.session.delete(sessao)
        
        db.session.delete(filme)
        db.session.commit()
        return True
    
    # Função para atualizar um filme por ID
    @staticmethod
    def update_filme(filme_id, titulo=None):
        filme = Filme.query.get(filme_id)
        if not filme:
            raise ValueError("Filme não encontrado")
        
        if titulo:
            filme.titulo = titulo
        
        db.session.commit()
        return filme
    
# ========== SESSAO ===========
class SessaoService:
    
    # Função para criar uma nova sessão
    @staticmethod
    def create_sessao(horario_data, is_dub, sala_id, filme_id):
        if not horario_data or is_dub is None or not sala_id  or not filme_id:
            raise ValueError("Todos os campos são obrigatórios") 
        
        filme_existente = Filme.query.get(filme_id)
        if not filme_existente:
            raise ValueError("Filme não encontrado")
        
        nova_sessao = Sessao(horario_data=horario_data, is_dub=is_dub, sala_id=sala_id, filme_id=filme_id)
        db.session.add(nova_sessao)
        db.session.commit()
        return nova_sessao
    
    # Função para obter uma sessão por ID
    @staticmethod
    def get_sessao_by_id(sessao_id):
        sessao = Sessao.query.get(sessao_id)
        if not sessao:
            raise ValueError("Sessão não encontrada")
        return sessao
    
    # Função para obter todas as sessões
    @staticmethod
    def get_all_sessoes():
        return Sessao.query.all()
    
    # Função para deletar uma sessão e suas reservas associadas
    @staticmethod
    def delete_sessao(sessao_id):
        sessao = Sessao.query.get(sessao_id)
        if not sessao:
            raise ValueError("Sessão não encontrada")
        
        # Deletar reservas associadas à sessão
        reservas = Reserva.query.filter_by(sessao_id=sessao_id).all()
        for reserva in reservas:
            db.session.delete(reserva)
        
        db.session.delete(sessao)
        db.session.commit()
        return True

    # Função para atualizar uma sessão por ID
    @staticmethod
    def update_sessao(sessao_id, horario_data=None, is_dub=None, sala_id=None, filme_id=None):
        sessao = Sessao.query.get(sessao_id)
        if not sessao:
            raise ValueError("Sessão não encontrada")
        
        if horario_data:
            sessao.horario_data = horario_data
        
        if is_dub is not None:
            sessao.is_dub = is_dub
        
        if sala_id:
            sala_existente = Sala.query.get(sala_id)
            if not sala_existente:
                raise ValueError("Sala não encontrada")
            sessao.sala_id = sala_id
        
        if filme_id:
            filme_existente = Filme.query.get(filme_id)
            if not filme_existente:
                raise ValueError("Filme não encontrado")
            sessao.filme_id = filme_id
        
        db.session.commit()
        return sessao

# ========== ASSENTO ===========
class AssentoService:
    # Função para criar um novo assento
    @staticmethod
    def create_assento(numero, sala_id):
        if not numero or not sala_id:
            raise ValueError("Número e ID da sala são obrigatórios")
        
        sala_existente = Sala.query.get(sala_id)
        if not sala_existente:
            raise ValueError("Sala não encontrada")
        
        novo_assento = Assento(numero=numero, sala_id=sala_id)
        db.session.add(novo_assento)
        db.session.commit()
        return novo_assento
    
    # Função para obter um assento por ID
    @staticmethod
    def get_assento_by_id(assento_id):
        assento = Assento.query.get(assento_id)
        if not assento:
            raise ValueError("Assento não encontrado")
        return assento

    # Função para obter todos os assentos
    @staticmethod
    def get_all_assentos():
        return Assento.query.all()
    
    # Função para deletar um assento por ID e suas reservas associadas
    @staticmethod
    def delete_assento(assento_id):
        assento = Assento.query.get(assento_id)
        if not assento:
            raise ValueError("Assento não encontrado")
        
        # Deletar reservas associadas ao assento
        reservas = Reserva.query.filter_by(assento_id=assento_id).all()
        for reserva in reservas:
            db.session.delete(reserva)
        
        db.session.delete(assento)
        db.session.commit()
        return True
    
    # Função para atualizar um assento por ID
    @staticmethod
    def update_assento(assento_id, numero=None, sala_id=None):
        assento = Assento.query.get(assento_id)
        if not assento:
            raise ValueError("Assento não encontrado")
        if numero:
            assento.numero = numero
        if sala_id:
            sala_existente = Sala.query.get(sala_id)
            if not sala_existente:
                raise ValueError("Sala não encontrada")
            assento.sala_id = sala_id
        db.session.commit()
        return assento  
    
# ========== SALA ===========
class SalaService:
    # Função para criar uma nova sala
    @staticmethod
    def create_sala(nome, tipo, capacidade):
        if not nome or not tipo or not capacidade:
            raise ValueError("Nome, tipo e capacidade são obrigatórios")
        
        nova_sala = Sala(nome=nome, tipo=tipo, capacidade=capacidade)
        db.session.add(nova_sala)
        db.session.commit()
        return nova_sala
    
    # Função para obter uma sala por ID
    @staticmethod
    def get_sala_by_id(sala_id):
        sala = Sala.query.get(sala_id)
        if not sala:
            raise ValueError("Sala não encontrada")
        return sala
    
    # Função para obter todas as salas
    @staticmethod
    def get_all_salas():
        return Sala.query.all()
    
    # Função para deletar uma sala por ID e suas sessões e assentos associados
    @staticmethod
    def delete_sala(sala_id):
        sala = Sala.query.get(sala_id)
        if not sala:
            raise ValueError("Sala não encontrada")
        
        # Deletar sessões associdas à sala
        sessoes = Sessao.query.filter_by(sala_id=sala_id).all()
        for sessao in sessoes:
            db.session.delete(sessao)

        # Deletar assentos associados à sala
        assentos = Assento.query.filter_by(sala_id=sala_id).all()
        for assento in assentos:
            db.session.delete(assento)

        db.session.delete(sala)
        db.session.commit()
        return True
    
    # Função para atualizar uma sala por ID
    @staticmethod
    def update_sala(sala_id, nome=None, tipo=None, capacidade=None):
        sala = Sala.query.get(sala_id)
        if not sala:
            raise ValueError("Sala não encontrada")
        if nome:
            sala.nome = nome
        if tipo:
            sala.tipo = tipo
        if capacidade:
            sala.capacidade = capacidade
        db.session.commit()
        return sala

# ========== RESERVA ===========
class ReservaService:
    # Função para criar uma nova reserva
    @staticmethod
    def create_reserva(user_id, sessao_id, assento_id):
        if not user_id or not sessao_id or not assento_id:
            raise ValueError("ID do usuário, sessão e assento são obrigatórios")
        
        user_existente = User.query.get(user_id)
        if not user_existente:
            raise ValueError("Usuário não encontrado")
        
        sessao_existente = Sessao.query.get(sessao_id)
        if not sessao_existente:
            raise ValueError("Sessão não encontrada")

        assento_existente = Assento.query.get(assento_id)
        if not assento_existente:
            raise ValueError("Assento não encontrado")
        
        reserva_existente = Reserva.query.filter_by(sessao_id=sessao_id, assento_id=assento_id).first()
        if reserva_existente:
            raise ValueError("Este assento já está reservado para esta sessão")

        nova_reserva = Reserva(user_id=user_id, sessao_id=sessao_id, assento_id=assento_id)
        db.session.add(nova_reserva)
        db.session.commit()
        return nova_reserva

    # Função para obter uma reserva por ID
    @staticmethod
    def get_reserva_by_id(reserva_id):
        reserva = Reserva.query.get(reserva_id)
        if not reserva:
            raise ValueError("Reserva não encontrada")
        return reserva

    # Função para obter todas as reservas
    @staticmethod
    def get_all_reservas():
        return Reserva.query.all()

    # Função para deletar uma reserva por ID
    @staticmethod
    def delete_reserva(reserva_id):
        reserva = Reserva.query.get(reserva_id)
        if not reserva:
            raise ValueError("Reserva não encontrada")
        
        db.session.delete(reserva)
        db.session.commit()
        return True

    # Função para atualizar uma reserva por ID
    @staticmethod
    def update_reserva(reserva_id, user_id=None, sessao_id=None, assento_id=None):
        reserva = Reserva.query.get(reserva_id)
        if not reserva:
            raise ValueError("Reserva não encontrada")
        
        if user_id:
            user_existente = User.query.get(user_id)
            if not user_existente:
                raise ValueError("Usuário não encontrado")
            reserva.user_id = user_id
        
        if sessao_id:
            sessao_existente = Sessao.query.get(sessao_id)
            if not sessao_existente:
                raise ValueError("Sessão não encontrada")
            reserva.sessao_id = sessao_id

        if assento_id:
            assento_existente = Assento.query.get(assento_id)
            if not assento_existente:
                raise ValueError("Assento não encontrado")
            reserva.assento_id = assento_id

        db.session.commit()
        return reserva  
