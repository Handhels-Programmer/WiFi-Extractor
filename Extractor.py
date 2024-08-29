import subprocess

def obtener_perfiles_wifi():
    try:
        # Obtener los perfiles de Wi-Fi
        comando = "netsh wlan show profiles"
        resultado = subprocess.check_output(comando, shell=True, text=True)
        
        # Extraer los Wi-Fi
        perfiles = []
        for linea in resultado.split("\n"):
            # Busca la línea que contiene los Wi-Fi
            if "Perfil de todos los usuarios" in linea or "User Profile" in linea:
                # Extrae el nombre de los Wi-Fi
                perfil = linea.split(":")[1].strip()
                perfiles.append(perfil)
        
        # Mensaje si no se encuentren Wi-Fi
        if not perfiles:
            print("No se encontraron perfiles de Wi-Fi.")
        
        return perfiles
    except Exception as e:
        print(f"Error al obtener perfiles: {e}")
        return []

def obtener_detalles_perfil(perfil):
    try:
        # Obtener los detalles de los Wi-Fi, incluida la contraseña
        comando = f'netsh wlan show profile name="{perfil}" key=clear'
        resultado = subprocess.check_output(comando, shell=True, text=True)
        
        detalles = {}
        detalles['Perfil'] = perfil
        
        # Extraer informacion
        for linea in resultado.split("\n"):
            if "SSID name" in linea or "Nombre de SSID" in linea:
                detalles['SSID'] = linea.split(":")[1].strip()
            elif "Key Content" in linea or "Contenido de la clave" in linea:
                detalles['Contraseña'] = linea.split(":")[1].strip()
        
        return detalles
    except Exception as e:
        print(f"Error al obtener detalles del perfil {perfil}: {e}")
        return {}

def guardar_perfiles_en_txt():
    perfiles = obtener_perfiles_wifi()
    
    if not perfiles:
        print("No se encontraron perfiles para guardar en el archivo.")
        return
    
    with open("datos.txt", "w") as archivo:
        for perfil in perfiles:
            detalles = obtener_detalles_perfil(perfil)
            archivo.write(f"Perfil: {detalles.get('Perfil', 'Desconocido')}\n")
            archivo.write(f"SSID: {detalles.get('SSID', 'No disponible')}\n")
            archivo.write(f"Contraseña: {detalles.get('Contraseña', 'No disponible')}\n")
            archivo.write("-" * 40 + "\n")
    
    print("Los datos se han guardado en el archivo datos.txt")

# Extraer y guardar los Wi-Fi en un archivo de texto
guardar_perfiles_en_txt()
