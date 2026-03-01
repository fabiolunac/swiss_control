
from datetime import datetime

data_hoje  = datetime.now()
data_cheg  = datetime(2026, 1, 12)
data_final = datetime(2026, 7, 9 )

dias_totais = (data_final - data_cheg).days
dias_rest   = (data_final - data_hoje).days
dias_corr = dias_totais - dias_rest

print(dias_corr)
