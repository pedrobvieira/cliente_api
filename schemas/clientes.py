from pydantic import BaseModel
from typing import Optional, List
from model.clientes import Clientes

class ClientesSchema(BaseModel):
    """ Define como um novo cliente a ser inserido deve ser representado
    """
    nome: str = "Pedro"
    cpf: str = "11209074621"
    telefone: str = "32999127280"
    cep: str = "36740000"
    comentario: Optional[str] = " "


class ClientesBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do cliente.
    """
    nome: str = "Pedro"
    cpf: str = "11209074621"
    telefone: str = "32999127280"
    cep: str = "36740000"
    comentario: Optional[str] = " "


class ListagemClientesSchema(BaseModel):
    """ Define como uma listagem das clientes será retornada.
    """
    clientes:List[ClientesSchema]

class ClientesViewSchema(BaseModel):
    """ Define como uma cliente será retornada: cliente.
    """
    id: int = 1
    nome: str = "Pedro"
    cpf: str = "11209074621"
    telefone: str = "32999127280"
    cep: str = "36740000"
    comentario: Optional[str] = " "


class ClientesDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str


def apresenta_clientes(clientes: List[Clientes]):
    """ Retorna uma representação do cliente seguindo o schema definido em
        ClienteViewSchema.
    """
    result = []
    for cliente in clientes:
        result.append({
            "id": cliente.id,
            "nome": cliente.nome,
            "cpf": cliente.cpf,
            "telefone": cliente.telefone,
            "cep": cliente.cep,
            "comentario": cliente.comentario,
        })
    return {"clientes": result}



def apresenta_cliente(clientes: Clientes):
    """ Retorna uma representação do cliente seguindo o schema definido em
        ClientesViewSchema.
    """
    return {
        "id": clientes.id,
        "nome": clientes.nome,
        "cpf": clientes.cpf,
        "telefone": clientes.telefone,
        "cep": clientes.cep,
        "comentario": clientes.comentario
    }
