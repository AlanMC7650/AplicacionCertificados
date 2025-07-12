# 🧠 Flask Project

Este proyecto es una aplicación web construida con **Flask + PostgreSQL** siguiendo una estructura **profesional y escalable**.  
Incluye Blueprints, controladores, validadores, migraciones, templates y todo lo necesario para backend y frontend integrados.

---

## ⚙️ Tecnologías principales

- Python 3.11
- Flask
- SQLAlchemy
- PostgreSQL
- Flask-Migrate
- Flask-CORS
- Jinja2 (para frontend)
- dotenv (variables de entorno)

---

## 🚀 Estructura del proyecto

```plaintext
awesome-project/
├── .gitignore
├── .env.example
├── requirements.txt
├── README.md
├── docker-compose.yml        ← opcional (contenedor DB)
├── manage.py                 ← comandos personalizados
├── setup.cfg                 ← linters y formatos
│
├── app/
│   ├── __init__.py           ← create_app(), registros
│   ├── config.py             ← configuración por entorno
│   ├── extensions.py         ← db, migrate, cors
│   ├── models/               ← modelos ORM (User, Post…)
│   ├── controllers/          ← lógica de negocio
│   ├── api/                  ← rutas JSON (blueprints)
│   ├── views/                ← rutas HTML
│   ├── templates/            ← HTML Jinja2
│   ├── static/               ← CSS, JS, imágenes
│   ├── schemas/              ← validación de datos
│   └── migrations/           ← autogenerado por Flask-Migrate
│
├── tests/                    ← pruebas unitarias
└── docs/                     ← swagger.json, diagramas, etc.
