from parameters import *
import requests


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
    df = pd.read_excel(path)

    last_values = df.iloc[-1].to_dict()

    print(last_values)

    last_data = last_values['Data']

    last_local = last_values['Local']

    last_valor = last_values['Valor']

    return last_data, last_local, last_valor

def eur_chf():
    url = "https://api.frankfurter.app/latest?from=EUR&to=CHF"
    response = requests.get(url, timeout=10)
    data = response.json()
    return data["rates"]["CHF"]

def prepare_data():
    df = pd.read_excel(PATH)
    df_parametros = pd.read_excel(PATH, sheet_name='Parâmetros')

    df['Data'] = pd.to_datetime(df['Data'])

    #Criacao das novas colunas
    df['Categoria'] = df['Local'].map(
        df_parametros.set_index('Local')['Categoria']
    ).fillna('Extra')

    df['Pagamento?'] = np.where(
        (df['Local'] == "CERN") & (df['Valor'] > 3000),
        "Sim",
        "Não"
    )
    df['Mês Pagamento'] = np.where(
        df['Data'].dt.day >= 25, 
        (df['Data'] + pd.DateOffset(months=1)), 
        df['Data']
    )
    df['Mês Pagamento'] = df['Mês Pagamento'].dt.strftime('%m/%y')


    saldo = []
    for i, row in df.iterrows():
        if i == 0:
            saldo_atual = 3486

        elif row['Pagamento?'] == 'Sim':
            saldo_atual = 3486

        else:
            saldo_atual = saldo[-1] - row['Valor']
        
        saldo.append(saldo_atual)

    df['Saldo'] = saldo

    df['Mês Pagamento Atual?'] = np.where(df['Mês Pagamento'] == MES_ATUAL, 'Sim', 'Não')

    return df

def fig_gastos_por_dia():
    df = prepare_data()

    df_gastos = df[df['Pagamento?'] == 'Não']

    gastos_por_dia = df_gastos[df_gastos['Mês Pagamento Atual?'] == "Sim"].groupby('Data')['Valor'].sum()
    gastos_por_dia.index = gastos_por_dia.index.strftime('%d/%m') 

    # fig = gastos_por_dia.plot(kind='bar')
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(gastos_por_dia.index, gastos_por_dia.values)
    ax.set_title("Gastos por dia - Mês Atual")
    ax.set_xlabel("Data")
    ax.set_ylabel("Valor (CHF)")
    fig.tight_layout()

    return fig

def fig_gastos_categoria():
    df = prepare_data()

    df_gastos = df[df['Pagamento?'] == 'Não']

    gastos_categoria = df_gastos[df_gastos['Mês Pagamento Atual?'] == "Sim"].groupby('Categoria')['Valor'].sum().sort_values(ascending=True)

    ax = gastos_categoria.plot(kind='barh', figsize=(8,5))
    plt.title('Gastos por Categoria - Mês Atual')
    plt.xlabel('Valor (CHF)')
    plt.ylabel('Categoria')
    plt.grid(axis='x', alpha=0.2)
    plt.xlim([0, 1200])

    for i, v in enumerate(gastos_categoria.values):
        ax.text(v + 1, i, f'{v:.1f} CHF', va='center')
    # plt.show()

    # return fig