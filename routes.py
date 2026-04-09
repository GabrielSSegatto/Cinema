from flask import Blueprint, request, jsonify
from models import Assento, Sessao, db, User, Filme, Reserva
from services import UserService, FilmeService, SessaoService, AssentoService, SalaService, ReservaService

# criando o blueprint 
bp = Blueprint('api', __name__)

# Mini guia de status code:
#
# 201 - Created: Recurso criado com sucesso
# 400 - Bad Request: Erro de validação dos dados de entrada
# 404 - Not Found: Recurso não encontrado
# 500 - Internal Server Error: Erro inesperado no servidor

#==========================================
# USUARIO
# =========================================
# Endpoint para criar um novo usuário

@bp.route('/users', methods=['POST'])
def create_user():
    dados = request.get_json()

    if not dados or 'name' not in dados or 'cpf' not in dados:
        return jsonify({'error': 'Dados incompletos'}), 400
    
    try:
        novo_usuario = UserService.create_user(
            name=dados.get('name'),
            cpf=dados.get('cpf')
        )

        return jsonify({
            "mensagem": "Usuário criado com sucesso",
            "usuario": {
                "id": novo_usuario.id,
                "name": novo_usuario.name,
                "cpf": novo_usuario.cpf
            }   
        }), 201
    
    except ValueError as e:
        # erros de validação, como CPF inválido ou já existente, serão capturados aqui
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        # erro genérico para capturar outros tipos de erros inesperados
        return jsonify({"error": "Erro interno do servidor"}), 500
    
# Endpoint para listar todos os usuários
@bp.route('/users', methods=['GET'])
def get_users():

    usuarios = UserService.get_all_users()

    lista_usuarios = [
        {
            "id": u.id,
            "name": u.name,
            "cpf": u.cpf
        }
        for u in usuarios
    ]

    return jsonify(lista_usuarios), 200

# Endpoint para obter um usuário específico por ID
@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):

    try:

        u = UserService.get_user_by_id(user_id)

        return jsonify({
            "id": u.id,
            "name": u.name,
            "cpf": u.cpf
        }), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    
# Endpoint para atualizar um usuário existente
@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    dados = request.get_json()

    if not dados:
        return jsonify({'error': 'Dados incompletos'}), 400
    
    try:
        usuario_atualizado = UserService.update_user(
            user_id,
            name=dados.get('name'),
            cpf=dados.get('cpf')
        )

        return jsonify({
            "mensagem": "Usuário atualizado com sucesso",
            "usuario": {
                "id": usuario_atualizado.id,
                "name": usuario_atualizado.name,
                "cpf": usuario_atualizado.cpf
            }
        }), 200
    
    except ValueError as e:
        # se o erro for "não encontrado", retornamos 404, caso contrário, 400 para erros de validação
        status = 404 if "não encontrado" in str(e) else 400
        return jsonify({"error": str(e)}), status
    
# Endpoint para deletar um usuário
@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    try:
        UserService.delete_user(user_id)
        return jsonify({"mensagem": "Usuário e reservas deletados com sucesso"}), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    

#==========================================
# FILME
# =========================================

# endpoint para criar um novo filme
@bp.route('/filmes', methods=['POST'])
def create_filme():
    dados = request.get_json()

    if not dados or 'titulo' not in dados:
        return jsonify({'error': 'Dados incompletos'}), 400
    
    try:
        novo_filme = FilmeService.create_filme(
            titulo=dados.get('titulo')
        )

        return jsonify({
            "mensagem": "Filme criado com sucesso",
            "filme": {
                "id": novo_filme.id,
                "titulo": novo_filme.titulo
            }   
        }), 201
    
    except ValueError as e:
        # erros de validação, como título vazio, serão capturados aqui
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        # erro genérico para capturar outros tipos de erros inesperados
        return jsonify({"error": "Erro interno do servidor"}), 500

# endpoint para listar todos os filmes
@bp.route('/filmes', methods=['GET'])
def get_filmes():

    filmes = FilmeService.get_all_filmes()

    lista_filmes = [
        {
            "id": f.id,
            "titulo": f.titulo
        }
        for f in filmes
    ]

    return jsonify(lista_filmes), 200

# endpoint para obter um filme específico por ID
@bp.route('/filmes/<int:filme_id>', methods=['GET'])
def get_filme(filme_id):

    try: 

        f = FilmeService.get_filme_by_id(filme_id)

        return jsonify({
            "id": f.id,
            "titulo": f.titulo
        }), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404 

