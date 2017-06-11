# Servicio interno de control de la App del Consejo de Estudiantes de la UPNA

Este proyecto ha sido desarrollado en su totalidad en python. En este sentido, se ha utilizado [scrapy](https://scrapy.org) como herramienta de inspección web, a fin de parte de los datos que se ofrecen por medio del servicio REST desarrollado con [Django REST framework](http://www.django-rest-framework.org). Además, posiblemente a futuro tenga una interfaz web de administración para poder controlar todos los parámetros del servicio así como su actualización.


## Araña web

La intención básica de esta araña es obtener todos los datos que se van a ofrecer de entre los que dispone la [web de la UPNA](http://www.unavarra.es). Esta decisión se toma por la inexistencia de un servicio público de datos, al menos no en forma de API. De esta forma, alimentará de datos una base propia que será ofrecida por la API que se describe más abajo.
 
### Utilización de la araña

La araña se encarga de obtener todos los datos necesarios de la web, por lo que para facilitar esta tarea en realidad son varias arañas las qu se ejecutan. Así, para poder listar todas las que existen hay que situarse en el directorio de scrapy y hacer:
```
scrapy list
```

Actualmente, para ejecutar la araña, después de haber satisfecho sus dependencias, se debe ejecutar el siguiente comando:
```sh
scrapy crawl <spider-name> [-o fichero.json]
```
Si se le añade la opción `-o fichero.json` hará que los datos sean obtenidos en un fichero JSON, algo que puede ser interesante para hacer tests. Se puede hacer lo mismo con ficheros XML o CSV.

Todas estas opciones se encuentran [documentadas](https://doc.scrapy.org/en/latest/topics/commands.html).

### Unión con la base de datos de Django REST framework

A fin de conseguir que los datos sean guardados en la base, se han preparado diferentes _scripts_ de adición de datos. Para ello se debe llamarlo así:
```
python manage.py import_data [opciones]
```
Sabiendo que las opciones que hay implementadas coinciden con los diferentes modelos y son:
* `-c|--centers <ruta/a/centers.json>` 
* `-T|--teachers <ruta/a/teachers.json>`
* `-t|--tics <ruta/a/tics.json>`

Cuando los datos que se quieran introducir ya estuvieran previamente introducidos, el _script_ se encarga de actualizar los mismos a la nueva versión que se presenta.


## API REST
Este servicio REST está programado también en python con Django REST framework como ya se ha explicado. Genera con ellos los JSON necearios para presentar la información contenida en la base de datos. A día de hoy, por razones de seguridad así como por coherencia, todos sus datos son de sólo lectura. Igualmente, ofrece búsquedas sobre algunos de los campos que muestra.

En particular, ahora mismo se puede recuperar por medio del servicio REST los siguientes datos:
* relativos a los centros;
* relativos a los profesores;
* relativos a los recursos TIC que tienen los estudiantes.


## Instalación de todo el entorno
El proyecto actual trabaja en Python 3. Además, se deben tener en cuenta las siguientes dependencias:
* [Scrapy](https://scrapy.org)
* [Django](https://www.djangoproject.com)
* [Django REST Framework](http://www.django-rest-framework.org)
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)

Todas ellas se encuentran en el fichero `requirements.txt` en la versión adecuada para la que está preparada el código. Se puede encontrar toda la información en relación al despligue en esta [entrada del blog de Michal Karzynski](http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/). Existe, también, una [versión en castellano](https://github.com/RITSI/MapaTasas/blob/master/docs/index.md).
