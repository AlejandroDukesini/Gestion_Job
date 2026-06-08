# PROEDU CRM 2.0.0v

Licencia el 15/05/2026
Última Actualización 08/06/2026 2.0v

Sitio Web desplegada a nivel local para la gestión de los trabajos a entregar, con sus estados de pendientes, entregados, si están pagados o hay adelantos. Utilizado para las personas que realizan trabajos de otros (freelancer/independiente) y quiere mantener una auditoría de como va su trabajo.

# 1. Estructura del Proyecto

Código Back en la carpeta Raíz y el Frontend en /templates (html) /static (css e imágenes).
<br>
├── app.py
<br>
├── database.db
<br>
├── init_db.py
<br>
├── models.py
<br>
├── update_db.py
<br>
├── pages/ # Código de la interfaz (html)
<br>
├── static/ # Código o archivos estáticos (css e imágenes)
<br>
└── README.md # Este archivo

El proyecto fue realizado con los siguientes programas y sus versiones:<br>
Python 3.13.13<br>
fastapi 0.127.0<br>
Flask 3.1.2<br>
Jinja2 3.1.6<br>
pip 26.0.0<br>
HTML 5<br>
CSS 3<br>

# 2. Activar el servidor de python

python app.py

Te saldrá el ip del sitio web sin necesidad de activar también el front, ejemplo: 127.000.000.1

# 3. Instalar las dependencias

pip install -r requirements.txt

# 2. Tecnologías Utilizadas

Detalla el ecosistema técnico del proyecto para dar contexto rápido:Backend: Python, [Flask, FastAPI] base de datos en sql .Frontend: html y css. Comunicación: REST API
