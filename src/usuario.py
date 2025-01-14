# src/usuario.py
import pandas as pd
import os
from datetime import datetime
from src.base_model import BaseModel

class Usuario(BaseModel):
    """
    Classe responsável por representar e manipular dados de um usuário.

    Atributos:
        DATA_PATH (str): Caminho para o arquivo Excel onde os usuários são salvos.
        id (int): Identificador único do usuário.
        nome (str): Nome do usuário.
        email (str): E-mail do usuário.
        senha (str): Senha do usuário .
        data_cadastro (str): Data e hora de cadastro do usuário no formato string.

    Parâmetros do construtor:
        nome (str): Nome do usuário.
        email (str): E-mail do usuário.
        senha (str): Senha do usuário.
        id (int, opcional): Identificador único do usuário. Se None, será gerado automaticamente.
        data_cadastro (str, opcional): Data/hora de criação do usuário. Se None, define a data/hora atual.
    """

    DATA_PATH = 'src/data/usuarios.xlsx'

    def __init__(self, nome: str, email: str, senha: str, id: int = None, data_cadastro: str = None):
        self.id: int = id or self._generate_id()
        self.nome: str = nome
        self.email: str = email
        self.senha: str = senha
        self.data_cadastro: str = data_cadastro or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def salvar(self) -> None:
        """
        Salva ou anexa os dados do usuário ao arquivo Excel, criando-o se não existir.

        Retorno:
            None: Esta função não retorna valor.
        """

        dados_anteriores = self.carregar_todas()
        nova_linha = {
            'id': [self.id],
            'nome': [self.nome],
            'email': [self.email],
            'senha': [self.senha],
            'data_cadastro': [self.data_cadastro]
        }
        df_novo = pd.DataFrame(nova_linha)
        df_final = pd.concat([dados_anteriores, df_novo], ignore_index=True)
        df_final.to_excel(self.DATA_PATH, index=False)

    @classmethod
    def buscar_por_email(cls, email: str):
        """
        Busca um usuário pelo seu e-mail.

        Parâmetros:
            email (str): E-mail do usuário a ser buscado.

        Retorno:
            Usuario ou None: Retorna uma instância de Usuario se encontrado, ou None caso contrário.
        """
        df = cls.carregar_todas()
        usuario = df[df['email'] == email]
        if not usuario.empty:
            user_data = usuario.iloc[0]
            return cls(
                id=user_data['id'],
                nome=user_data['nome'],
                email=user_data['email'],
                senha=user_data['senha'],
                data_cadastro=str(user_data['data_cadastro'])
            )
        return None

    def atualizar_perfil(self, nome: str = None, email: str = None, senha: str = None) -> None:
        """
        Atualiza os dados do perfil do usuário no arquivo Excel.

        Parâmetros:
            nome (str, opcional): Novo nome do usuário.
            email (str, opcional): Novo e-mail do usuário.
            senha (str, opcional): Nova senha do usuário.

        Retorno:
            None: Esta função não retorna valor.

        Exceções:
            ValueError: Se o usuário não for encontrado no arquivo de dados.
        """
        df = self.carregar_todas()
        index = df.index[df['id'] == self.id].tolist()
        if not index:
            raise ValueError("Usuário não encontrado.")
        index = index[0]
        if nome:
            df.at[index, 'nome'] = nome
            self.nome = nome
        if email:
            df.at[index, 'email'] = email
            self.email = email
        if senha:
            df.at[index, 'senha'] = senha
            self.senha = senha
        df.to_excel(self.DATA_PATH, index=False)

    def autenticar(self, senha: str) -> bool:
        """
        Verifica se a senha informada corresponde à senha do usuário.

        Parâmetros:
            senha (str): Senha a ser verificada.

        Retorno:
            bool: True se a senha estiver correta, False caso contrário.
        """
        return self.senha == senha
