# src/base_model.py
import pandas as pd
import os


class BaseModel:
    """
    Superclasse que fornece métodos genéricos para carregar dados de um arquivo
    e gerar IDs automaticamente.

    As classes que herdarem desta classe deverão sobrescrever o atributo de classe DATA_PATH.
    """
    DATA_PATH = None  # Deve ser sobrescrito pelas subclasses

    @classmethod
    def carregar_todas(cls) -> pd.DataFrame:
        """
        Carrega todos os registros do arquivo Excel em um DataFrame.
        Retorna um DataFrame vazio se o arquivo não existir.
        """
        if cls.DATA_PATH is None:
            raise ValueError("A subclasse deve definir DATA_PATH.")

        if not os.path.exists(cls.DATA_PATH):
            return pd.DataFrame()

        return pd.read_excel(cls.DATA_PATH)

    def _generate_id(self) -> int:
        """
        Gera um novo ID com base no arquivo de dados existente, retornando
        1 se o arquivo não existir ou estiver vazio.
        """
        if self.DATA_PATH is None:
            raise ValueError("A subclasse deve definir DATA_PATH.")

        if not os.path.exists(self.DATA_PATH):
            return 1

        df = pd.read_excel(self.DATA_PATH)
        return df['id'].max() + 1 if not df.empty else 1
