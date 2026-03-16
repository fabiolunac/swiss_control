import sqlite3
import pandas as pd


def ler_tabela(conn):
    df_param = pd.read_sql_query("SELECT rowid, * FROM param", conn)
    print(df_param)


def adicionar_linha(conn):
    cursor = conn.cursor()

    new_local = input('Local: ')
    new_categ = input('Categoria: ')

    cursor.execute(
        """
        INSERT INTO param (Local, Categoria)
        VALUES (?, ?)
        """,
        (new_local, new_categ)
    )

    conn.commit()
    print(f'Dados adicionados! LOCAL: {new_local}, CATEGORIA: {new_categ}')

def deletar_linha(conn):
    cursor = conn.cursor()

    rowid = int(input('Digite o id da linha: '))

    cursor.execute(
    """
    DELETE FROM param
    WHERE rowid = ?
    """, (rowid,)
    )

    conn.commit()

    print(f'Linhar {rowid} deletada')

def mostrar_menu():
    print('--------------------------------------------------------')
    print('Script para gerenciar a tabela de parâmetros')
    print('Menu:')
    print('1 - Ler Tabela')
    print('2 - Adicionar Linha')
    print('3 - Deletar Linha')

    print('0 - Sair')


def main():
    conn = sqlite3.connect('../db/local_param.db')

    while True:
        mostrar_menu()

        try:
            c = int(input('Digite uma opção: '))
        except ValueError:
            print("Digite um número válido!")
            continue

        match c:
            case 1:
                ler_tabela(conn)

            case 2:
                adicionar_linha(conn)

            case 3:
                deletar_linha(conn)

            case 0:
                print("Saindo...")
                break

            case _:
                print("Opção inválida!")

        input("\nPressione ENTER para continuar...")

    conn.close()


if __name__ == "__main__":
    main()