# endpoint para atualizar um filme existente
@bp.route('/filmes/<int:filme_id>', methods=['PUT'])
def update_filme(filme_id):
    dados = request.get_json()

    if not dados:
        return jsonify({'error': 'Dados incompletos'}), 400
    
    try:
        filme_atualizado = FilmeService.update_filme(
            filme_id,
            titulo=dados.get('titulo')
        )

        return jsonify({
            "mensagem": "Filme atualizado com sucesso",
            "filme": {
                "id": filme_atualizado.id,
                "titulo": filme_atualizado.titulo
            }
        }), 200
    
    except ValueError as e:
        # se o erro for "não encontrado", retornamos 404, caso contrário, 400 para erros de validação
        status = 404 if "não encontrado" in str(e) else 400
        return jsonify({"error": str(e)}), status

# endpoint para deletar um filme
@bp.route('/filmes/<int:filme_id>', methods=['DELETE'])
def delete_filme(filme_id):
    
    try:
        FilmeService.delete_filme(filme_id)
        return jsonify({"mensagem": "Filme e sessões deletados com sucesso"}), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


#==========================================
# SESSÃO
# =========================================

# Endpoint para criar uma nova sessão
@bp.route('/sessoes', methods=['POST'])
def create_sessao():
    dados = request.get_json()

    # Verificação básica de campos obrigatórios antes de chamar a service
    campos_obrigatorios = ['horario_data', 'is_dub', 'sala_id', 'filme_id']
    if not dados or not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({'error': 'Dados incompletos. Todos os campos são obrigatórios'}), 400
    
    try:
        nova_sessao = SessaoService.create_sessao(
            horario_data=dados.get('horario_data'),
            is_dub=dados.get('is_dub'),
            sala_id=dados.get('sala_id'),
            filme_id=dados.get('filme_id')
        )

        return jsonify({
            "mensagem": "Sessão criada com sucesso",
            "sessao": {
                "id": nova_sessao.id,
                "horario_data": nova_sessao.horario_data.isoformat() if hasattr(nova_sessao.horario_data, 'isoformat') else nova_sessao.horario_data,
                "is_dub": nova_sessao.is_dub,
                "sala_id": nova_sessao.sala_id,
                "filme_id": nova_sessao.filme_id
            }   
        }), 201
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500


# Endpoint para listar todas as sessões
@bp.route('/sessoes', methods=['GET'])
def get_sessoes():
    sessoes = SessaoService.get_all_sessoes()

    lista_sessoes = [
        {
            "id": s.id,
            "horario_data": s.horario_data.isoformat() if hasattr(s.horario_data, 'isoformat') else s.horario_data,
            "is_dub": s.is_dub,
            "sala_id": s.sala_id,
            "filme_id": s.filme_id,
            # Se você configurou os relationship no models, pode exibir o nome:
            # "filme_titulo": s.filme.titulo if s.filme else None
        }
        for s in sessoes
    ]

    return jsonify(lista_sessoes), 200


# Endpoint para obter uma sessão específica por ID
@bp.route('/sessoes/<int:sessao_id>', methods=['GET'])
def get_sessao(sessao_id):
    try:
        s = SessaoService.get_sessao_by_id(sessao_id)

        return jsonify({
            "id": s.id,
            "horario_data": s.horario_data.isoformat() if hasattr(s.horario_data, 'isoformat') else s.horario_data,
            "is_dub": s.is_dub,
            "sala_id": s.sala_id,
            "filme_id": s.filme_id
        }), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


# Endpoint para atualizar uma sessão existente
@bp.route('/sessoes/<int:sessao_id>', methods=['PUT'])
def update_sessao(sessao_id):
    dados = request.get_json()

    if not dados:
        return jsonify({'error': 'Dados incompletos'}), 400
    
    try:
        sessao_atualizada = SessaoService.update_sessao(
            sessao_id,
            horario_data=dados.get('horario_data'),
            is_dub=dados.get('is_dub'),
            sala_id=dados.get('sala_id'),
            filme_id=dados.get('filme_id')
        )

        return jsonify({
            "mensagem": "Sessão atualizada com sucesso",
            "sessao": {
                "id": sessao_atualizada.id,
                "horario_data": sessao_atualizada.horario_data.isoformat() if hasattr(sessao_atualizada.horario_data, 'isoformat') else sessao_atualizada.horario_data,
                "is_dub": sessao_atualizada.is_dub,
                "sala_id": sessao_atualizada.sala_id,
                "filme_id": sessao_atualizada.filme_id
            }
        }), 200
    
    except ValueError as e:
        # Se a mensagem contiver "não encontrada", retornamos 404
        status = 404 if "não encontrada" in str(e).lower() else 400
        return jsonify({"error": str(e)}), status


