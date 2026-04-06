import pandas as pd
import sqlite3

def show_menu():
    print('--------------------------------------------------------')
    print('Script too verify finance database')
    print('Menu:')
    print('1 - Read Table')
    # print('2 - Add Line')
    print('3 - Delete Line')

    print('0 - Quit')

def read_table(conn):
    df = pd.read_sql_query("SELECT rowid, * from gastos", conn)

    print(df.tail(50))

# def add_line(conn):
#     cursor = conn.cursor()

#     cursor.execute(
        
#     )

def deletar_linha(conn):
    cursor = conn.cursor()

    rowid = int(input('Digite o id da linha: '))

    cursor.execute(
    """
    DELETE FROM gastos
    WHERE rowid = ?
    """, (rowid,)
    )

    conn.commit()

    print(f'Linhar {rowid} deletada')

def main():

    conn = sqlite3.connect('../db/finance_control.db')

    while True:
        show_menu()

        try:
            c = int(input('Enter a number: '))
        except ValueError:
            print('Enter a valid number!')
            continue

        match c:
            case 1:
                read_table(conn)

            case 3:
                deletar_linha(conn)

            case 0:
                print('Leaving program...')
                break

            
                
            case _:
                print('Invalid command!')

        input('\nPress ENTER to continue...')




if __name__ == "__main__":
    main()