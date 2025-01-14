# src/conta.py

import pandas as pd
import os
from datetime import datetime
from src.transacao import Transacao
from src.base_model import BaseModel

class Conta(BaseModel):
    """
    Classe responsável por representar e manipular contas de usuários.

    Atributos:
        DATA_PATH (str): Caminho para o arquivo Excel onde as contas são salvas.
        id (int): Identificador único da conta.
        usuario_id (int): Identificador do usuário ao qual a conta pertence.
        tipo (str): Tipo da conta (e.g. 'corrente', 'poupanca').
        data_criacao (str): Data e hora de criação da conta em formato string.

    OBS: O saldo não é salvo diretamente no Excel. Ele é calculado
    a partir das transações (soma das entradas - soma das saídas).
    """

    DATA_PATH = 'src/data/contas.xlsx'

    def __init__(self, usuario_id: int, tipo: str, id: int = None, data_criacao: str = None):
        self.id: int = id or self._generate_id()
        self.usuario_id: int = usuario_id
        self.tipo: str = tipo
        self.data_criacao: str = data_criacao or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def salvar(self) -> None:
        """
        Salva ou anexa os dados da conta ao arquivo Excel, criando-o se não existir.

        Retorno:
            None: Esta função não retorna valor.
        """
        df_existente = self.carregar_todas()  # método herdado
        dados = {
            'id': [self.id],
            'usuario_id': [self.usuario_id],
            'tipo': [self.tipo],
            'data_criacao': [self.data_criacao]
        }
        df_nova = pd.DataFrame(dados)
        df_final = pd.concat([df_existente, df_nova], ignore_index=True)
        df_final.to_excel(self.DATA_PATH, index=False)

    @classmethod
    def buscar_por_id(cls, conta_id: int):
        """
        Busca e retorna uma conta pelo seu ID.
        """
        df = cls.carregar_todas()
        conta = df[df['id'] == conta_id]
        if not conta.empty:
            conta_data = conta.iloc[0]
            return cls(
                id=conta_data['id'],
                usuario_id=conta_data['usuario_id'],
                tipo=conta_data['tipo'],
                data_criacao=str(conta_data['data_criacao'])
            )
        return None

    @classmethod
    def buscar_por_usuario(cls, usuario_id: int) -> pd.DataFrame:
        """
        Busca e retorna todas as contas de um usuário específico.
        """
        df = cls.carregar_todas()
        return df[df['usuario_id'] == usuario_id]

    def get_saldo(self) -> float:
        """
        Calcula o saldo da conta somando todas as transações de 'entrada' e
        subtraindo todas as de 'saida'.
        """
        # Carrega todas as transações
        df_transacoes = Transacao.carregar_todas()
        if df_transacoes.empty:
            return 0.0

        # Filtra apenas as transações desta conta
        df_conta = df_transacoes[df_transacoes['conta_id'] == self.id]
        if df_conta.empty:
            return 0.0

        entradas = df_conta[df_conta['tipo'] == 'entrada']['valor'].sum()
        saidas = df_conta[df_conta['tipo'] == 'saida']['valor'].sum()
        return entradas - saidas

    def depositar(self, valor: float, categoria_id: int, descricao: str = "Depósito") -> None:
        """
        Cria uma transação de 'entrada' (receita).
        """
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser positivo.")

        transacao = Transacao(
            conta_id=self.id,
            categoria_id=categoria_id,
            tipo='entrada',
            valor=valor,
            descricao=descricao
        )
        transacao.salvar()

    def inserir_despesa(self, valor: float, categoria_id: int, descricao: str = "Despesa") -> None:
        """
        Cria uma transação de 'saida' (despesa).
        """
        if valor <= 0:
            raise ValueError("O valor da despesa deve ser positivo.")
        if valor > self.get_saldo():
            raise ValueError("Saldo insuficiente para registrar essa despesa.")

        transacao = Transacao(
            conta_id=self.id,
            categoria_id=categoria_id,
            tipo='saida',
            valor=valor,
            descricao=descricao
        )
        transacao.salvar()
