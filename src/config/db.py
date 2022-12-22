import json, os

ruta = os.path.dirname(os.path.abspath(__file__)) + "\\db.json"

def constructor_uri() -> dict:
    if not os.path.exists(ruta):
        with open(ruta, "w") as f: json.dump({}, f)
        print(f'Recuerda agregar el archivo {ruta} al .gitignore')

    with open(ruta) as f:
        db_config = json.load(f)
        for credencial in ["host", "nombre_bd", "usuario","clave", "motor"]:
            if credencial not in db_config:
                db_config[credencial] = ""
                with open(ruta, "w") as ff: json.dump(db_config, ff)

        if "puerto" not in db_config:
            db_config["puerto"] = 0
            with open(ruta, "w") as ff: json.dump(db_config, ff)

        return db_config