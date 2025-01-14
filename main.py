# src/main.py

from src.usuario import Usuario
from src.conta import Conta
from src.transacao import Transacao
from src.categoria import Categoria  # Para exibir/criar/editar categorias


def criar_usuario(email: str) -> Usuario:
    """
    Cria um novo usuário solicitando os dados pelo console.
    Retorna o objeto Usuario recém-criado.
    """
    nome = input("Digite seu nome: ")
    senha = input("Digite sua senha: ")

    novo_usuario = Usuario(nome=nome, email=email, senha=senha)
    novo_usuario.salvar()

    print(f"Usuário '{nome}' criado com sucesso!")
    return novo_usuario


def obter_ou_criar_conta(usuario: Usuario) -> Conta:
    """
    Retorna a primeira conta do usuário, ou cria uma se não existir nenhuma.
    """
    contas_df = Conta.buscar_por_usuario(usuario.id)
    if contas_df.empty:
        # Cria conta padrão
        nova_conta = Conta(usuario_id=usuario.id, tipo="corrente")
        nova_conta.salvar()
        print("Nenhuma conta encontrada. Uma conta 'corrente' foi criada!")
        return nova_conta
    else:
        # Para simplificar, retorna a primeira conta encontrada
        conta_id = contas_df.iloc[0]["id"]
        return Conta.buscar_por_id(conta_id)


def exibir_categorias_existentes() -> None:
    """
    Exibe todas as categorias salvas no sistema.
    """
    df_categorias = Categoria.carregar_todas()
    if df_categorias.empty:
        print("Não há categorias cadastradas ainda.")
        return

    print("\n=== CATEGORIAS EXISTENTES ===")
    for _, row in df_categorias.iterrows():
        print(f"ID: {row['id']} | Nome: {row['nome']} | Tipo: {row['tipo']} | Ícone: {row['icone']}")
    print("=============================\n")


def criar_nova_categoria() -> Categoria:
    """
    Cria uma nova categoria solicitando os dados pelo console.
    Retorna a instância de Categoria criada.
    """
    nome = input("Digite o nome da categoria: ")
    tipo = input("Digite o tipo da categoria (fixa ou variavel): ")
    icone = input("Digite um ícone (ou deixe em branco): ")

    nova_cat = Categoria(nome=nome, tipo=tipo, icone=icone)
    nova_cat.salvar()
    print(f"Categoria '{nome}' criada com sucesso (ID={nova_cat.id}).")
    return nova_cat


def editar_categoria() -> None:
    """
    Permite editar uma categoria existente, alterando nome, tipo ou ícone.
    """
    df_categorias = Categoria.carregar_todas()
    if df_categorias.empty:
        print("Não há categorias para editar.")
        return

    cat_id_str = input("Digite o ID da categoria que deseja editar: ")
    try:
        cat_id = int(cat_id_str)
    except ValueError:
        print("ID inválido.")
        return

    categoria_obj = Categoria.buscar_por_id(cat_id)
    if not categoria_obj:
        print("Categoria não encontrada.")
        return

    print(f"Editando categoria: [ID={categoria_obj.id}] {categoria_obj.nome}")
    novo_nome = input(f"Novo nome (deixe em branco para manter '{categoria_obj.nome}'): ")
    novo_tipo = input(f"Novo tipo (fixa/variavel) [atual: {categoria_obj.tipo}]: ")
    novo_icone = input(f"Novo ícone (deixe em branco para manter '{categoria_obj.icone}'): ")

    # Se o usuário não digitar nada, mantemos os valores atuais
    if not novo_nome.strip():
        novo_nome = categoria_obj.nome
    if not novo_tipo.strip():
        novo_tipo = categoria_obj.tipo
    if not novo_icone.strip():
        novo_icone = categoria_obj.icone

    try:
        categoria_obj.editar(nome=novo_nome, tipo=novo_tipo, icone=novo_icone)
        print("Categoria atualizada com sucesso!")
    except ValueError as e:
        print(f"Erro ao atualizar categoria: {e}")


