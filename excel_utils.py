from parameters import *


def salvar_dados(path, dados, sheet_name=None):
    """"
    Function to save the data on excel file
    """

    wb = load_workbook(path)

    ws = wb[sheet_name] if sheet_name else wb.active

    ws.append(dados)

    ws.cell(row=ws.max_row, column=1).number_format = "DD/MM/YYYY"

    wb.save(path)


def read_last_line(path):
    """"
    Function to read the last line from excel file
    """
    df = pd.read_excel(PATH)

    last_values = df.iloc[-1].to_dict()

    last_data = last_values['Data']

    last_local = last_values['Local']

    last_valor = last_values['Valor']

    return last_data, last_local, last_valor
