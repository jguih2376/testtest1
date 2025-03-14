import pandas as pd
import yfinance as yf

@st.cache_data(ttl=1200)
def get_ibov_data():
    acoes = [
        'ALOS3', 'ABEV3', 'ASAI3', 'AURE3', 'AMOB3', 'AZUL4', 'AZZA3', 'B3SA3', 'BBSE3', 'BBDC3', 'BBDC4', 
        'BRAP4', 'BBAS3', 'BRKM5', 'BRAV3', 'BRFS3', 'BPAC11', 'CXSE3', 'CRFB3', 'CCRO3', 'CMIG4', 'COGN3', 
        'CPLE6', 'CSAN3', 'CPFE3', 'CMIN3', 'CVCB3', 'CYRE3', 'ELET3', 'ELET6', 'EMBR3', 'ENGI11', 'ENEV3', 
        'EGIE3', 'EQTL3', 'FLRY3', 'GGBR4', 'GOAU4', 'NTCO3', 'HAPV3', 'HYPE3', 'IGTI11', 'IRBR3', 'ISAE4', 
        'ITSA4', 'ITUB4', 'JBSS3', 'KLBN11', 'RENT3', 'LREN3', 'LWSA3', 'MGLU3', 'POMO4', 'MRFG3', 'BEEF3', 
        'MRVE3', 'MULT3', 'PCAR3', 'PETR3', 'PETR4', 'RECV3', 'PRIO3', 'PETZ3', 'PSSA3', 'RADL3', 'RAIZ4', 
        'RDOR3', 'RAIL3', 'SBSP3', 'SANB11', 'STBP3', 'SMTO3', 'CSNA3', 'SLCE3', 'SUZB3', 'TAEE11', 'VIVT3', 
        'TIMS3', 'TOTS3', 'UGPA3', 'USIM5', 'VALE3', 'VAMO3', 'VBBR3', 'VIVA3', 'WEGE3', 'YDUQ3'
    ]
    
    tickers = [acao + '.SA' for acao in acoes]
    resultados = {"Ação": [], "Variação (%)": [], "Último Preço": []}
    
    for ticker in tickers:
        try:
            # Baixar dados individualmente para cada ticker
            data = yf.download(ticker, period="2d", interval="1d")["Close"]
            if len(data) < 2:
                print(f"{ticker}: Dados insuficientes, pulando.")
                continue
            
            ultimo_preco = data.iloc[-1]
            variacao = ((data.iloc[-1] - data.iloc[-2]) / data.iloc[-2]) * 100
            
            resultados["Ação"].append(ticker[:-3])
            resultados["Variação (%)"].append(variacao)
            resultados["Último Preço"].append(ultimo_preco)
        except Exception as e:
            print(f"Erro ao processar {ticker}: {e}")
    
    # Criar DataFrame a partir dos resultados
    df = pd.DataFrame(resultados)
    return df

# Testar
df = get_ibov_data()
print(df)