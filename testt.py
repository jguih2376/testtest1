import streamlit as st
import plotly.graph_objects as go
from bcb import sgs

@st.cache_data
def get_data():
    start_date = '2010-01-01'  # Reduzindo o período
    dolar = sgs.get({'Dólar': 10813}, start=start_date)
    selic = sgs.get({'Selic': 432}, start=start_date)
    ipca = sgs.get({'IPCA': 13522}, start=start_date)
    
    dolar_atual = dolar.iloc[-1].values[0]
    selic_atual = selic.iloc[-1].values[0]
    ipca_atual = ipca.iloc[-1].values[0]
    juros_real = (((1 + selic_atual/100) / (1 + ipca_atual/100)) - 1) * 100
    
    return selic, selic_atual, ipca, ipca_atual, juros_real, dolar, dolar_atual

@st.cache_resource
def create_chart(data, atual, title, yaxis_title, unit):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data.iloc[:, 0], mode='lines'))
    fig.add_trace(go.Scatter(x=[data.index[-1]], y=[atual], mode='markers', marker=dict(color='red', size=5)))
    fig.update_layout(title=title, yaxis_title=yaxis_title, showlegend=False,                            yaxis=dict(
                                side="right",
                                gridcolor='rgba(255, 255, 255, 0.1)',  # Gridlines sutis
                                zeroline=False,
                                color='#FFFFFF'),
                                                            xaxis=dict(
                                
                                gridcolor='rgba(255, 255, 255, 0.1)',  # Gridlines sutis
                                zeroline=False,
                                color='#FFFFFF'
                            ),
                                height=450)
    fig.add_annotation(
                            x=1,  # Posição no extremo direito (relativo ao eixo X)
                            y=atual,  # Posição no valor do preço atual (eixo Y)
                            xref="paper",  # Referência relativa ao papel (0 a 1)
                            yref="y",  # Referência ao eixo Y em valores absolutos
                            text=f"{atual:.2f}",  # Texto com o preço atual formatado
                            showarrow=True,
                            arrowhead=0,
                            ax=5,  # Deslocamento horizontal da seta
                            ay=0,  # Sem deslocamento vertical
                            font=dict(size=12, color='#FFFFFF'),
                            bgcolor='rgba(0, 0, 0, 0.5)',  # Fundo semi-transparente para legibilidade
                            bordercolor='#FFFFFF',
                            borderwidth=1,
                            xanchor="left",  # Ancorar o texto à esquerda para não invadir o gráfico
                            yanchor="middle"  # Centralizar verticalmente no preço atual
                            )
   
    return fig



st.title("🏛️Estatística Monetária")
with st.spinner("Carregando dados..."):
    selic, selic_atual, ipca, ipca_atual, juros_real, dolar, dolar_atual = get_data()
    
col1, col2 = st.columns([5, 1])
with col1:
    st.plotly_chart(create_chart(selic, selic_atual, 'Taxa de Juros SELIC', 'Taxa de Juros (%)', '%'))
    st.plotly_chart(create_chart(ipca, ipca_atual, 'IPCA Acumulado 12M', 'IPCA acumulado (%)', '%'))
    st.plotly_chart(create_chart(dolar, dolar_atual, 'Cotação do Dólar', 'Valor em R$', 'R$'))


with col2:
    # Exibindo o iframe com alinhamento ajustado
    st.markdown("<br><br><br>", unsafe_allow_html=True)  # Spacing above the box
    combined_code = f"""
        <div style="
            background-color: #ffffff; 
            padding: 12px; 
            border-radius: 8px; 
            margin: 8px 0; 
            box-shadow: 2px 2px 4px rgba(0,0,0,0.1); 
            text-align: center; 
            font-family: sans-serif; 
            max-width: 150px; 
            margin-left: auto; 
            margin-right: auto;">
            <!-- Mundo Section -->
            <span style="font-size: 20px; font-weight: bold; display: block; margin-bottom: 8px; color: black;">Mundo</span>
            <div style="display: flex; justify-content: center; margin-bottom: 12px;">
                <iframe frameborder="0" scrolling="no" height="146" width="108" allowtransparency="true" marginwidth="0" marginheight="0" 
                src="https://sslirates.investing.com/index.php?rows=1&bg1=FFFFFF&bg2=F1F5F8&text_color=333333&enable_border=hide&border_color=0452A1&
                header_bg=ffffff&header_text=FFFFFF&force_lang=12"></iframe>
            </div>
            <!-- Juros Real Section -->
            <span style="font-weight: bold; font-size: 14px; color: black; display: block; margin-bottom: 8px;">Juros Real 🇧🇷</span>
            <span style="font-size: 20px; color: black; font-weight: normal;">{juros_real:.2f}%</span>
        </div>
        """
    st.components.v1.html(combined_code, height=350)
