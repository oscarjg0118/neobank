# Neobank

Este proyecto es una aplicación web desarrollada con Django y Django Rest Framework, utilizando PostgreSQL como sistema de gestión de base de datos, y está desplegada en Vercel.

## Tecnologías Utilizadas

- Django: Framework web para desarrollo en Python.
- Django Rest Framework: Toolkit para construir APIs Web en Django.
- PostgreSQL: Sistema de gestión de base de datos relacional.
- Vercel: Plataforma de despliegue y hosting.

## Características del Proyecto

Sistema backend para un neobanco, un banco digital que opera exclusivamente en línea. El sistema debe incluye gestión de usuarios, gestión de cuentas,
procesamiento de transacciones y características de seguridad básicas.

Puede ver la documentacion del API en [Neobank API](https://neobank-delta.vercel.app/redoc/)
## Instalación y Configuración

1. **Clonar el Repositorio**

   ```sh
   git clone https://github.com/oscarjg0118/neobank.git
   cd neobank

   # Configurar Entorno Virtual
   python -m venv venv
   source venv/bin/activate  # En Windows usar `venv\Scripts\activate`

   # Instalar Dependencias
   pip install -r requirements.txt
   ```
2. **Configurar Variables de Entorno**

   Crear un archivo .env en la carpeta vercerl_app y añadir las variables de entorno necesarias, por ejemplo:

   ```
   DB_NAME= name   
   DB_USER= user
   DB_PASSWORD= password
   DB_HOST= host.com
   DB_PORT= 5432
   ```
3. **Migraciones y ejecutar**
   ```sh
   # Ejecutar Migraciones
   python manage.py migrate

   # Ejecutar el Servidor de Desarrollo
   python manage.py runserver
   ```
4. Ahora puedes acceder a la aplicación en http://127.0.0.1:8000/redoc/.

## Documentación
- Django: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
- Django Rest Framework: [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
- PostgreSQL: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)
- Vercel: [https://vercel.com/docs](https://vercel.com/docs)

## Contribuir
Si deseas contribuir al proyecto, por favor revisa las guías de contribución.

## Licencia
Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.
