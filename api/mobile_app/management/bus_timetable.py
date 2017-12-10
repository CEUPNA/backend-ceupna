# Script para obtener los diferentes horarios de las villavesas de Pamplona

import requests

stops = {18: 'Aulario', 161: 'Sario', 461: 'Frente a Sario', 556: 'Sario',
         106: 'Avda. Barañain', 119: 'Avda. Barañain', 205: 'Avda. Barañain'}
stops_arrosadia = (18, 161, 461, 556)
stops_sanitarios = (106, 119, 205)
base_url = 'https://www.infotuc.es/visor/v1/todasllegadas.php?parada='


def __pamplona_line_icon__(line_num):
    return 'https://commons.wikimedia.org/wiki/File:TUCPamplona' + line_num + '.svg'


def get_bus_timetables():
    return __get_pamplona_bus_timetables__() + __get_tudela_bus_timetables__()
#    return __get_tudela_bus_timetables__()


def __get_pamplona_bus_timetables__():
    list_timetable = list()

    for s in stops:
        # Datos generales de la parada.
        stop_dict = dict()
        stop_dict['stop_id'] = s
        stop_dict['stop_name'] = stops[s]
        if s in stops_arrosadia:
            stop_dict['stop_campus'] = 'arrosadia'
        elif s in stops_sanitarios:
            stop_dict['stop_campus'] = 'salud'
        else:
            stop_dict['stop_campus'] = 'unknow'

        # Extracción de todos los horarios y líneas para una cierta parada.
        stop_dict['timetables'] = dict()

       # r = requests.post("https://www.infotuc.es/visor/v1/todasllegadas.php?parada=23")
        #str_cal = r.text
        #print(str_cal)



        list_timetable.append(stop_dict)

    return list_timetable


def __get_tudela_bus_timetables__():
    list_timetable = list()

    # Primera línea
    stop_dict = dict()
    stop_dict['stop_id'] = 0
    stop_dict['stop_name'] = ''
    stop_dict['stop_campus'] = 'tudela'
    l = list()
    l.append({'time1': 'https://www.arasa.es/wp-content/uploads/2017/10/l220upnatudela.gif', 'line': 'Línea 2 (Roja)'})
    stop_dict['timetables'] = l
    list_timetable.append(stop_dict)

    return list_timetable


print(get_bus_timetables())
