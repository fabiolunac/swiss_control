# Swiss Control (Tkinter + TTK)

Pequeno app em Python com interface gráfica (Tkinter/TTK) para registrar gastos/entradas em uma planilha Excel e visualizar rapidamente a última linha registrada.

## Funcionalidades

- Formulário com campos: **Data**, **Local**, **Valor (CHF)**
- **Salvar Valores**: adiciona uma nova linha ao final do Excel
- **Últimos Dados**: lê a planilha e mostra a última linha registrada na tela
- Atalhos:
  - **Enter** → salva
  - **Esc** → fecha o app
- Formatação da data na coluna 1 do Excel (`DD/MM/YYYY`)

## Requisitos

- Python 3.10+ (recomendado)
- Dependências:
  - `openpyxl`
  - `pandas`

## Instalação

Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Gerar aplicativo

Para gerar um novo aplicativo executável, rode o seguinte comando:

```
pyinstaller --onefile --windowed app.py
```