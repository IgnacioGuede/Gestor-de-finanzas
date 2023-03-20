from django.shortcuts import render
from etiquetas.models import Etiqueta
from .models import Registro
from datetime import datetime
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import HttpResponse
import os
import mimetypes
from . import registros_funcionalidad


# Create your views here.

def home(request):
    return render(request, "registros/home.html")


def registros(request):

    etiquetas = Etiqueta.objects.only("nombre").filter(oculta = False).order_by("nombre")
    registros = Registro.objects.all()

    suma = 0
    for registro in registros:
        suma = suma + registro.valor

    informacion = ["Mostrando todos los registros", "Suma de valores: " + str(suma)]

    context = { "etiquetas":etiquetas, "registros":registros, "informacion":informacion}
    return render(request, "registros/registros.html", context)




def registros_search(request):

    etiquetas = Etiqueta.objects.all().order_by("nombre")

    
    if request.GET["etiqueta"] == "None":
        registros = Registro.objects.filter(
            descripcion__icontains = str.title(request.GET["descripcion"]),
            valor__icontains = request.GET["valor"],
            etiqueta = None 
        )


    else:
        registros = Registro.objects.filter(
            descripcion__icontains = str.title(request.GET["descripcion"]),
            valor__icontains = request.GET["valor"],
            etiqueta__nombre = request.GET["etiqueta"]
        )
    
       

    suma = 0
    for registro in registros:
        suma = suma + registro.valor

    filtros = {"descripcion":request.GET["descripcion"], "valor":request.GET["valor"], "etiqueta":request.GET["etiqueta"]}
    informacion = ["Mostrando " + str(registros.count()) + " de " + str(Registro.objects.count()) + " registros",
        "Suma de valores: " + str(suma)
    ]

    context = { "etiquetas":etiquetas, "registros":registros, "filtros":filtros, "informacion": informacion}
    return render(request, "registros/registros.html", context)





def registros_create(request):

    nombre_etiquetas = Etiqueta.objects.only("nombre").filter(oculta = False).order_by("nombre")
    informacion = ["Creando registros..."]

    if request.method == "POST":
        
        descripcion = str.title(request.POST["descripcion"])
        valor = int(request.POST["valor"])

        validacion = registros_funcionalidad.validacion(descripcion, valor)
        
        if validacion["valido"]:

            Registro.objects.create(
                etiqueta = None if request.POST["etiqueta"] == "None" else Etiqueta.objects.get(nombre = request.POST["etiqueta"]),
                descripcion = descripcion,
                valor = valor,
                fecha = datetime.now().date()
            )

        context = {"etiquetas":nombre_etiquetas, "mensaje":validacion["mensaje"], "informacion":informacion}
        return render(request,"registros/create.html",context)

    return render(request, "registros/create.html", {"etiquetas":nombre_etiquetas, "informacion":informacion})




def registros_update(request, pk):
    
    nombre_etiquetas = Etiqueta.objects.only("nombre").all()
    registro_actualizar = Registro.objects.get(id = pk)
    informacion = [f"Actualizando registro '{registro_actualizar.descripcion}'..."]

    if request.method == "POST":
        
        descripcion = str.title(request.POST["descripcion"])   
        valor = int(request.POST["valor"])

        validacion = registros_funcionalidad.validacion(descripcion, valor)
        
        if validacion["valido"]:
            Registro.objects.filter(id = pk).update(
                etiqueta = None if request.POST["etiqueta"] == "None" else Etiqueta.objects.get(nombre = request.POST["etiqueta"]),
                descripcion = descripcion,
                valor = valor,
                fecha = datetime.now().date()
            )
            return HttpResponseRedirect(reverse_lazy("registros"))


        context = {"etiquetas":nombre_etiquetas, "mensaje":validacion["mensaje"],"informacion":informacion}
        return render(request,"registros/registros_update.html",context)

    context = {"registro":registro_actualizar, "etiquetas":nombre_etiquetas,"informacion":informacion}
    return render(request, "registros/update.html", context)






# para borrar registros, la url recibe la PK del registro
class RegistrosDelete(DeleteView):
    model = Registro
    template_name = "registros/confirm_delete.html"
    success_url = reverse_lazy("registros")






def registros_borrar_todo(request):

    if request.method == "POST":
        
        Registro.objects.all().delete()
        return HttpResponseRedirect(reverse_lazy("registros"))

    informacion = ["Borrando todos los registros..."]
    context = {"informacion":informacion}
    return render(request, "registros/borrar_todo.html", context)







def registros_exportar(request):

    if request.method == "POST":

        nombre = str(request.POST["nombre"])
        extension = str(request.POST["extension"])

        archivo = open(nombre + extension, "w")
        registros = Registro.objects.all()

        for x in registros:
            if x.etiqueta == None:
                archivo.write(f"{x.descripcion},None,{x.valor}\n")
            else:
                archivo.write(f"{x.descripcion},{x.etiqueta.nombre},{x.valor}\n")
        archivo.close()


        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file = nombre + extension
        file_path = BASE_DIR + "\\" + file
        path = open(file_path, "r")

        mime_type = mimetypes.guess_type(file_path)
        
        response = HttpResponse(path,content_type = mime_type)

        response['Content-Disposition'] = f"attachment; filename = {file}"

        return response
    
    return render(request, "registros/exportar.html")




def registros_importar(request):

    if request.method == "POST":

        archivo = request.FILES.get("archivo")

        if archivo != None:

            lista = archivo.readline()
            lista = str(lista,"utf-8")

            while len(lista) != 0:

                lista = lista.split(",")

                if not Etiqueta.objects.filter(nombre = lista[1]).exists() and lista[1] != "None":    #Si la etiqueta no existe y tenia algun contenido creado por el usuario
                    if request.POST["crear"] == 0:                                                      #Si no se quiere crear etiquetas, se guardara como NULL
                        lista[1] = "None"
                    else:                                                                               #Caso contrario, se crea la etiqueta
                        Etiqueta.objects.create(nombre = lista[1], oculta = False)
                    
                Registro.objects.create(
                    descripcion = lista[0],
                    etiqueta = None if lista[1] == "None" else Etiqueta.objects.get(nombre = lista[1]),
                    valor = int(lista[2]),
                    fecha = datetime.now().date()
                )

                lista = archivo.readline()
                lista = str(lista,"utf-8")

            mensaje = "La exportación finalizó con éxito"  

        else:
            mensaje = "Debe seleccionar un archivo"  
        
        context = {"mensaje":mensaje}
        return render(request, "registros/importar.html", context)

    return render(request, "registros/importar.html")