# Endpoint para deletar uma sessão
@bp.route('/sessoes/<int:sessao_id>', methods=['DELETE'])
def delete_sessao(sessao_id):

    try:
        SessaoService.delete_sessao(sessao_id)
        return jsonify({"mensagem": "Sessão e reservas deletadas com sucesso"}), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    

#==========================================
# ASSENTO
# =========================================

# Endpoint para criar um novo assento
@bp.route('/assentos', methods=['POST'])
def create_assento():
    dados = request.get_json()

    if not dados or 'numero' not in dados or 'sala_id' not in dados:
        return jsonify({'error': 'Dados incompletos. Número e ID da sala são obrigatórios'}), 400
    
    try:
        novo_assento = AssentoService.create_assento(
            numero=dados.get('numero'),
            sala_id=dados.get('sala_id')
        )

        return jsonify({
            "mensagem": "Assento criado com sucesso",
            "assento": {
                "id": novo_assento.id,
                "numero": novo_assento.numero,
                "sala_id": novo_assento.sala_id
            }   
        }), 201
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500


# Endpoint para listar todos os assentos
@bp.route('/assentos', methods=['GET'])
def get_assentos():
    assentos = AssentoService.get_all_assentos()

    lista_assentos = [
        {
            "id": a.id,
            "numero": a.numero,
            "sala_id": a.sala_id
        }
        for a in assentos
    ]

    return jsonify(lista_assentos), 200


# Endpoint para obter um assento específico por ID
@bp.route('/assentos/<int:assento_id>', methods=['GET'])
def get_assento(assento_id):
    try:
        a = AssentoService.get_assento_by_id(assento_id)

        return jsonify({
            "id": a.id,
            "numero": a.numero,
            "sala_id": a.sala_id
        }), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


# Endpoint para atualizar um assento existente
@bp.route('/assentos/<int:assento_id>', methods=['PUT'])
def update_assento(assento_id):
    dados = request.get_json()

    if not dados:
        return jsonify({'error': 'Dados incompletos'}), 400
    
    try:
        assento_atualizado = AssentoService.update_assento(
            assento_id,
            numero=dados.get('numero'),
            sala_id=dados.get('sala_id')
        )

        return jsonify({
            "mensagem": "Assento atualizado com sucesso",
            "assento": {
                "id": assento_atualizado.id,
                "numero": assento_atualizado.numero,
                "sala_id": assento_atualizado.sala_id
            }
        }), 200
    
    except ValueError as e:
        # Se o erro for "não encontrado", retornamos 404 (tanto para Assento quanto para Sala)
        status = 404 if "não encontrad" in str(e).lower() else 400
        return jsonify({"error": str(e)}), status


# Endpoint para deletar um assento
@bp.route('/assentos/<int:assento_id>', methods=['DELETE'])
def delete_assento(assento_id):

    try:
        AssentoService.delete_assento(assento_id)
        return jsonify({"mensagem": "Assento e reservas associadas deletados com sucesso"}), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    
#==========================================
# SALA
# =========================================

# Endpoint para criar uma nova sala
@bp.route('/salas', methods=['POST'])
def create_sala():
    dados = request.get_json()

    if not dados or 'nome' not in dados or 'tipo' not in dados or 'capacidade' not in dados:
        return jsonify({'error': 'Dados incompletos. Nome, tipo e capacidade são obrigatórios'}), 400
    
    try:
        nova_sala = SalaService.create_sala(
            nome=dados.get('nome'),
            tipo=dados.get('tipo'),
            capacidade=dados.get('capacidade')
        )

        return jsonify({
            "mensagem": "Sala criada com sucesso",
            "sala": {
                "id": nova_sala.id,
                "nome": nova_sala.nome,
                "tipo": nova_sala.tipo,
                "capacidade": nova_sala.capacidade
            }   
        }), 201
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500


# Endpoint para listar todas as salas
@bp.route('/salas', methods=['GET'])
def get_salas():
    salas = SalaService.get_all_salas()

    lista_salas = [
        {
            "id": s.id,
            "nome": s.nome,
            "tipo": s.tipo,
            "capacidade": s.capacidade
        }
        for s in salas
    ]

    return jsonify(lista_salas), 200


# Endpoint para obter uma sala específica por ID
@bp.route('/salas/<int:sala_id>', methods=['GET'])
def get_sala(sala_id):
    try:
        s = SalaService.get_sala_by_id(sala_id)

        return jsonify({
            "id": s.id,
            "nome": s.nome,
            "tipo": s.tipo,
            "capacidade": s.capacidade
        }), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


