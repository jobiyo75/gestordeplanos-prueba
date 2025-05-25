# PLANOSREVIT/VIEWS.PY
from django.shortcuts import render
from .models import PlanoRevit
from .forms import CargarCSVRevitForm

import pandas as pd


#--------------------------------
# importar_form.html
#--------------------------------
def importar_csv_revit(request):
    mensaje=''
    if request.method == 'POST':
        form = CargarCSVRevitForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo_csv']

            # Leer csv con pandas
            try:
                df = pd.read_csv(archivo, delimiter=';', encoding='utf-8')
            except Exceptoin as e:
                mensaje = f'Error al leer el archivo: {e}'
                return render(request, 'planosrevit/importar_form.html', {'form': form, 'mensaje': mensaje})

        planos_creados = 0
        planos_omitidos = 0

        for _, fila in df.iterrows():
            sheetnumber = str(fila.get('Sheet Number', '')).strip()

            if sheetnumber and not PlanoRevit.objects.filter(sheetnumber=sheetnumber).exists():
                PlanoRevit.objects.create(
                    sheetnumber=sheetnumber,
                    sheetname = str(fila.get('Sheet Name', '')).strip(),
                    viewsubgroup = str(fila.get('GEN_ViewSubgroup', '')).strip(),
                    buildingzone = str(fila.get('SHE_DisciplineBuildingZone', '')).strip(),
                    )
                planos_creados += 1
            else:
                planos_omitidos += 1

        mensaje = f'{planos_creados} planos Revit importados correctamente.'
    else:
        form = CargarCSVRevitForm()
    
    return render(request, 'planosrevit/importar_form.html',{'form': form, 'mensaje': mensaje})



# lista_planos_revit.html
def lista_planos_revit(request):
    planos = PlanoRevit.objects.all()
    return render(request, 'planosrevit/lista_planos_revit.html',{'planos': planos})