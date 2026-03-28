from flask import Blueprint, request, jsonify
from models import Assento, Sessao, db, User, Filme, Reserva

# criando o blueprint 
bp = Blueprint('api', __name__)

# Mini guia de status code:
#
# 201 - Created: Recurso criado com sucesso
# 400 - Bad Request: Erro de validação dos dados de entrada
# 404 - Not Found: Recurso não encontrado

#==========================================
# USUARIO
# =========================================

# rota para criar um novo usuário
@bp.route('/users', methods=['POST'])
def create_user():

    # obtendo os dados do corpo da requisição
    dados = request.get_json()

    # validação dos dados de entrada
    if not dados or not 'name' in dados or not 'cpf' in dados:
        return jsonify({'error': 'Nome e CPF são obrigatórios'}), 400
    
    # verificando se o CPF já está cadastrado
    usuario_existente = User.query.filter_by(cpf=dados['cpf']).first()
    if usuario_existente:
        return jsonify({'error': 'CPF já cadastrado'}), 400
    
    # caso os dados sejam válidos, cria o usuário
    novo_usuario = User(name=dados['name'], cpf=dados['cpf'])
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({"mensagem": "Usuário criado com sucesso!", "id": novo_usuario.id}), 201

# rota para listar todos os usuários
@bp.route('/usuarios', methods=['GET'])
def get_users():
    # consulta todos os usuários no banco de dados
    usuarios = User.query.all()
    
    # converte os objetos User em dicionários para retornar como JSON
    lista_usuarios = [{"id": u.id, "name": u.name, "cpf": u.cpf} for u in usuarios]

    return jsonify(lista_usuarios), 200


#Rota para atualizar um usuário
@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # consulta o usuário pelo ID
    usuario = User.query.get(user_id)

    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    # obtendo os dados do corpo da requisição
    dados = request.get_json()

    # validação dos dados de entrada
    if not dados or not 'name' in dados or not 'cpf' in dados:
        return jsonify({'error': 'Nome e CPF são obrigatórios'}), 400
    
    # verificando se o CPF já está cadastrado para outro usuário
    usuario_existente = User.query.filter_by(cpf=dados['cpf']).first()
    if usuario_existente and usuario_existente.id != user_id:
        return jsonify({'error': 'CPF já cadastrado para outro usuário'}), 400
    
    # atualiza os campos do usuário
    usuario.name = dados['name']
    usuario.cpf = dados['cpf']
    
    db.session.commit()

    return jsonify({"mensagem": "Usuário atualizado com sucesso!"}), 200    


#Rota para deletar um usuário
@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # consulta o usuário pelo ID
    usuario = User.query.get(user_id)

    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    # deleta o usuário do banco de dados
    db.session.delete(usuario)
    db.session.commit()

    return jsonify({'mensagem': 'Usuário deletado com sucesso'}), 200

#==========================================
# FILME
# =========================================

# rota para criar um novo filme
@bp.route('/filmes', methods=['POST'])
def create_filme():

    # obtendo os dados do corpo da requisição
    dados = request.get_json()

    # validação dos dados de entrada
    if not dados or not 'titulo' in dados:
        return jsonify({'error': 'Título é obrigatório'}), 400
    
    # caso os dados sejam válidos, cria o filme
    novo_filme = Filme(titulo=dados['titulo'])
    db.session.add(novo_filme)
    db.session.commit()

    return jsonify({"mensagem": "Filme criado com sucesso!", "id": novo_filme.id}), 201

# rota para listar todos os filmes
@bp.route('/filmes', methods=['GET'])
def get_filmes():
    # consulta todos os filmes no banco de dados
    filmes = Filme.query.all()
    
    # converte os objetos Filme em dicionários para retornar como JSON
    lista_filmes = [{"id": f.id, "titulo": f.titulo} for f in filmes]

    return jsonify(lista_filmes), 200

#Rota para atualizar um filme
@bp.route('/filmes/<int:filme_id>', methods=['PUT'])
def update_filme(filme_id):
    # consulta o filme pelo ID
    filme = Filme.query.get(filme_id)

    if not filme:
        return jsonify({'error': 'Filme não encontrado'}), 404
    
    # obtendo os dados do corpo da requisição
    dados = request.get_json()

    # validação dos dados de entrada
    if not dados or not 'titulo' in dados:
        return jsonify({'error': 'Título é obrigatório'}), 400
    
    # atualiza os campos do filme
    filme.titulo = dados['titulo']
    
    db.session.commit()

    return jsonify({"mensagem": "Filme atualizado com sucesso!"}), 200

#Rota para deletar um filme
@bp.route('/filmes/<int:filme_id>', methods=['DELETE'])
def delete_filme(filme_id):
    # consulta o filme pelo ID
    filme = Filme.query.get(filme_id)

    if not filme:
        return jsonify({'error': 'Filme não encontrado'}), 404
    
    # deleta o filme do banco de dados
    db.session.delete(filme)
    db.session.commit()

    return jsonify({'mensagem': 'Filme deletado com sucesso'}), 200


#==========================================
# Sessão
# =========================================

