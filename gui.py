import os
import json
import pandas as pd
import streamlit as st

archivo_productos = "productos_monitoreados.json"

if os.path.exists(archivo_productos):
    try:
        with open(archivo_productos, 'r', encoding='utf-8') as archivo:
            d = json.load(archivo)
    except Exception:
                pass

product = d
l_product = len(d)

st.title("Compra bien, compra inteligente😎")

for i in range(l_product):
    precios = (d[i].get('historial_precios'))
    preciospd = pd.DataFrame(precios)
    etiqueta_precio = int(d[i].get('precio_actual'))
    container = st.container(border=True)
    container.header(d[i].get('nombre'))
    
    col1, col2 = container.columns(2)
    with col1:
        st.link_button('Comprar 🛒',d[i].get('url'))
    with col2:
        st.badge("💰 "+ str(etiqueta_precio))
    
    container.area_chart(preciospd.get('precio'),color='#ffaa00',stack="center")
    #print(etiqueta_precio)

    
from notificador import NotificadorPrecios
notifica = NotificadorPrecios()
notifica.actualizar_precios()