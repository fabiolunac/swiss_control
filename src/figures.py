import plotly.express as px
import plotly.graph_objects as go
GRAPH_COLOR = '#b82b30'

def fig_expenses_per_column(exp, column, mean=None):
    fig = px.bar(
        exp, 
        x=column, 
        y='Valor', 
        text='Valor'
    )
    if mean is not None:
        fig.add_hline(
            y=mean,
            line_dash="dash",
            line_color="white",
            annotation_text=f"Média: {mean:,.2f} CHF",
            annotation_position="bottom left"
        )
    fig.update_traces(
        texttemplate='%{text:,.2f} CHF', 
        textposition='outside', 
        marker_color=GRAPH_COLOR
    )
    fig.update_layout(
        title=f"Gastos por {column}",
        xaxis_title=column,
        yaxis_title="CHF",
        showlegend=False
    )

    return fig


def fig_waterfall_saldo(df_filtrado, df_gastos):
    pagamentos = df_filtrado[df_filtrado['Pagamento?'] == 'Sim']
    saldo_inicial = float(pagamentos['Valor'].iloc[-1]) if not pagamentos.empty else 3486.0

    gastos_por_dia = df_gastos.groupby('Data')['Valor'].sum().reset_index().sort_values('Data')
    gastos_por_dia['Data_str'] = gastos_por_dia['Data'].dt.strftime('%d/%m')

    saldo_final = saldo_inicial - gastos_por_dia['Valor'].sum()

    x = ['Saldo Inicial'] + list(gastos_por_dia['Data_str']) + ['Saldo Final']
    y = [saldo_inicial] + list(-gastos_por_dia['Valor']) + [0]
    measure = ['absolute'] + ['relative'] * len(gastos_por_dia) + ['total']
    text = (
        [f'{saldo_inicial:,.2f}']
        + [f'-{v:,.2f}' for v in gastos_por_dia['Valor']]
        + [f'{saldo_final:,.2f}']
    )

    fig = go.Figure(go.Waterfall(
        x=x,
        y=y,
        measure=measure,
        text=text,
        textposition='outside',
        decreasing={'marker': {'color': '#b82b30'}},
        totals={'marker': {'color': '#2b5ab8'}},
        connector={'line': {'color': 'gray', 'dash': 'dot'}},
    ))

    fig.update_layout(
        title='Evolução do Saldo por Dia',
        yaxis_title='CHF',
        showlegend=False
    )

    return fig