# Rota para criar uma nova sessão
@bp.route('/sessoes', methods=['POST'])
def create_sessao():

    dados = request.get_json()

    # validação dos dados de entrada
    if not dados or not 'horario_data' in dados or not 'is_dub' in dados or not 'sala' in dados or not 'filme_id' in dados:
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400
    
    # verificando se o filme existe
    filme = Filme.query.get(dados['filme_id'])
    if not filme:
        return jsonify({'error': 'Filme não encontrado'}), 404
    
    # caso os dados sejam válidos, cria a sessão
    nova_sessao = Sessao(
        horario_data=dados['horario_data'],
        is_dub=dados['is_dub'],
        sala=dados['sala'],
        filme_id=dados['filme_id']
    )
    db.session.add(nova_sessao)
    db.session.commit()
    
    return jsonify({"mensagem": "Sessão criada com sucesso!", "id": nova_sessao.id}), 201

# Rota para listar todas as sessões
@bp.route('/sessoes', methods=['GET'])
def get_sessoes():
    sessoes = Sessao.query.all()

    lista_sessoes = []
    for s in sessoes:
        filme = Filme.query.get(s.filme_id)
        lista_sessoes.append({
            "id": s.id,
            "horario_data": s.horario_data.isoformat(),
            "is_dub": s.is_dub,
            "sala": s.sala,
            "filme": {
                "id": filme.id,
                "titulo": filme.titulo
            }
        })
    return jsonify(lista_sessoes), 200

# Rota para atualizar uma sessão
@bp.route('/sessoes/<int:sessao_id>', methods=['PUT'])
def update_sessao(sessao_id):
    sessao = Sessao.query.get(sessao_id)

    if not sessao:
        return jsonify({'error': 'Sessão não encontrada'}), 404
    
    dados = request.get_json()

    # validação dos dados de entrada
    if not dados or not 'horario_data' in dados or not 'is_dub' in dados or not 'sala' in dados or not 'filme_id' in dados:
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400
    
    # verificando se o filme existe
    filme = Filme.query.get(dados['filme_id'])
    if not filme:
        return jsonify({'error': 'Filme não encontrado'}), 404
    
    # atualiza os campos da sessão
    sessao.horario_data = dados['horario_data']
    sessao.is_dub = dados['is_dub']
    sessao.sala = dados['sala']
    sessao.filme_id = dados['filme_id']
    
    db.session.commit()

    return jsonify({"mensagem": "Sessão atualizada com sucesso!"}), 200

# Rota para deletar uma sessão
@bp.route('/sessoes/<int:sessao_id>', methods=['DELETE'])
def delete_sessao(sessao_id):
    sessao = Sessao.query.get(sessao_id)

    if not sessao:
        return jsonify({'error': 'Sessão não encontrada'}), 404
    
    db.session.delete(sessao)
    db.session.commit()

    return jsonify({'mensagem': 'Sessão deletada com sucesso'}), 200

#==========================================
# Assento
# =========================================

# Rota para criar um novo assento
@bp.route('/assentos', methods=['POST'])
def create_assento():

    dados = request.get_json()

    # validação dos dados de entrada
    if not dados or not 'numero' in dados or not 'sessao_id' in dados:
        return jsonify({'error': 'Número e ID da sessão são obrigatórios'}), 400
    
    # verificando se a sessão existe
    sessao = Sessao.query.get(dados['sessao_id'])
    if not sessao:
        return jsonify({'error': 'Sessão não encontrada'}), 404
    
    # verificando se o número do assento já está cadastrado para a sessão
    assento_existente = Assento.query.filter_by(numero=dados['numero'], sessao = dados['sessao_id']).first()
    if assento_existente:
        return jsonify({'error': 'Número do assento já cadastrado para esta sessão'}), 400
    
    # caso os dados sejam válidos, cria o assento

    novo_assento = Assento(
        numero=dados['numero'],
        sessao_id=dados['sessao_id']
    )
    db.session.add(novo_assento)
    db.session.commit()

    return jsonify({"mensagem": "Assento criado com sucesso!", "id": novo_assento.id}), 201

# Rota para listar assentos de uma sessão
@bp.route('/sessoes/<int:sessao_id>/assentos', methods=['GET'])
def get_assentos(sessao_id):
    # verificando se a sessão existe
    sessao = Sessao.query.get(sessao_id)
    if not sessao:
        return jsonify({'error': 'Sessão não encontrada'}), 404
    
    assentos = Assento.query.filter_by(sessao_id=sessao_id).all()

    lista_assentos = [{"id": a.id, "numero": a.numero} for a in assentos]

    return jsonify(lista_assentos), 200

# Rota para deletar um assento
@bp.route('/assentos/<int:assento_id>', methods=['DELETE'])
def delete_assento(assento_id):
    assento = Assento.query.get(assento_id) 
    if not assento:
        return jsonify({'error': 'Assento não encontrado'}), 404
    db.session.delete(assento)
    db.session.commit()

    return jsonify({'mensagem': 'Assento deletado com sucesso'}), 200

#==========================================
# Reserva
# =========================================