def cadastrar_despesa(conta: Conta) -> None:
    """
    Cadastra uma despesa na conta:
      - Exibe as categorias existentes.
      - Permite criar/editar categoria.
      - Solicita o ID da categoria, valor e descrição para registrar a despesa.
    """
    print("\n=== Cadastrar Despesa ===")
    # Exibe as categorias disponíveis logo de cara
    exibir_categorias_existentes()

    while True:
        print("Opções de Categoria:")
        print("1 - Criar Nova Categoria")
        print("2 - Editar Categoria")
        print("3 - Continuar para informar valor e registrar despesa")
        print("4 - Voltar ao menu principal")

        opc = input("Escolha uma opção: ")

        if opc == "1":
            criar_nova_categoria()
            exibir_categorias_existentes()  # Mostra lista novamente atualizada

        elif opc == "2":
            editar_categoria()
            exibir_categorias_existentes()  # Atualiza lista novamente

        elif opc == "3":
            cat_id_str = input("Digite o ID da categoria para essa despesa: ")
            try:
                cat_id = int(cat_id_str)
            except ValueError:
                print("ID inválido.")
                continue

            valor_str = input("Digite o valor da despesa: ")
            try:
                valor = float(valor_str)
            except ValueError:
                print("Valor inválido.")
                continue

            descricao = input("Digite uma descrição para a despesa: ")

            try:
                conta.inserir_despesa(valor, cat_id, descricao=descricao)
                print("Despesa registrada com sucesso!")
            except ValueError as e:
                print(f"Erro ao registrar despesa: {e}")
            break  # encerra o loop e volta ao menu principal

        elif opc == "4":
            # Volta ao menu principal sem cadastrar despesa
            break

        else:
            print("Opção inválida. Tente novamente.")


def menu_usuario(usuario: Usuario):
    """
    Mostra o menu após o usuário ter se autenticado com sucesso.
    """
    conta = obter_ou_criar_conta(usuario)

    while True:
        print("\n==== MENU DO USUÁRIO ====")
        print(f"Bem-vindo(a), {usuario.nome}!")
        saldo_atual = conta.get_saldo()
        print(f"Seu saldo atual é: R$ {saldo_atual:.2f}")
        print("----------------------------")
        print("1 - Depositar")
        print("2 - Cadastrar Despesa")
        print("3 - Consultar Histórico de Transações")
        print("4 - Sair")
        print("----------------------------")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            valor_str = input("Digite o valor do depósito: ")
            try:
                valor = float(valor_str)
            except ValueError:
                print("Valor inválido. Tente novamente.")
                continue

            # Exemplo de ID de categoria para "Depósito"
            categoria_id = 1
            try:
                conta.depositar(valor, categoria_id, descricao="Depósito via menu")
                print("Depósito realizado com sucesso!")
            except ValueError as e:
                print(f"Erro ao depositar: {e}")

        elif opcao == "2":
            # Cadastra despesa (com sub-menu de categorias)
            cadastrar_despesa(conta)

        elif opcao == "3":
            df_transacoes = Transacao.buscar_por_conta(conta.id)
            if df_transacoes.empty:
                print("Não há transações para exibir.")
            else:
                print("\n==== HISTÓRICO DE TRANSAÇÕES ====")
                for _, row in df_transacoes.iterrows():
                    print(f"ID: {row['id']} | "
                          f"Tipo: {row['tipo']} | "
                          f"Valor: R$ {row['valor']:.2f} | "
                          f"Descrição: {row['descricao']} | "
                          f"Data: {row['data']}")
                print("==================================")

        elif opcao == "4":
            print("Saindo do menu...")
            break

        else:
            print("Opção inválida. Tente novamente.")


def main():
    print("=== SISTEMA DE CONTROLE FINANCEIRO ===\n")

    # Solicita email e senha
    email = input("Insira seu e-mail: ")
    senha = input("Insira sua senha: ")

    # Tenta buscar o usuário pelo e-mail
    usuario_encontrado = Usuario.buscar_por_email(email)

    if usuario_encontrado:
        # Usuário existe -> verificar senha
        if usuario_encontrado.autenticar(senha):
            print("Usuário autenticado com sucesso!\n")
            menu_usuario(usuario_encontrado)
        else:
            print("Erro de autenticação: senha incorreta!")
    else:
        # Usuário não existe
        print("Usuário não encontrado.")
        criar_novo = input("Gostaria de criar uma nova conta de usuário? (s/n): ")
        if criar_novo.lower() in ["s", "sim"]:
            novo_usuario = criar_usuario(email)
            # Agora que o usuário foi criado, entra no menu
            menu_usuario(novo_usuario)
        else:
            print("Encerrando o sistema...")


if __name__ == "__main__":
    main()
