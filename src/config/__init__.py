import json, os

config = {}

ruta = os.path.dirname(os.path.abspath(__file__))

def init_config(forzar_entorno: str = "PRD"):
    def init_config_ruta(ruta_config: str):
        with open(ruta_config) as f: config.update(json.load(f))

    ruta_final = ruta + f'\\config_{forzar_entorno.lower()}.json'

    if forzar_entorno == "PRD":
        try: init_config_ruta(ruta_final)

        except FileNotFoundError:
            print("Archivo de produccion no encontrado\n" +
                    "Pasa a usar archivo de desarrollo")
            init_config(forzar_entorno = "DES")

    elif forzar_entorno == "DES":
        try: init_config_ruta(ruta_final)

        except FileNotFoundError:
            print("Archivo de desarrollo no encontrado\n")
            init_config(forzar_entorno = None)

    else:
        print("Ningun archivo para la configuracion")
        raise(RuntimeError)

    config["directorio_carga"] = ruta + '..\\archivos\\al_cargar'
    config["entorno"] = forzar_entorno
    config["nombre_entorno"] = {
            "DES": "desarrollo",
            "PRD":"produccion"}[forzar_entorno]