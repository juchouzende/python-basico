import os #Bibioteca para habilitar cmd's terminal
import sqlite3 #Banco de dados

# Variável com o nome do BD a ser criado
CAMINHO_BANCO = "jogos.db"

def exibir_cabecalho(texto):
    os.system('cls') # Limpa a tela

    # Cria um efeito visual na palavra "GameVault"
    linha ="*" *len(texto)
    print(linha)
    print(texto)
    print(linha)
    print() #Linha em branco

def inicializar_banco():
    # Abre a conexão com o banco de dados (O indicado em: "CAMINHO_BANCO" no caso: "jogos.db")
    conn = sqlite3.connect(CAMINHO_BANCO)

    # Diz ao BD que de fato SQL está habilitado
    cursor = conn.cursor() 

    # Executa de fato o comando SQL descrito abaixo
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jogos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            plataforma TEXT NOT NULL,
            zerado BOOLEAN NOT NULL DEFAULT 0
        )
        """
    )

    # Funciona como "Ctrl + S" ou salva, ele que grava
    conn.commit()
    # Fecha a conexão
    conn.close()


def listar_jogos():
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor() 
    cursor.execute("SELECT titulo, plataforma, zerado FROM jogos")

    # "fetchall" - Devolve TODAS as linhas do resultado como uma Tupla
    jogos = cursor.fetchall()

    conn.close()

    # Se BD vazio mostra a mensagem abaixo
    if not jogos:
        print("Nenhum jogo cadastrado ainda!\n")
        return

    # Formam o cabeçalho visual antes de listar com 55 traços e alinhamento a esquerda "ljust"
    print(f"{'Título'.ljust(25)} | {'Plataforma'.ljust(12)} | Status")
    print("-" * 55)

    # Laço para exibir todos os jogos cadastrados
    for titulo, plataforma, zerado in jogos:
        status = "zerado" if zerado else "jogando"
        print(f"{titulo.ljust(25)} | {plataforma.ljust(12)} | {status}")

    print() #Linha em branco para não colar no próximo print


def adicionar_jogo(titulo, plataforma):
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor() 
    # SQL - Para inserir novos jogos
    cursor.execute("INSERT INTO jogos (titulo, plataforma, zerado) VALUES (?, ?, ?)", (titulo, plataforma, False),
    )

    conn.commit()
    conn.close()

def marcar_como_zerado(titulo):
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor() 

    # SQL - Para atualizar Status de: jogando para zerado
    cursor.execute("UPDATE jogos SET zerado = ? WHERE titulo = ?", (True, titulo),
    )

    # Guarda quantas linhas foram afetadas na atualização
    encontrou = cursor.rowcount > 0

    conn.commit()
    conn.close()
    return encontrou

def buscar_jogo(titulo):
    # Busca um único jogo pelo título exato. Usada antes de editar,
    # pra saber o título e a plataforma ATUAIS e poder oferecer a opção
    # de manter o valor caso o usuário não queira trocar.
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()

    cursor.execute("SELECT titulo, plataforma FROM jogos WHERE titulo = ?", (titulo,),
    )

    # "fetchone" - Devolve só a PRIMEIRA linha que bater (ou None se não achar nada)
    jogo = cursor.fetchone()

    conn.close()
    return jogo

def atualizar_jogo(titulo_atual, novo_titulo, nova_plataforma):
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()

    # SQL - Para atualizar título e plataforma de um jogo já cadastrado
    # (busca pelo título atual, mesmo critério usado em marcar_como_zerado)
    cursor.execute("UPDATE jogos SET titulo = ?, plataforma = ? WHERE titulo = ?", (novo_titulo, nova_plataforma, titulo_atual),
    )

    # Guarda quantas linhas foram afetadas na atualização
    encontrou = cursor.rowcount > 0

    conn.commit()
    conn.close()
    return encontrou

def deletar_jogo(titulo):
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()

    # SQL - Para excluir um jogo do banco (busca pelo título)
    cursor.execute("DELETE FROM jogos WHERE titulo = ?", (titulo,),
    )

    # Guarda quantas linhas foram afetadas na exclusão
    encontrou = cursor.rowcount > 0

    conn.commit()
    conn.close()
    return encontrou

def exibir_menu():
    exibir_cabecalho("🕹️ GameVault")
    print("1. Adicionar jogo")
    print("2. Listar jogo")
    print("3. Marcar jogo como zerado")
    print("4. Editar jogo")
    print("5. Excluir jogo")
    print("6. Sair\n")

def pausar():
    input("Pressione Enter para voltar ao menu...")

def main():
    inicializar_banco()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            exibir_cabecalho("Adicionar jogo")
            titulo = input("Título do jogo: ")
            plataforma = input("Plataforma: ")
            adicionar_jogo(titulo, plataforma)
            print(f"\n'{titulo}' adicionado com sucesso!")
            pausar()

        elif opcao == "2":
            exibir_cabecalho("Seus jogos")
            listar_jogos()
            pausar()

        elif opcao == "3":
            exibir_cabecalho("Marcar como zerado")
            titulo = input("Título do jogo que zerou: ")

            if marcar_como_zerado(titulo):
                print(f"\n'{titulo}' marcado como zerado!")
            else:
                print(f"\n'{titulo}' Não encontrado!")
                print("Confira se digitou corretamente.")
            pausar()

        elif opcao == "4":
            exibir_cabecalho("Editar jogo")
            titulo = input("Título do jogo que deseja editar: ")

            # Busca o jogo ANTES de perguntar os novos valores, pra poder
            # mostrar o título e a plataforma atuais e permitir manter
            # qualquer um dos dois (só apertando Enter em branco).
            jogo = buscar_jogo(titulo)

            if jogo is None:
                print(f"\n'{titulo}' Não encontrado!")
                print("Confira se digitou corretamente.")
            else:
                titulo_atual, plataforma_atual = jogo
                print(f"\nJogo encontrado: {titulo_atual} ({plataforma_atual})")

                novo_titulo = input(f"Novo título (Enter para manter '{titulo_atual}'): ")
                nova_plataforma = input(f"Nova plataforma (Enter para manter '{plataforma_atual}'): ")

                # Se a pessoa só apertou Enter (string vazia), mantém o valor atual
                if novo_titulo.strip() == "":
                    novo_titulo = titulo_atual
                if nova_plataforma.strip() == "":
                    nova_plataforma = plataforma_atual

                atualizar_jogo(titulo_atual, novo_titulo, nova_plataforma)
                print(f"\n'{titulo_atual}' atualizado para '{novo_titulo}' ({nova_plataforma}) com sucesso!")
            pausar()

        elif opcao == "5":
            exibir_cabecalho("Excluir jogo")
            titulo = input("Título do jogo que deseja excluir: ")

            if deletar_jogo(titulo):
                print(f"\n'{titulo}' excluído com sucesso!")
            else:
                print(f"\n'{titulo}' Não encontrado!")
                print("Confira se digitou corretamente.")
            pausar()

        elif opcao == "6":
            print("Até a próxima! 👋")
            break

        else:
            # Caso o usuário digite uma opção inválida. Exemplo: 9 (Não existe)
            print("Opção inválida! Escolha um número de 1 a 6.")
            pausar()

# Fechamento da função main
if __name__== "__main__":
    main()