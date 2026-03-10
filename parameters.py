import tkinter as tk
from tkinter import ttk
from datetime import datetime
from openpyxl import load_workbook
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
import numpy as np

TODAY = datetime.now().strftime("%d/%m")
MES_ATUAL = datetime.now().strftime('%m/%y')
PATH = "/Users/fabioluna/OneDrive - CERN/Swiss Control.xlsx"
# print(MES_ATUAL)


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
