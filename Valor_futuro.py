import streamlit as st

# --- FUNÇÕES MATEMÁTICAS ---

def calcular_valor_futuro(pv, taxa, periodos):
    return pv * ((1 + taxa) ** periodos)

def calcular_valor_presente(fv, taxa, periodos):
    return fv / ((1 + taxa) ** periodos)

def calcular_aporte_mensal(fv, pv, taxa_mensal, meses):
    if taxa_mensal == 0:
        return (fv - pv) / meses
        
    fator_juros = (1 + taxa_mensal) ** meses
    pmt = (fv - (pv * fator_juros)) / ((fator_juros - 1) / taxa_mensal)
    return pmt

# --- INTERFACE STREAMLIT ---

st.set_page_config(page_title="Calculadora Financeira", page_icon="📈", layout="centered")

st.title("📈 Calculadora Financeira Interativa")
st.write("Escolha a simulação desejada nas abas abaixo:")

# Criando as abas de navegação
tab1, tab2, tab3 = st.tabs([
    "1. Valor Futuro", 
    "2. Valor Presente", 
    "3. Aporte Mensal"
])

# --- ABA 1: VALOR FUTURO ---
with tab1:
    st.subheader("Quanto meu dinheiro vai render no futuro?")
    st.caption("Calcule o rendimento de um investimento único sem novos aportes.")
    
    pv1 = st.number_input("Quanto você tem para investir HOJE (R$)", min_value=0.0, value=1000.0, step=100.0, key="pv1")
    taxa_anual1 = st.number_input("Taxa de juros ANUAL (%)", min_value=0.0, value=10.0, step=0.5, key="taxa1")
    anos1 = st.number_input("Tempo do investimento (em anos)", min_value=1, value=5, step=1, key="anos1")
    
    if st.button("Calcular Valor Futuro", type="primary", use_container_width=True):
        taxa = taxa_anual1 / 100.0
        fv_resultado = calcular_valor_futuro(pv1, taxa, anos1)
        juros_ganhos = fv_resultado - pv1
        
        st.divider()
        st.metric("Você terá no FUTURO", f"R$ {fv_resultado:,.2f}", delta=f"R$ {juros_ganhos:,.2f} em juros")
        st.info(f"Ao investir **R$ {pv1:,.2f}** a **{taxa_anual1}% ao ano** por **{anos1} anos**, você terá **R$ {fv_resultado:,.2f}**.")

# --- ABA 2: VALOR PRESENTE ---
with tab2:
    st.subheader("Qual o valor de investimento HOJE?")
    st.caption("Descubra o valor inicial necessário para alcançar uma meta futura.")
    
    fv2 = st.number_input("Quanto você quer ter no FUTURO (R$)", min_value=0.0, value=50000.0, step=1000.0, key="fv2")
    taxa_anual2 = st.number_input("Taxa de juros ANUAL (%)", min_value=0.0, value=10.0, step=0.5, key="taxa2")
    anos2 = st.number_input("Em quantos anos quer atingir esse objetivo?", min_value=1, value=5, step=1, key="anos2")
    
    if st.button("Calcular Valor Presente", type="primary", use_container_width=True):
        taxa = taxa_anual2 / 100.0
        pv_resultado = calcular_valor_presente(fv2, taxa, anos2)
        
        st.divider()
        st.metric("Você precisa investir HOJE", f"R$ {pv_resultado:,.2f}")
        st.info(f"Para alcançar **R$ {fv2:,.2f}** em **{anos2} anos** a **{taxa_anual2}% ao ano**, você precisa investir **R$ {pv_resultado:,.2f}** de uma vez só hoje.")

# --- ABA 3: APORTE MENSAL ---
with tab3:
    st.subheader("Quanto preciso investir POR MÊS?")
    st.caption("Calcule o valor da parcela mensal necessária para atingir um objetivo.")
    
    fv3 = st.number_input("Valor FINAL que você deseja ter (R$)", min_value=0.0, value=100000.0, step=5000.0, key="fv3")
    pv3 = st.number_input("Valor de ENTRADA que já possui hoje (R$)", min_value=0.0, value=0.0, step=500.0, key="pv3")
    taxa_anual3 = st.number_input("Taxa de juros ANUAL esperada (%)", min_value=0.0, value=10.0, step=0.5, key="taxa3")
    anos3 = st.number_input("Em quantos ANOS quer atingir esse objetivo?", min_value=1, value=10, step=1, key="anos3")
    
    if st.button("Calcular Aporte Mensal", type="primary", use_container_width=True):
        taxa_anual_decimal = taxa_anual3 / 100.0
        taxa_mensal = (1 + taxa_anual_decimal) ** (1/12) - 1
        meses = anos3 * 12
        
        aporte_resultado = calcular_aporte_mensal(fv3, pv3, taxa_mensal, meses)
        
        st.divider()
        if aporte_resultado <= 0:
            st.success(f"🎉 O seu valor inicial de **R$ {pv3:,.2f}** já é suficiente para alcançar a meta apenas com os juros acumulados!")
        else:
            st.metric("Aporte Mensal Necessário", f"R$ {aporte_resultado:,.2f} / mês")
            st.info(f"Para alcançar **R$ {fv3:,.2f}** em **{anos3} anos** ({meses} meses) começando com **R$ {pv3:,.2f}**, você precisará investir **R$ {aporte_resultado:,.2f} por mês**.")