from notificador import NotificadorPrecios

def mostrar_productos(notifica):
    productos = notifica.cargar_productos()

    if not productos:
        print('\nNo hay profuctos monitoreados.')
        return
    
    print(f"\n PRODUCTOS MONITOREADOS ({len(productos)}) ===")

    for i, producto in enumerate(productos, 1):
        print(f"\n{i}. {producto['nombre']}")
        print(f"    URL: {producto['url']}")
        print(f"    Precio actual: {producto.get('precio_actual', 'No disponible')}")
        print(f"    Precio deseado: {producto['precio_deseado']}")

        # Mostrar precio si existe

        if producto.get('historial_precios'):
            print(" Historial de precios recientes:")
            for registro in producto['historial_precios'][-3:]: # Muestra los ultimos 3
                print(f"    {registro['fecha']}: {registro['precio']}")

def main():
    "Funcion principal con menu interativo"
    print("=== NOTIFICADOR DE PRECIOS GENERICO ===")

    notifica = NotificadorPrecios()

    while True:
        print("\nOpciones:")
        print("1. Agregar producto para monitorear")
        print("2. Mostrar productos monitoreados")
        print("3. Actualizar precios")
        print("4. Eliminar un producto")
        print("5. Salir")

        opcion = input("\n Seleciona una opcion (1-5): ")

        if opcion == "1":
            nombre = input("\nIngresa el nombre del producto: ")
            url = input('Ingresal la url del producto: ')
            precio_deseado = float(input("Ingresa el precio deseado: "))
            usar_selector = input("Deseas espesificar un selector CSS personalizado? (s/n): ").lower() == 's'
            selector_css = None

            if usar_selector:
                selector_css = input('Ingresa el selector CSS para el precio: ')

            # Preguntar por el separador de miles

            separador_miles = input("Cual es el separador de miles en el precio? (, o .) [por defecto ',']: ").strip()
            if separador_miles not in ['.',',']:
                separador_miles = ','
                print("Usando separador de miles por defecto: ','")

            resultado = notifica.agregar_producto(nombre,url,precio_deseado,selector_css,separador_miles)

            if resultado:
                print(f"\nProducto '{nombre}' agregado correctamente")
            else:
                print(f"\nNo se pudo agregar el producto '{nombre}' (posiblemente ya existe)")

        elif opcion == '2':
            mostrar_productos(notifica)
        
        elif opcion == '3': # Actualiza precios
            print('\nActualizando precio de los productos...')
            productos_actualizados = notifica.actualizar_precios()

            if productos_actualizados:
                print(f'\nSe encontraron {len(productos_actualizados)} productos bajo el precio!')
                for producto in productos_actualizados:
                    print(f"- {producto['nombre']}': Precio actual {producto['precio_actual']}")
            else:
                print("\nNo se encontraron cambios importantes en los precios")

        elif opcion == '4':
            mostrar_productos(notifica)

            productos = notifica.cargar_productos()
            if productos:
                try:
                    indice = int(input('\nIngresa el numero del producto a eliminar: '))
                    if notifica.eliminar_producto(indice):
                        print(f"\nProducto #{indice} eliminado correctamente")
                    else:
                        print(f'\nNo se pudo eliminar correcamente el producto #{indice}')
                except ValueError:
                    print('\nPor favor, ingresa un numero valido')
            else:
                print('\nNo hay productos que eliminar')
        
        elif opcion == '5':
            print('\nGracias por usar el programa')
            break
        
        else:
            print("\nOpcion no valida.")

main()