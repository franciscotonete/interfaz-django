import re
from django.shortcuts import render
from formulario.models import CallesCondiciones
from django.contrib.auth.decorators import login_required

@login_required
def calculadorauv(request):   
    return render(request, 'calculadorauv/calculadora_uv.html')

def cal_uv(request):
    

    nombre_calle = request.GET['nombre_calle']
    numero_calle = request.GET['numero_calle']
    calle_condiciones = []
    calle_calle = []

    for calles in CallesCondiciones.objects.all():
        if calles.calle == nombre_calle:
            calle_condiciones = calles.condiciones
            calle_calle = calles.calle
    data = [calle_calle,calle_condiciones]

    def getConditions( data ):
        # complex es una condición que afecta a más de una dirección, lo opuesto es stand-alone
        # si la condición tiene a lo más dos caracteres: es sólo una UV, luego es complex porque afecta toda la calle
        if len(data[1]) < 3:
            conditions = [{
                'n': 0,
                'type': 'complex',
                'range': [None,None],
                'parity': 0,
                'uv': data[1],
                'str': data[0]
                }]
        # si hay más de una condición
        else:
            strings = data[1].split('/')[1:] # separar condiciones
            conditions = [] 
            for cond in strings: # quitar información innecesaria y dejar solo [condición, UV]
                cond = cond.strip()[9:].split(' -> ') 
                cond[1] = int(cond[1][6:])
                conditions.append(cond)
            objcond = []
            for cond in conditions:
                c = {
                'n': 0,
                'type': 'complex',
                'range': [None,None],
                'parity': 0,
                'uv': cond[1],
                'str': cond[0]
                }
                multi = False # variable para avisar si eran condiciones stand-alone
                # definir paridad de la condición
                if len(re.findall("IMPAR",c['str'])) > 0:
                    c['parity'] = 2
                elif len(re.findall("PAR",c['str'])) > 0:
                    c['parity'] = 1
                # encontrar rangos
                if len(re.findall("> [0-9]*",c['str'])) > 0:
                    c['range'][0] = int(re.findall("> [0-9]*",c['str'])[0][2:])+1
                elif len(re.findall("< [0-9]*",c['str'])) > 0:
                    c['range'][1] = int(re.findall("< [0-9]*",c['str'])[0][2:])-1
                elif len(re.findall(">= [0-9]*",c['str'])) > 0:
                    c['range'][0] = int(re.findall(">= [0-9]*",c['str'])[0][3:])
                elif len(re.findall("<= [0-9]*",c['str'])) > 0:
                    c['range'][1] = int(re.findall("<= [0-9]*",c['str'])[0][3:])
                elif len(re.findall("= \([0-9]\)*",c['str'])) > 0: # encontrar si hay números stand-alone
                    exceptions = re.findall("[0-9]*",c['str']) # exceptions son los números stand-alone
                    for m in exceptions:
                        if m != '': # agregar directamente cada excepción como una codición separada
                            objcond.append({
                                'n': int(m),
                                'type': 'stand-alone',
                                'uv': cond[1]
                            })
                    multi = True
                # si la condición es compleja y no multi se agrega ahora a las condiciones
                if c['type'] == 'complex': 
                    c['n'] = c['range'][0] or 0;
                if not multi:
                    objcond.append(c)
            # ordenar condiciones por número de apertura
            def getnum( a ):
                return a['n']
            objcond.sort( key=getnum )
            conditions = objcond
        return conditions # diccionario de condiciones

    def getUV( street, number, conditions ):

         
            for i in range(len(conditions)):
                a = conditions[i]
                if (a['n'] == number and a['type'] == 'stand-alone'):
                    uv = a['uv']
                    c = conditions[i]
                    break
                elif a['type'] == 'complex' and int(a['n']) <= int(number) and (not a['parity'] or (number%2)+1 == a['parity']):
                    uv = a['uv']
                    c = conditions[i]
                elif a['n'] > number:
                    break
            try:
                return uv
            except:
                return 0

    UV = getUV(nombre_calle,numero_calle, getConditions(data))
    
    


    context = {
        'uv': UV,
    }

    return render(request, 'calculadorauv/calculadora_uv.html', context)