# Endpoint para atualizar uma sala existente
@bp.route('/salas/<int:sala_id>', methods=['PUT'])
def update_sala(sala_id):
    dados = request.get_json()

    if not dados:
        return jsonify({'error': 'Dados incompletos'}), 400
    
    try:
        sala_atualizada = SalaService.update_sala(
            sala_id,
            nome=dados.get('nome'),
            tipo=dados.get('tipo'),
            capacidade=dados.get('capacidade')
        )

        return jsonify({
            "mensagem": "Sala atualizada com sucesso",
            "sala": {
                "id": sala_atualizada.id,
                "nome": sala_atualizada.nome,
                "tipo": sala_atualizada.tipo,
                "capacidade": sala_atualizada.capacidade
            }
        }), 200
    
    except ValueError as e:
        # Se o erro for "não encontrada", retornamos 404, senão 400
        status = 404 if "não encontrada" in str(e).lower() else 400
        return jsonify({"error": str(e)}), status


# Endpoint para deletar uma sala
@bp.route('/salas/<int:sala_id>', methods=['DELETE'])
def delete_sala(sala_id):
    try:
        SalaService.delete_sala(sala_id)
        return jsonify({"mensagem": "Sala, sessões e assentos associados deletados com sucesso"}), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    

#==========================================
# RESERVA
# =========================================

# Endpoint para criar uma nova reserva
@bp.route('/reservas', methods=['POST'])
def create_reserva():
    dados = request.get_json()

    if not dados or 'user_id' not in dados or 'sessao_id' not in dados or 'assento_id' not in dados:
        return jsonify({'error': 'Dados incompletos. ID do usuário, sessão e assento são obrigatórios'}), 400
    
    try:
        nova_reserva = ReservaService.create_reserva(
            user_id=dados.get('user_id'),
            sessao_id=dados.get('sessao_id'),
            assento_id=dados.get('assento_id')
        )

        return jsonify({
            "mensagem": "Reserva criada com sucesso",
            "reserva": {
                "id": nova_reserva.id,
                "user_id": nova_reserva.user_id,
                "sessao_id": nova_reserva.sessao_id,
                "assento_id": nova_reserva.assento_id,
                "data_reserva": nova_reserva.data_reserva.isoformat() if hasattr(nova_reserva, 'data_reserva') and nova_reserva.data_reserva else None
            }   
        }), 201
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500


# Endpoint para listar todas as reservas
@bp.route('/reservas', methods=['GET'])
def get_reservas():
    reservas = ReservaService.get_all_reservas()

    lista_reservas = [
        {
            "id": r.id,
            "user_id": r.user_id,
            "sessao_id": r.sessao_id,
            "assento_id": r.assento_id,
            "data_reserva": r.data_reserva.isoformat() if hasattr(r, 'data_reserva') and r.data_reserva else None
        }
        for r in reservas
    ]

    return jsonify(lista_reservas), 200


# Endpoint para obter uma reserva específica por ID
@bp.route('/reservas/<int:reserva_id>', methods=['GET'])
def get_reserva(reserva_id):
    try:
        r = ReservaService.get_reserva_by_id(reserva_id)

        return jsonify({
            "id": r.id,
            "user_id": r.user_id,
            "sessao_id": r.sessao_id,
            "assento_id": r.assento_id,
            "data_reserva": r.data_reserva.isoformat() if hasattr(r, 'data_reserva') and r.data_reserva else None
        }), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


# Endpoint para atualizar uma reserva existente
@bp.route('/reservas/<int:reserva_id>', methods=['PUT'])
def update_reserva(reserva_id):
    dados = request.get_json()

    if not dados:
        return jsonify({'error': 'Dados incompletos'}), 400
    
    try:
        reserva_atualizada = ReservaService.update_reserva(
            reserva_id,
            user_id=dados.get('user_id'),
            sessao_id=dados.get('sessao_id'),
            assento_id=dados.get('assento_id')
        )

        return jsonify({
            "mensagem": "Reserva atualizada com sucesso",
            "reserva": {
                "id": reserva_atualizada.id,
                "user_id": reserva_atualizada.user_id,
                "sessao_id": reserva_atualizada.sessao_id,
                "assento_id": reserva_atualizada.assento_id,
                "data_reserva": reserva_atualizada.data_reserva.isoformat() if hasattr(reserva_atualizada, 'data_reserva') and reserva_atualizada.data_reserva else None
            }
        }), 200
    
    except ValueError as e:
        status = 404 if "não encontrad" in str(e).lower() else 400
        return jsonify({"error": str(e)}), status


# Endpoint para deletar uma reserva
@bp.route('/reservas/<int:reserva_id>', methods=['DELETE'])
def delete_reserva(reserva_id):
    try:
        ReservaService.delete_reserva(reserva_id)
        return jsonify({"mensagem": "Reserva deletada com sucesso"}), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    
