# Importando librerias
import os
import json
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup

class NotificadorPrecios:
    def __init__(self, archivo_productos="productos_monitoreados.json"):
        self.archivo_productos = archivo_productos
    def obtener_precio(self, url, selector_css=None, separador_miles=','):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept-Lenguage': 'es-ES,es;q=0.9,en;q=0/8'
            }

            respuesta = requests.get(url, headers=headers, timeout=10)

            if respuesta.status_code != 200:
                return None
            
            soup = BeautifulSoup(respuesta.text, 'html.parser')

            # Buscar el precio con el selector

            precio_elem = None
            if selector_css:
                precio_elem = soup.select_one(selector_css)
            else:
                selectores_comunes = [
                    '.price', '.product-price', '.offer-price', 
                    '.price-value', '.andes-money-amount__fraction'
                ]

                for selector in selectores_comunes:
                    precio_elem = soup.select_one(selector)
                    if precio_elem:
                        break
            if not precio_elem:
                return None
            
            precio_texto = precio_elem.text.strip()

            # Manejar el separador de miles
            if separador_miles == '.':
                precio_texto= precio_texto.replace('.','')
                precio_texto= precio_texto.replace(',','')
            else:
                precio_texto= precio_texto.replace(',','')

            # Estraer el numero
            precio_limpio = re.sub(r'[^\d.]','', precio_texto)
            match = re.search(r'\d+\.\d+|\d+', precio_limpio)

            return float(match.group()) if match else None
        
        except Exception as e:
            return None
        
    def cargar_productos(self):
        if os.path.exists(self.archivo_productos):
            try:
                with open(self.archivo_productos, 'r', encoding='utf-8') as archivo:
                    return json.load(archivo)
            except Exception:
                pass
        return []
    
    def guardar_productos(self, productos):
        try:
            with open(self.archivo_productos, 'w', encoding='utf-8') as archivo:
                json.dump(productos,archivo, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def agregar_producto(self, nombre, url, precio_deseado, selector_css=None, separador_miles=','):
        productos = self.cargar_productos()

        # Verificar si el producto ya existe
        for producto in productos:
            if producto['url'] == url:
                return False
        
        # Obtener el precio actual
        precio_actual = self.obtener_precio(url, selector_css, separador_miles)

        # Crear nuevo producto
        nuevo_producto ={
            'nombre': nombre,
            'url' : url,
            'precio_deseado': float(precio_deseado),
            'precio_actual': precio_actual,
            'selector_css': selector_css,
            'separador_miles': separador_miles,
            'fecha_agregado': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'historial_precios': []
        }

        if precio_actual is not None:
            nuevo_producto['historial_precios'].append({
                'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'precio': precio_actual
            })

        productos.append(nuevo_producto)
        self.guardar_productos(productos)

        return True
    
    def actualizar_precios(self):
        productos = self.cargar_productos()
        productos_actualizados = []

        for producto in productos:
            separador_miles = producto.get('separadpr_miles', ',')
            precio_actual = self.obtener_precio(producto['url'], producto.get('selector_css'), separador_miles)

            if precio_actual is not None:
                precio_anterior = producto.get('precio_actual')
                producto['precio_actual'] = precio_actual

                # Agregar al historial
                producto['historial_precios'].append({
                    'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'precio': precio_actual
                })

                # Verificar si el precio ha bajado o alcanzado el precio deseado
                if (precio_anterior is not None and precio_actual < precio_anterior) or (precio_actual <= producto['precio_deseado']):
                    productos_actualizados.append(producto)

        self.guardar_productos(productos)
        return productos_actualizados
    
    def eliminar_producto(self, indice):
        productos = self.cargar_productos()
        if not productos or indice < 1 or indice > len(productos):
            return False
        
        productos.pop(indice - 1)
        self.guardar_productos(productos)

        return True






