import requests
from bs4 import BeautifulSoup
import re
import json



from src.models.currency import Currency
import src.models.Trend as Trend


def get_cotization(url='https://www.mydcambios.com.py/'):
    """
    Obtiene las cotizaciones actuales de M&D Cambios
    """
    try:
        # Hacer la petición
        response = requests.get(url)
        response.raise_for_status()
        
        # Parsear HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Mapeo de nombres de moneda
        monedas_map = {
            'us-1': 'USD',           # Dólar Estadounidense
            '640px-Flag_of_Europe': 'EUR',  # Euro
            'descarga': 'BRL',       # Real Brasileño
            'ar': 'ARS',             # Peso Argentino
            'cl[1]': 'CLP',          # Peso Chileno
            '200px-Flag_of_Uruguay_(1828-1830)': 'UYU',  # Peso Uruguayo
            '260px-Bandera-de-inglaterra-400x240': 'GBP',  # Libra Esterlina
            'ca[2]': 'CAD',          # Dólar Canadiense
            '175-suiza_400px[1]': 'CHF',  # Franco Suizo
            'jp[1]': 'JPY'           # Yen Japonés
        }
                
        # Encontrar secciones de cotizaciones
        secciones = soup.find_all('div', class_='cambios-banner-text scrollbox')
        result = {}
        
        for idx, seccion in enumerate(secciones[:2]):
            ciudad = 'Asuncion' if idx == 0 else 'CDE'

            if ciudad != 'Asuncion':
                continue
            
            items = seccion.find_all('ul')
            # Saltar encabezado
            for item in items[1:]:
                try:
                    img = item.find('img')
                    if not img:
                        continue
                    
                    # Obtener nombre de la moneda
                    src = img.get('src', '')

                    nombre_archivo = src.split('/')[-1] #type: ignore

                    extensiones = ['.png', '.jpg', '.jpeg', '.svg', '.gif', '.webp']



                    while any(nombre_archivo.endswith(ext) for ext in extensiones):
                        for ext in extensiones:
                            if nombre_archivo.endswith(ext):
                                nombre_archivo = nombre_archivo[:-len(ext)]
                                break

                    
                    moneda = monedas_map.get(nombre_archivo, nombre_archivo)


                    
                    # Obtener valores
                    valores = item.find_all('li')
                    if len(valores) >= 3:
                        # Limpiar textos
                        buy_text = valores[1].get_text(strip=True)
                        sell_text = valores[2].get_text(strip=True)
                        
                        # Extraer números
                        buy_value = re.sub(r'[^\d.,]', '', buy_text)
                        sell_value = re.sub(r'[^\d.,]', '', sell_text)
                        
                        # Verificar tendencia
                        buy_trend = 'sube' if 'green' in str(valores[1]) else 'baja'
                        sell_trend = 'sube' if 'green' in str(valores[2]) else 'baja'


                        buy_trend = Trend.normalize_trend(buy_trend)
                        sell_trend = Trend.normalize_trend(sell_trend)
                        
                        # result[moneda] = {
                        #     'name': moneda,
                        #     'buy': buy,
                        #     'sell': sell,
                        #     'buy_trend': buy_trend,
                        #     'sell_trend': sell_trend
                        # }

                        result[moneda] = Currency(
                            house= 'MyD',
                            name= moneda,
                            buy= buy_value,
                            sell= sell_value,
                            buy_trend= buy_trend,
                            sell_trend= sell_trend
                        )



                except Exception as e:
                    print(f"Error procesando: {e}")
                    continue
        
        return result
        
    except requests.RequestException as e:
        print(f"Error al obtener la página: {e}")
        return None