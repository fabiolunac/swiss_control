import plotly.express as px
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