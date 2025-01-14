# src/transacao.py
import pandas as pd
import os
from datetime import datetime
from src.base_model import BaseModel

class Transacao(BaseModel):
    """
    Classe responsável por representar e manipular dados de uma transação.

    Atributos:
        DATA_PATH (str): Caminho para o arquivo Excel onde as transações são salvas.
        id (int): Identificador único da transação.
        conta_id (int): Identificador da conta à qual a transação está associada.
        categoria_id (int): Identificador da categoria à qual a transação está associada.
        tipo (str): Tipo da transação ('entrada' ou 'saida').
        valor (float): Valor da transação.
        descricao (str): Descrição da transação.
        data (str): Data e hora em que a transação foi registrada (no formato string).

    Parâmetros do construtor:
        conta_id (int): ID da conta.
        categoria_id (int): ID da categoria.
        tipo (str): Tipo da transação ('entrada' ou 'saida').
        valor (float): Valor da transação.
        descricao (str, opcional): Descrição da transação. Default é "".
        data (str, opcional): Data e hora da transação. Se None, é definido automaticamente.
        id (int, opcional): Identificador único. Se None, será gerado automaticamente.
    """

    DATA_PATH = 'src/data/transacoes.xlsx'

    def __init__(
            self,
            conta_id: int,
            categoria_id: int,
            tipo: str,
            valor: float,
            descricao: str = "",
            data: str = None,
            id: int = None
    ):
        self.id: int = id or self._generate_id()
        self.conta_id: int = conta_id
        self.categoria_id: int = categoria_id
        self.tipo: str = tipo  # 'entrada' ou 'saida'
        self.valor: float = valor
        self.descricao: str = descricao
        self.data: str = data or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def salvar(self) -> None:
        """
        Salva os dados da transação no arquivo Excel, criando-o se não existir.

        Retorno:
            None: Esta função não retorna valor.
        """

        dados_anteriores = self.carregar_todas()
        nova_linha = {
            'id': [self.id],
            'conta_id': [self.conta_id],
            'categoria_id': [self.categoria_id],
            'tipo': [self.tipo],
            'valor': [self.valor],
            'descricao': [self.descricao],
            'data': [self.data]
        }
        df_novo = pd.DataFrame(nova_linha)
        df_final = pd.concat([dados_anteriores, df_novo], ignore_index=True)
        df_final.to_excel(self.DATA_PATH, index=False)

    @classmethod
    def buscar_por_conta(cls, conta_id: int) -> pd.DataFrame:
        """
        Busca e retorna todas as transações relacionadas a uma conta específica.

        Parâmetros:
            conta_id (int): ID da conta cujas transações serão buscadas.

        Retorno:
            pd.DataFrame: DataFrame contendo todas as transações da conta informada.
        """
        df = cls.carregar_todas()
        transacoes = df[df['conta_id'] == conta_id]
        return transacoes

    def editar(
        self,
        categoria_id: int = None,
        tipo: str = None,
        valor: float = None,
        descricao: str = None,
        data: str = None
    ) -> None:
        """
        Edita os atributos da transação e atualiza o arquivo Excel.

        Parâmetros:
            categoria_id (int, opcional): Novo ID de categoria.
            tipo (str, opcional): Novo tipo da transação ('entrada' ou 'saida').
            valor (float, opcional): Novo valor da transação.
            descricao (str, opcional): Nova descrição da transação.
            data (str, opcional): Nova data/hora da transação.

        Retorno:
            None: Esta função não retorna valor.

        Exceções:
            ValueError: Se a transação não for encontrada ou se o tipo for inválido.
        """
        df = self.carregar_todas()
        index = df.index[df['id'] == self.id].tolist()
        if not index:
            raise ValueError("Transação não encontrada.")
        index = index[0]
        if category_id := categoria_id or None:   # Will do a quick check in code
            df.at[index, 'categoria_id'] = category_id
            self.categoria_id = category_id
        if tipo:
            if tipo not in ['entrada', 'saida']:
                raise ValueError("Tipo inválido. Deve ser 'entrada' ou 'saida'.")
            df.at[index, 'tipo'] = tipo
            self.tipo = tipo
        if valor is not None:
            df.at[index, 'valor'] = valor
            self.valor = valor
        if descricao is not None:
            df.at[index, 'descricao'] = descricao
            self.descricao = descricao
        if data is not None:
            df.at[index, 'data'] = data
            self.data = data
        df.to_excel(self.DATA_PATH, index=False)

    def excluir(self) -> None:
        """
        Exclui a transação do arquivo Excel.

        Retorno:
            None: Esta função não retorna valor.
        """
        df = self.carregar_todas()
        df = df[df['id'] != self.id]
        df.to_excel(self.DATA_PATH, index=False)
