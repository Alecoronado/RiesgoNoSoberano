import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuración
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(credentials)

# ID de la Google Sheet
spreadsheet_id = "1huJO_UeOc8bnD7LU8gf4BnJpFnu4uqxtiru6fRvuRWs"

# Intentar abrir la hoja
try:
    sheet = client.open_by_key(spreadsheet_id).sheet1
    print("✅ Conexión exitosa. Se puede leer la hoja.")
except Exception as e:
    print("❌ Error de permisos:", e)
