# Finance App

Aplicação desenvolvida em **Python** para controle financeiro pessoal.  
O projeto é composto por dois componentes principais:

- **Mini aplicativo para inserção de dados**
- **Interface gráfica para visualização e análise dos dados**

Todos os dados são armazenados em um banco **SQLite**, sem necessidade de planilhas externas.

---

# Estrutura do projeto

O sistema é dividido em dois módulos principais:

```
project/
│
├── app.py
├── add_data.py
├── streamlit.py
├── db/
│   └── finance_control.db
```

---

# Adição de dados

A inserção de dados é feita através de um **mini aplicativo desenvolvido com Tkinter**, que permite registrar gastos de forma rápida e organizada.

Arquivos envolvidos:

- **app.py**  
  Classe principal responsável por criar a janela da aplicação e gerenciar as abas.

- **add_data.py**  
  Subclasse responsável pela aba de inserção de dados no banco SQLite.

Para iniciar o aplicativo de inserção de dados:

```
python3 app.py
```

---

# Interface de visualização

A visualização e análise dos dados é feita através de uma interface web desenvolvida com **Streamlit**.

Essa interface permite:

- Visualizar tabelas de gastos
- Filtrar dados
- Gerar gráficos
- Acompanhar o histórico financeiro

Para iniciar a interface:

```
streamlit run streamlit.py
```

Após iniciar, o Streamlit abrirá automaticamente no navegador.

---

# Banco de dados

O projeto utiliza **SQLite** como sistema de armazenamento.

Características:

- Banco local em arquivo `.db`
- Não requer instalação de servidor
- Integrado diretamente com Python

O banco é criado automaticamente na pasta:

```
db/finance_control.db
```

---

# Bibliotecas utilizadas

O projeto utiliza as seguintes bibliotecas:

- **Tkinter** – interface gráfica para inserção de dados  
- **Streamlit** – dashboard interativo  
- **Pandas** – manipulação e análise de dados  
- **SQLite3** – banco de dados local

---

# Observações

- O sistema **não depende de arquivos Excel**.
- Todos os dados são armazenados diretamente no banco **SQLite**.
- O banco de dados é criado automaticamente caso não exista.