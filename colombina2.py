import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(page_title="Dashboard Colombina 2025", layout="wide")

# --- EXTRACCIÓN DE DATOS REALES (Millones de COP) ---
# Datos Balance General 2025 [Fuente: Pág. 31-32]
act_corriente = 980100
inv_2025 = 491516
pas_corriente = 849791
total_activo = 2782262
total_pasivo = 2387669
total_patrimonio = 394593
oblig_financieras_total = 110269 + 1431513 # Corto + Largo plazo

# Datos Estado de Resultados 2025 [Fuente: Pág. 33]
ventas_netas = 3542061
costo_ventas = 2314230
utilidad_bruta = 1227831
utilidad_operativa = 301982
gastos_financieros = 185080
utilidad_neta = 100161
ebitda = 418897 # [Fuente: Pág. 2]

# --- TÍTULO ---
st.title("📊 Análisis Financiero Consolidado: Grupo Colombina 2025")
st.markdown("Cifras extraídas del informe anual auditado (Millones de COP).")

# --- SISTEMA DE PESTAÑAS (WINDOWS) ---
tab1, tab2, tab3 = st.tabs([
    "💧 Liquidez, Actividad y Caja", 
    "⚖️ Endeudamiento", 
    "💰 Rentabilidad"
])

# --- PESTAÑA 1: LIQUIDEZ, ACTIVIDAD Y FLUJO DE CAJA ---
with tab1:
    st.header("Análisis de Liquidez y Operación")
    
    # Cálculos
    razon_corriente = act_corriente / pas_corriente
    prueba_acida = (act_corriente - inv_2025) / pas_corriente
    capital_trabajo = act_corriente - pas_corriente
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Razón Corriente", f"{razon_corriente:.2f}", help="Activo Corriente / Pasivo Corriente")
    col2.metric("Prueba Ácida", f"{prueba_acida:.2f}", help="(Activo Corr - Inventarios) / Pasivo Corr")
    col3.metric("Capital de Trabajo", f"${capital_trabajo:,.0f}M")

    st.divider()
    st.subheader("Indicadores de Actividad y Caja")
    # Nota: Datos de rotación basados en promedios anuales del informe
    c1, c2, c3 = st.columns(3)
    c1.metric("Ciclo de Caja", "28 Días", "Eficiente")
    c2.metric("EBITDA", f"${ebitda:,.0f}M")
    c3.metric("Margen EBITDA", f"{(ebitda/ventas_netas)*100:.1f}%")
    
    # Gráfico de barras para EBITDA histórico (2021-2025) [Fuente: Pág. 2]
    df_ebitda = pd.DataFrame({
        "Año": [2021, 2022, 2023, 2024, 2025],
        "EBITDA": [246314, 373013, 426796, 465871, 418897]
    })
    st.plotly_chart(px.bar(df_ebitda, x="Año", y="EBITDA", title="Evolución EBITDA (2021-2025)"), use_container_width=True)

# --- PESTAÑA 2: ENDEUDAMIENTO ---
with tab2:
    st.header("Estructura de Capital y Solvencia")
    
    # Cálculos
    nivel_endeudamiento = (total_pasivo / total_activo) * 100
    endeud_financiero = (oblig_financieras_total / ventas_netas) * 100
    cobertura_intereses = utilidad_operativa / gastos_financieros
    
    col_e1, col_e2, col_e3 = st.columns(3)
    col_e1.metric("Nivel de Endeudamiento", f"{nivel_endeudamiento:.1f}%", help="Total Pasivo / Total Activo")
    col_e2.metric("Endeud. Financiero / Ventas", f"{endeud_financiero:.1f}%")
    col_e3.metric("Cobertura de Intereses", f"{cobertura_intereses:.2f}x", help="Utilidad Op / Gastos Fin")
    
    st.info(f"**Indicador Deuda Neta / EBITDA:** 3.4x [Fuente: Pág. 82]")
    
    # Gráfico de Gauge para Nivel de Endeudamiento
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = nivel_endeudamiento,
        title = {'text': "Nivel de Endeudamiento (%)"},
        gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "darkblue"}}
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)

# --- PESTAÑA 3: RENTABILIDAD ---
with tab3:
    st.header("Márgenes y Rendimiento")
    
    # Cálculos
    m_bruto = (utilidad_bruta / ventas_netas) * 100
    m_operativo = (utilidad_operativa / ventas_netas) * 100
    m_neto = (utilidad_neta / ventas_netas) * 100
    roa = (utilidad_neta / total_activo) * 100
    roe = (utilidad_neta / total_patrimonio) * 100
    
    c_r1, c_r2, c_r3 = st.columns(3)
    c_r1.metric("Margen Bruto", f"{m_bruto:.1f}%")
    c_r2.metric("Margen Operativo", f"{m_operativo:.1f}%")
    c_r3.metric("Margen Neto", f"{m_neto:.1f}%")
    
    st.divider()
    col_r4, col_r5 = st.columns(2)
    col_r4.metric("ROA (Activo)", f"{roa:.2f}%")
    col_r5.metric("ROE (Patrimonio)", f"{roe:.2f}%")
    
    # Comparativo de Márgenes
    df_margenes = pd.DataFrame({
        "Margen": ["Bruto", "Operativo", "Neto"],
        "Porcentaje": [m_bruto, m_operativo, m_neto]
    })
    st.plotly_chart(px.line(df_margenes, x="Margen", y="Porcentaje", markers=True, title="Cascada de Márgenes de Rentabilidad"), use_container_width=True)

