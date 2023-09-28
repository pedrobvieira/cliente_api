from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, render_template, request, abort, flash, session
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Clientes
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Cliente API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
cliente_tag = Tag(name="Cliente", description="Adição, visualização e remoção de clientes à base")
usuario_tag = Tag(name="Usuario", description="Transfere para o serviço de Login para autenticar o usuário")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/incluir_cliente', tags=[cliente_tag],
          responses={"200": ClientesViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_cliente(form: ClientesSchema):
    """Adiciona um novo cliente à base de dados

    Retorna uma representação dos clientes
    """
    cliente = Clientes(
        nome=form.nome,
        cpf=form.cpf,
        telefone=form.telefone,
        cep=form.cep,
        comentario=form.comentario)
    logger.debug(f"Adicionando cliente: '{cliente.nome}'")
    print('data cliente', cliente.cep)
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(cliente)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado cliente: '{cliente.nome}'")
        return apresenta_cliente(cliente), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Cliente de mesmo nome já salvo na base :/"
        #ogger.warning(f"Erro ao adicionar cliente '{cliente.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar cliente '{cliente.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/buscar_cliente', tags=[cliente_tag],
         responses={"200": ListagemClientesSchema, "404": ErrorSchema})
def get_clientes():
    """Faz a busca por todas os clientes cadastradas

    Retorna uma representação da listagem de clientes.
    """
    #logger.debug(f"Coletando clientes ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    clientes = session.query(Clientes).all()

    if not clientes:
        # se não há clientes cadastrados
        return {"clientes": []}, 200
    else:
        logger.debug(f"%d clientes econtrados" % len(clientes))
        # retorna a representação do cliente
        return apresenta_clientes(clientes), 200


@app.delete('/deletar_cliente', tags=[cliente_tag],
            responses={"200": ClientesSchema, "404": ErrorSchema})
def del_cliente(query: ClientesViewSchema):
    """Exclui um cliente a partir do id do cliente informada

    Retorna uma mensagem de confirmação da remoção.
    """
    cliente_id = query.id
    cliente_nome = unquote(unquote(query.nome))
    cliente_cpf = unquote(unquote(query.cpf))
    cliente_telefone = query.telefone
    cliente_cep = query.cep
    logger.debug(f"Deletando dados sobre o cliente #{cliente_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Clientes).filter(Clientes.id == cliente_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletada cliente #{cliente_nome}")
        return {"mesage": "Cliente removido", "id": cliente_nome}
    else:
        # se a cliente não foi encontrada
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"Erro ao deletar cliente {cliente_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.put('/alterar_cliente', tags=[cliente_tag],
          responses={"200": ClientesViewSchema, "409": ErrorSchema, "400": ErrorSchema})

def alt_cliente(form: ClientesViewSchema):
    """Altera um cliente na base de dados

    Retorna uma representação dos clientes
    """
    cliente = Clientes(
        nome=form.nome,
        cpf=form.cpf,
        telefone=form.telefone,
        cep=form.cep,
        comentario=form.comentario)

    logger.debug(f"Alterando cliente: '{cliente.nome}'")
    print('alterar cliente.......................',  cliente.nome, cliente.cpf)

    try:
        session = Session()
        # Alterando cliente
        my_cliente = session.query(Clientes).get(form.id)
        my_cliente.nome = cliente.nome
        my_cliente.cpf = cliente.cpf
        my_cliente.telefone = cliente.telefone
        my_cliente.cep = cliente.cep
        my_cliente.comentario = cliente.comentario
        # efetivando o comando de alteração doitem na tabela
        session.commit()
        return apresenta_cliente(cliente), 200


    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar cliente '{cliente.nome}', {error_msg}")
        return {"mesage": error_msg}, 400

@app.get ('/login', tags=[usuario_tag])

def do_login(email, senha):
    """Faz o Autenticação do usuário no sistema

    Retorna o nome do usuário autenticado e libera o sistema para o seu uso
    """
    try:
        req = requests.get("http://127.0.0.1:5001/login?email=" + email + "&senha=" + senha)
    except requests.exceptions.ConnectionError:
        return "Service unavailable"
    return req.text
