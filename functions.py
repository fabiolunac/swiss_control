import requests
import pandas as pd
from datetime import datetime



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

def parse_date_input(value):
    raw = (value or "").strip()
    if not raw:
        return datetime.now()

    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            pass

    for fmt in ("%d/%m", "%d-%m"):
        try:
            parsed = datetime.strptime(raw, fmt)
            now = datetime.now()
            return parsed.replace(year=now.year)
        except ValueError:
            pass

    raise ValueError("Formato de data inválido. Use DD/MM, DD/MM/AAAA ou AAAA-MM-DD.")

