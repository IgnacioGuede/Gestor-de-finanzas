import re

def validacion(descripcion,  valor) -> dict:
    
    valido = False

    if len(descripcion) == 0:
        mensaje = "La descripción se encuentra en blanco"

    elif len(descripcion) > 30:
        mensaje = "La descripción permite máximo 30 caracteres"

    elif re.search("[^0-9]", str(valor)):
        mensaje = "El valor debe contener solo numeros"

    else:
        valido = True
        mensaje = f"Registro '{descripcion}' con el valor '{valor}' ha sido guardado exitosamente!"


    return {"valido":valido, "mensaje":mensaje}


