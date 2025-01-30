import os
import streamlit as st
import pandas as pd
import gspread
import plotly.express as px
from google.oauth2.service_account import Credentials

# ✅ Configurar credenciales y conexión con Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# ✅ Ruta correcta del archivo de credenciales en Codespaces
json_path = "credentials.json"

# ✅ Verificar si el archivo existe antes de cargarlo
if not os.path.exists(json_path):
    st.error("❌ ERROR: No se encontró el archivo credentials.json.")
    st.stop()

# ✅ Autenticación con Google Sheets usando `google-auth`
try:
    credentials = Credentials.from_service_account_file(json_path, scopes=scope)
    client = gspread.authorize(credentials)
    spreadsheet_id = "1huJO_UeOc8bnD7LU8gf4BnJpFnu4uqxtiru6fRvuRWs"
    sheet = client.open_by_key(spreadsheet_id).sheet1
except Exception as e:
    st.error(f"❌ ERROR: No se pudo conectar a Google Sheets. Detalles: {e}")
    st.stop()

# ✅ Función para cargar datos de la hoja
def load_data():
    try:
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"❌ ERROR al cargar datos: {e}")
        return pd.DataFrame()

# ✅ Función para guardar datos en la hoja
def save_data(data):
    try:
        sheet.clear()
        sheet.update([data.columns.values.tolist()] + data.values.tolist())
    except Exception as e:
        st.error(f"❌ ERROR al guardar datos: {e}")

# ✅ Definir opciones actualizadas para País, Sector y ODS
paises = ["Argentina", "Bolivia", "Brasil", "Paraguay", "Uruguay"]
sectores = ["Infraestructura", "SocioAmbiental", "Productivo"]
subsectores = {
    "Infraestructura": ["Construcción", "Transporte", "Energía", "Obras Públicas"],
    "SocioAmbiental": ["Sostenibilidad", "Recursos Naturales", "Gestión Ambiental"],
    "Productivo": ["Industria", "Comercio", "Agricultura", "Turismo"]
}
ods_list = [
    "Fin de la Pobreza", "Hambre Cero", "Salud y Bienestar", "Educación de Calidad",
    "Igualdad de Género", "Agua Limpia y Saneamiento", "Energía Asequible y No Contaminante",
    "Trabajo Decente y Crecimiento Económico", "Industria, Innovación e Infraestructura",
    "Reducción de Desigualdades", "Ciudades y Comunidades Sostenibles", "Producción y Consumo Responsables",
    "Acción por el Clima", "Vida Submarina", "Vida de Ecosistemas Terrestres",
    "Paz, Justicia e Instituciones Sólidas", "Alianzas para Lograr los Objetivos"
]

# ✅ Interfaz de Streamlit
st.title("📌 Registro de Aprobaciones y Desembolsos")

# 🔹 Menú lateral con opciones separadas
menu = ["Registrar Aprobación", "Registrar Desembolso", "Ver Registros", "Estadísticas", "Configuración"]
choice = st.sidebar.selectbox("📌 Menú", menu)

# ✅ Página de Registro de Aprobaciones
if choice == "Registrar Aprobación":
    st.subheader("📝 Registrar Nueva Aprobación")

    pais = st.selectbox("🌍 País", paises)
    sector = st.selectbox("🏢 Sector", sectores)
    subsector = st.selectbox("🏗️ Subsector", subsectores[sector])
    alias = st.text_input("🔖 Alias")
    codigo_operacion = st.text_input("🆔 Código de Operación")
    responsable = st.text_input("👤 Responsable")
    ods_seleccionados = st.multiselect("🌱 ODS Relacionados", ods_list)
    monto = st.number_input("💰 Monto", min_value=0.0, format="%.2f")
    fecha = st.date_input("📅 Fecha de Aprobación")
    fecha_ultimo_desembolso = st.date_input("📅 Fecha Último Desembolso (opcional)", value=None)
    descripcion = st.text_area("📝 Descripción")

    # ✅ Botón para enviar datos
    if st.button("✅ Registrar Aprobación"):
        data = load_data()
        nuevo_registro = {
            "Tipo": "Aprobación", "País": pais, "Sector": sector, "Subsector": subsector,
            "Alias": alias, "Código de Operación": codigo_operacion, "Responsable": responsable,
            "ODS": ", ".join(ods_seleccionados),
            "Monto": monto, "Fecha": str(fecha), "FechaUltimoDesembolso": str(fecha_ultimo_desembolso) if fecha_ultimo_desembolso else "",
            "Descripción": descripcion
        }
        data = pd.concat([data, pd.DataFrame([nuevo_registro])], ignore_index=True)
        save_data(data)
        st.success("🎉 ¡Aprobación registrada con éxito!")
        st.balloons()

# ✅ Página de Registro de Desembolsos
elif choice == "Registrar Desembolso":
    st.subheader("💵 Registrar Nuevo Desembolso")

    pais = st.selectbox("🌍 País", paises)
    sector = st.selectbox("🏢 Sector", sectores)
    subsector = st.selectbox("🏗️ Subsector", subsectores[sector])
    alias = st.text_input("🔖 Alias")
    codigo_operacion = st.text_input("🆔 Código de Operación")
    responsable = st.text_input("👤 Responsable")
    ods_seleccionados = st.multiselect("🌱 ODS Relacionados", ods_list)
    monto = st.number_input("💰 Monto", min_value=0.0, format="%.2f")
    fecha = st.date_input("📅 Fecha de Desembolso")
    fecha_ultimo_desembolso = st.date_input("📅 Fecha Último Desembolso (opcional)", value=None)
    descripcion = st.text_area("📝 Descripción")

    # ✅ Botón para enviar datos
    if st.button("✅ Registrar Desembolso"):
        data = load_data()
        nuevo_registro = {
            "Tipo": "Desembolso", "País": pais, "Sector": sector, "Subsector": subsector,
            "Alias": alias, "Código de Operación": codigo_operacion, "Responsable": responsable,
            "ODS": ", ".join(ods_seleccionados),
            "Monto": monto, "Fecha": str(fecha), "FechaUltimoDesembolso": str(fecha_ultimo_desembolso) if fecha_ultimo_desembolso else "",
            "Descripción": descripcion
        }
        data = pd.concat([data, pd.DataFrame([nuevo_registro])], ignore_index=True)
        save_data(data)
        st.success("💰 ¡Desembolso registrado con éxito!")
        st.balloons()

# ✅ Página de Ver Registros
elif choice == "Ver Registros":
    st.subheader("📋 Registros Existentes")
    data = load_data()
    st.dataframe(data)

# ✅ Página de Estadísticas
elif choice == "Estadísticas":
    st.subheader("📊 Estadísticas de Aprobaciones y Desembolsos")
    data = load_data()
    if not data.empty:
        fig = px.bar(data, x="Tipo", y="Monto", color="Tipo", title="Monto total por tipo")
        st.plotly_chart(fig)
    else:
        st.warning("⚠️ No hay datos para mostrar.")

# ✅ Página de Configuración
elif choice == "Configuración":
    st.subheader("⚙️ Configuración")
    st.write("Aquí puedes agregar futuras opciones de configuración.")






