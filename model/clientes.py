from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Clientes(Base):
    __tablename__ = 'clientes'

    id = Column("pk_id", Integer, primary_key=True)
    nome = Column(String(40))
    cpf = Column(String(20))
    telefone = Column(String)
    cep = Column(String(8))
    comentario = Column(String(40))


    def __init__(self, nome:str, cpf:str, telefone:str,
                 cep:str,comentario:str):
        """
        Cria um Cliente

        Arguments:
            nome: nome do cliente efetuado.
            cpf: cpf do cliente
            telefone: telefone do cliente
            cep: cep do cliente
            comentario: comentário descrevendo informação sobre o cliente
        """
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.cep = cep
        self.comentario = comentario

    def update(self, nome:str, cpf:str, telefone:str, cep:str, comentario:str, **kwargs):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.cep = cep
        self.comentario = comentario