#cria uma reserva
@bp.route('/reservas', methods=['POST'])
def create_reserva():
    # obtendo os dados do corpo da requisição
    dados = request.get_json()

    # validação dos dados de entrada
    if not dados or not 'user_id' in dados or not 'sessao_id' in dados or not 'assento_id' in dados:
        return jsonify({'error': 'ID do usuário, ID da sessão e ID do assento são obrigatórios'}), 400
    
    #verificando se o usuário existe
    usuario = User.query.get(dados['user_id'])
    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    #verificando se a sessão existe
    sessao = Sessao.query.get(dados['sessao_id'])
    if not sessao:
        return jsonify({'error': 'Sessão não encontrada'}), 404
    
    #verificando se o assento existe nessa sessão
    assento = Assento.query.filter_by(id=dados['assento_id'], sessao_id=dados['sessao_id']).first()
    if not assento: 
        return jsonify({'error': 'Assento não encontrado para esta sessão'}), 404
    
    #verificando se o assento já está reservado
    reserva_existente = Reserva.query.filter_by(assento_id=dados['assento_id']).first()
    if reserva_existente:
        return jsonify({'error': 'Assento já reservado'}), 400
    
    # caso os dados sejam válidos, cria a reserva
    nova_reserva = Reserva(
        user_id=dados['user_id'],
        sessao_id=dados['sessao_id'],
        assento_id=dados['assento_id']
    )

    db.session.add(nova_reserva)
    db.session.commit()

    return jsonify({"mensagem": "Reserva criada com sucesso!", "id": nova_reserva.id}), 201

# Listar todas reservas de uma sessão
@bp.route('/sessoes/<int:sessao_id>/reservas', methods=['GET'])
def get_reservas(sessao_id):

    # verificar se a sessao existe
    sessao = Sessao.query.get(sessao_id)
    if not sessao:
        return jsonify({'error': 'Sessão não encontrada'}), 404
    
    reservas = Reserva.query.filter_by(sessao_id=sessao_id).all()

    lista_reservas = [{"id": r.id, "user_id": r.user_id, "assento_id": r.assento_id, "data_reserva": r.data_reserva.isoformat()} for r in reservas]

    return jsonify(lista_reservas), 200

# deletar uma reserva
@bp.route('/reservas/<int:reserva_id>', methods=['DELETE'])
def delete_reserva(reserva_id):
    reserva = Reserva.query.get(reserva_id) 
    if not reserva:
        return jsonify({'error': 'Reserva não encontrada'}), 404
    db.session.delete(reserva)
    db.session.commit()

    return jsonify({'mensagem': 'Reserva deletada com sucesso'}), 200

# Rota para atualizar uma reserva
@bp.route('/reservas/<int:reserva_id>', methods=['PUT'])
def update_reserva(reserva_id):
    reserva = Reserva.query.get(reserva_id) 
    if not reserva:
        return jsonify({'error': 'Reserva não encontrada'}), 404
    
    dados = request.get_json()

    # validação dos dados de entrada
    if not dados or not 'user_id' in dados or not 'sessao_id' in dados or not 'assento_id' in dados:
        return jsonify({'error': 'ID do usuário, ID da sessão e ID do assento são obrigatórios'}), 400
    
    #verificando se o usuário existe
    usuario = User.query.get(dados['user_id'])
    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    #verificando se a sessão existe
    sessao = Sessao.query.get(dados['sessao_id'])

    #verificando se o assento existe nessa sessão
    assento = Assento.query.filter_by(id=dados['assento_id'], sessao_id=dados['sessao_id']).first()
    if not assento: 
        return jsonify({'error': 'Assento não encontrado para esta sessão'}), 404
    #verificando se o assento já está reservado por outra reserva
    reserva_existente = Reserva.query.filter_by(assento_id=dados['assento_id']).first()
    if reserva_existente and reserva_existente.id != reserva_id:
        return jsonify({'error': 'Assento já reservado por outra reserva'}), 400
    
    # atualiza os campos da reserva
    reserva.user_id = dados['user_id']
    reserva.sessao_id = dados['sessao_id']
    reserva.assento_id = dados['assento_id']
    db.session.commit()

    return jsonify({'mensagem': 'Reserva atualizada com sucesso'}), 200

# listar reservas de um usuário
@bp.route('/users/<int:user_id>/reservas', methods=['GET'])
def get_reservas_usuario(user_id):
    # verificar se o usuário existe
    usuario = User.query.get(user_id)
    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    reservas = Reserva.query.filter_by(user_id=user_id).all()

    lista_reservas = []
    for r in reservas:
        sessao = Sessao.query.get(r.sessao_id)
        filme = Filme.query.get(sessao.filme_id)
        lista_reservas.append({
            "id": r.id,
            "sessao": {
                "id": sessao.id,
                "horario_data": sessao.horario_data.isoformat(),
                "is_dub": sessao.is_dub,
                "sala": sessao.sala,
                "filme": {
                    "id": filme.id,
                    "titulo": filme.titulo
                }
            },
            "assento_id": r.assento_id,
            "data_reserva": r.data_reserva.isoformat()
        })     
    return jsonify(lista_reservas), 200
