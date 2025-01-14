# src/categoria.py
import pandas as pd
from src.base_model import BaseModel

class Categoria(BaseModel):
    """
    Classe responsável por representar e manipular uma categoria.

    Atributos:
        DATA_PATH (str): Caminho para o arquivo Excel onde as categorias são salvas.
        id (int): Identificador único da categoria.
        nome (str): Nome da categoria.
        tipo (str): Tipo da categoria. Pode ser 'fixa' ou 'variavel'.
        icone (str): Ícone associado à categoria (pode ser uma string vazia se não houver ícone).

    Parâmetros do construtor:
        nome (str): Nome da categoria.
        tipo (str): Tipo da categoria ('fixa' ou 'variavel').
        icone (str, opcional): Ícone da categoria. Default é "".
        id (int, opcional): Identificador único. Se não informado, um novo ID será gerado automaticamente.
    """

    DATA_PATH = 'src/data/categorias.xlsx'

    def __init__(self, nome: str, tipo: str, icone: str = "", id: int = None):
        """
        Construtor da classe Categoria.
        """
        # Agora o ID é gerado chamando o método herdado _generate_id()
        self.id: int = id or self._generate_id()
        self.nome: str = nome
        self.tipo: str = tipo  # 'fixa' ou 'variavel'
        self.icone: str = icone

    def salvar(self) -> None:
        """
        Salva os dados da categoria no arquivo Excel, criando-o se não existir.
        """
        dados_anteriores = self.carregar_todas()  # chama o método herdado
        nova_linha = {
            'id': [self.id],
            'nome': [self.nome],
            'tipo': [self.tipo],
            'icone': [self.icone]
        }
        df_novo = pd.DataFrame(nova_linha)
        df_final = pd.concat([dados_anteriores, df_novo], ignore_index=True)
        df_final.to_excel(self.DATA_PATH, index=False)

    @classmethod
    def buscar_por_id(cls, categoria_id: int) -> pd.DataFrame:
        """
        Busca uma categoria pelo seu ID.

        Parâmetros:
            categoria_id (int): ID da categoria a ser buscada.

        Retorno:
            Categoria ou None: Retorna uma instância de Categoria se encontrada;
            caso contrário, retorna None.
        """
        df = cls.carregar_todas()
        categoria = df[df['id'] == categoria_id]
        if not categoria.empty:
            c = categoria.iloc[0]
            return cls(
                id=c['id'],
                nome=c['nome'],
                tipo=c['tipo'],
                icone=c['icone']
            )
        return None

    @classmethod
    def buscar_por_nome(cls, nome: str)-> pd.DataFrame :
        """
        Busca uma categoria pelo seu nome.

        Parâmetros:
            nome (str): Nome da categoria a ser buscada.

        Retorno:
            Categoria ou None: Retorna uma instância de Categoria se encontrada;
            caso contrário, retorna None.
        """
        df = cls.carregar_todas()
        categoria = df[df['nome'].str.lower() == nome.lower()]
        if not categoria.empty:
            c = categoria.iloc[0]
            return cls(
                id=c['id'],
                nome=c['nome'],
                tipo=c['tipo'],
                icone=c['icone']
            )
        return None

    def editar(self, nome: str = None, tipo: str = None, icone: str = None) -> None:
        """
        Edita os atributos da categoria e atualiza o arquivo Excel.

        Parâmetros:
            nome (str, opcional): Novo nome da categoria.
            tipo (str, opcional): Novo tipo da categoria ('fixa' ou 'variavel').
            icone (str, opcional): Novo ícone da categoria.

        Retorno:
            None: Esta função não retorna valor.

        Exceções:
            ValueError: Se a categoria não for encontrada ou se o tipo for inválido.
        """
        df = self.carregar_todas()
        index = df.index[df['id'] == self.id].tolist()
        if not index:
            raise ValueError("Categoria não encontrada.")
        index = index[0]
        if nome:
            df.at[index, 'nome'] = nome
            self.nome = nome
        if tipo:
            if tipo not in ['fixa', 'variavel']:
                raise ValueError("Tipo inválido. Deve ser 'fixa' ou 'variavel'.")
            df.at[index, 'tipo'] = tipo
            self.tipo = tipo
        if icone is not None:
            df.at[index, 'icone'] = icone
            self.icone = icone
        df.to_excel(self.DATA_PATH, index=False)

    def excluir(self) -> None:
        """
        Exclui a categoria do arquivo Excel.

        Retorno:
            None: Esta função não retorna valor.
        """
        df = self.carregar_todas()
        df = df[df['id'] != self.id]
        df.to_excel(self.DATA_PATH, index=False)
