# envysec

## Descripción
`envysec` es una plataforma construida con Django 5.2, Celery y Redis que expone una API REST para ejecutar herramientas de reconocimiento de subdominios (inicialmente Subfinder) de forma asíncrona.

## Requisitos
- Python 3.11
- Django 5.2
- Redis
- Subfinder instalado y accesible en el PATH

## Instalación
1. Clona el repositorio y entra en la carpeta:
   ```bash
   git clone https://tu.repo/envysec.git
   cd envysec
   ```
2. Crea y activa un entorno virtual:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Configuración
1. Asegúrate de que Redis esté instalado y corriendo:
   ```bash
   sudo apt-get install redis-server
   sudo systemctl start redis
   redis-cli ping  # debe responder PONG
   ```
2. Aplica las migraciones de Django:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Uso
1. Inicia el servidor de desarrollo de Django:
   ```bash
   python manage.py runserver
   ```
2. Inicia el worker de Celery:
   ```bash
   celery -A envysec worker --concurrency=1 --loglevel=info
   ```
3. visita el sitio y realiza escaneos:
   ```bash
   http://localhost:8000/scanner/ 
   ```

