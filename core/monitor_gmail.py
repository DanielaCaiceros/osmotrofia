"""
Osmotrofia - Monitor de Gmail
Obtiene datos de Gmail para alimentar la colonia de hongos
"""

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Alcances necesarios para leer emails
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class MonitorGmail:
    def __init__(self, credentials_path='credentials.json'):
        """
        Inicializa el monitor de Gmail

        Args:
            credentials_path: Ruta al archivo credentials.json de la API de Gmail
        """
        self.credentials_path = credentials_path
        self.service = None
        self._autenticar()

    def _autenticar(self):
        """Autentica con la API de Gmail"""
        creds = None

        # Token guardado previamente
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # Si no hay credenciales válidas, hacer login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"No se encuentra {self.credentials_path}. "
                        "Descárgalo desde Google Cloud Console."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Guardar credenciales
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)

    def obtener_nutrientes_digitales(self):
        """
        Obtiene datos de Gmail que servirán como 'nutrientes' para los hongos

        Returns:
            dict: Diccionario con conteos de diferentes tipos de emails
        """
        try:
            nutrientes = {
                'importante': self._contar_por_categoria('CATEGORY_PERSONAL'),
                'spam': self._contar_por_categoria('SPAM'),
                'promociones': self._contar_por_categoria('CATEGORY_PROMOTIONS'),
                'social': self._contar_por_categoria('CATEGORY_SOCIAL'),
                'no_leidos': self._contar_no_leidos(),
                'total': self._contar_total(),
                'adjuntos_pesados': self._contar_adjuntos_pesados(),
            }

            return nutrientes

        except HttpError as error:
            print(f'Error al obtener datos de Gmail: {error}')
            return self._nutrientes_por_defecto()

    def _contar_por_categoria(self, categoria):
        """Cuenta emails en una categoría específica"""
        try:
            result = self.service.users().messages().list(
                userId='me',
                labelIds=[categoria],
                maxResults=1
            ).execute()

            return result.get('resultSizeEstimate', 0)
        except:
            return 0

    def _contar_no_leidos(self):
        """Cuenta emails no leídos"""
        try:
            result = self.service.users().messages().list(
                userId='me',
                labelIds=['UNREAD'],
                maxResults=1
            ).execute()

            return result.get('resultSizeEstimate', 0)
        except:
            return 0

    def _contar_total(self):
        """Cuenta total de emails en inbox"""
        try:
            result = self.service.users().messages().list(
                userId='me',
                labelIds=['INBOX'],
                maxResults=1
            ).execute()

            return result.get('resultSizeEstimate', 0)
        except:
            return 0

    def _contar_adjuntos_pesados(self):
        """Cuenta emails con adjuntos grandes (>5MB)"""
        try:
            # Búsqueda de emails con adjuntos grandes
            result = self.service.users().messages().list(
                userId='me',
                q='larger:5M has:attachment',
                maxResults=1
            ).execute()

            return result.get('resultSizeEstimate', 0)
        except:
            return 0

    def _nutrientes_por_defecto(self):
        """Valores por defecto si falla la conexión"""
        return {
            'importante': 0,
            'spam': 0,
            'promociones': 0,
            'social': 0,
            'no_leidos': 0,
            'total': 0,
            'adjuntos_pesados': 0,
        }

    def obtener_estadisticas_detalladas(self):
        """
        Obtiene estadísticas más detalladas para análisis
        """
        try:
            # Obtener información del perfil
            profile = self.service.users().getProfile(userId='me').execute()

            return {
                'email': profile.get('emailAddress'),
                'total_mensajes': profile.get('messagesTotal', 0),
                'total_hilos': profile.get('threadsTotal', 0),
                'nutrientes': self.obtener_nutrientes_digitales()
            }
        except HttpError as error:
            print(f'Error: {error}')
            return None


# Test del módulo
if __name__ == "__main__":
    print("=== OSMOTROFIA - Monitor de Gmail ===\n")

    try:
        monitor = MonitorGmail()
        nutrientes = monitor.obtener_nutrientes_digitales()

        print("Nutrientes digitales detectados:")
        print(f"  📧 Total emails: {nutrientes['total']}")
        print(f"  ⭐ Importantes: {nutrientes['importante']}")
        print(f"  ☣️  Spam: {nutrientes['spam']}")
        print(f"  🛍️  Promociones: {nutrientes['promociones']}")
        print(f"  👥 Social: {nutrientes['social']}")
        print(f"  💡 No leídos: {nutrientes['no_leidos']}")
        print(f"  📎 Adjuntos pesados: {nutrientes['adjuntos_pesados']}")

    except FileNotFoundError as e:
        print(f"\n⚠️  {e}")
        print("\nPara usar este módulo:")
        print("1. Ve a https://console.cloud.google.com/")
        print("2. Crea un proyecto y habilita Gmail API")
        print("3. Descarga credentials.json")
        print("4. Colócalo en este directorio")
