from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DeleteView
from django.urls import reverse_lazy

from .models import Etiqueta
from registros.models import Registro


# Create your views here.

def etiquetas(request, ocultar):

    etiquetas = Etiqueta.objects.filter(oculta = False) if ocultar else Etiqueta.objects.all()

    informacion = "Mostrando " + str(etiquetas.count()) + " de " + str(Etiqueta.objects.count())
    context = {"etiquetas":etiquetas, "ocultar":ocultar, "informacion":informacion}
    return render(request, "etiquetas/etiquetas.html", context)
    




# lista etiquetas que contengan lo que el usuario ingrese, caso de no haber etiquetas desplegara un mensaje
def etiquetas_search(request):

    etiquetas = Etiqueta.objects.filter(nombre__icontains = str.title(request.GET["buscar"]))

    informacion = "Mostrando " + str(etiquetas.count()) + " de " + str(Etiqueta.objects.count())
    context = {"etiquetas":etiquetas, "informacion":informacion}
    return render(request, "etiquetas/etiquetas.html", context)





# Para crear etiquetas nuevas
def etiquetas_create(request):

    if request.method == "POST":

        nombre = str.title((request.POST["nombre"]))

        if len(nombre) == 0:
            mensaje = "El campo de nombre no puede estar vacío"

        elif len(nombre) > 30:
            mensaje = "El máximo de caracteres permitido es 30"

        elif Etiqueta.objects.filter(nombre = nombre).exists():
            mensaje = f"La etiqueta '{nombre}' ya existe"
        
        else:
            Etiqueta.objects.create(nombre = nombre, oculta = request.POST["oculta"])
            mensaje = f"La etiqueta '{nombre}' se guardó exitosamente!"
        
        informacion = f"Creando etiquetas..."
        context = {"mensaje":mensaje, "nombre": request.POST["nombre"], "oculta": request.POST["oculta"], "informacion":informacion}
        return render(request, "etiquetas/create.html", context)

    context = {"informacion":"Creando etiqueta..."}
    return render(request, "etiquetas/create.html", context)




# Para actualizacion de etiquetas
def etiquetas_update(request, pk):

    etiqueta = Etiqueta.objects.get(id = pk)
    informacion = f"Actualizando etiqueta '{etiqueta.nombre}'..."

    if request.method == "POST":

        nombre = str.title(request.POST["nombre"])

        if len(nombre) == 0:
            mensaje = "El campo de nombre no puede estar vacío"

        elif len(nombre) > 30:
            mensaje = "El máximo de caracteres permitido es 30"

        elif Etiqueta.objects.filter(nombre = nombre).exclude(id = pk).exists():
            mensaje = f"La etiqueta '{request.POST['nombre']}' ya existe"

        else:
            Etiqueta.objects.filter(id = pk).update(nombre = nombre, oculta = request.POST["oculta"])
            return HttpResponseRedirect(reverse_lazy("etiquetas", args = [1]))
        
        context = {"mensaje": mensaje, "informacion":informacion, "nombre": request.POST["nombre"], "oculta": request.POST["oculta"]}
        return render(request, "etiquetas/update.html", context)

    context = {"nombre":etiqueta.nombre, "oculta":etiqueta.oculta, "informacion":informacion}
    return render(request, "etiquetas/update.html", context)




# para borrar etiquetas, la url recibe la PK del registro
class EtiquetasDelete(DeleteView):
    model = Etiqueta
    template_name = "etiquetas/delete.html"
    success_url = reverse_lazy("etiquetas", args = [1])

    def get_context_data(self,*args, **kwargs):
        context = super(EtiquetasDelete, self).get_context_data(*args,**kwargs)

        query = Registro.objects.filter(etiqueta__nombre = kwargs["object"].nombre)
        context['uso_etiqueta'] = query.count()
        context['informacion'] = f"Borrando etiqueta '{kwargs['object'].nombre}'..."
        return context