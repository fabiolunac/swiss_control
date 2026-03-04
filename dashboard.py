import pandas as pd
from parameters import *

def main():
    df = pd.read_excel(PATH)

    last_line = df.iloc[-1]

    print(last_line['Saldo'])


if __name__ == "__main__":
    main()