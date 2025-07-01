# ProjectSetup

Dieses Repository bietet eine Vorlage für die Einrichtung eines Projekts mit drei Datenbanken: PostgreSQL, Redis und MongoDB, zusammen mit einem Python Backend und einem Vue.js Frontend. Es enthält Docker-Konfigurationen für einfache Bereitstellung und Verwaltung.

## Anforderungen

- Visual Studio Code
  - Empfohlene Erweiterungen
    - Database Client
    - Docker
    - ESLint
    - Prettier
    - Path Intellisense
    - Python
    - Pylint
    - Vite
    - Vue - Official
- Python 3.10 oder höher
- Git (für Versionskontrolle)
- Docker
- Node.js v22.12.0 (für das Vue.js Frontend)
- Node Version Manager (nvm) (optional, für die Verwaltung von Node.js-Versionen)
- conda (optional, für die Verwaltung von Python-Umgebungen)

### Empfohlene VS Code Einstellungen

Öffnen Sie die settings.json-Datei in VS Code und fügen Sie die folgenden Konfigurationen hinzu. Sie können auf diese Datei zugreifen, indem Sie auf das Zahnradsymbol in der unteren linken Ecke klicken, "Settings" auswählen und dann auf das Symbol "Open Settings (JSON)" in der oberen rechten Ecke klicken.

Fügen Sie die folgende JSON-Konfiguration in Ihre `settings.json`-Datei ein. Falls die Datei bereits einige Einstellungen enthält, können Sie diese mit den vorhandenen zusammenführen.

```json
{
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },
  "[vue]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[jsonl]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnType": true
  },
  "editor.inlineSuggest.enabled": true,
  "eslint.codeActionsOnSave.rules": null,
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "files.autoSave": "afterDelay",
  "[jsonc]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[html]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "typescript.updateImportsOnFileMove.enabled": "always",
  "database-client.autoSync": true,
  "editor.formatOnSave": true,
  "pylint.enabled": true,
  "pylint.args": ["--rcfile=.pylintrc"]
}
```

### Empfohlen bei Verwendung von conda

Wenn Sie conda für die Verwaltung Ihrer Python-Umgebungen verwenden, können Sie den folgenden Befehl verwenden, um eine neue Umgebung mit Python 3.10 zu erstellen:

```bash
conda create -n project_env python=3.10
```

Aktivieren Sie die Umgebung mit:

```bash
conda activate project_env
```

Nach dem Erstellen und Aktivieren der Umgebung können Sie die erforderlichen Python-Pakete mit pip installieren:

```bash
pip install -r requirements.txt
```

Ändern Sie schließlich den Python-Interpreter in VS Code, um die conda-Umgebung zu verwenden. Sie können dies tun, indem Sie die Befehlspalette öffnen (Ctrl+Shift+P), "Python: Select Interpreter" eingeben und den Interpreter aus Ihrer conda-Umgebung auswählen.

## Detaillierte Projektbeschreibung

### Überblick der Architektur

Dieses Projekt ist eine Full-Stack-Webanwendung, die aus einem Python FastAPI Backend, einem Vue.js Frontend und mehreren Datenbanken besteht. Die gesamte Infrastruktur kann über Docker Compose verwaltet werden.

Das Projekt folgt einer modernen Microservice-Architektur:

- **Backend**: FastAPI (Python) - REST API Server
- **Frontend**: Vue.js 3 mit Vuetify - Single Page Application
- **Datenbanken**: PostgreSQL (relationale Daten), MongoDB (Dokumente), Redis (Caching/Sessions)
- **Containerisierung**: Docker & Docker Compose

### Erweiterte Projektstruktur

```
ProjectSetup/
├── backend/                    # Python FastAPI Backend
│   ├── app/                   # Hauptanwendungscode
│   │   ├── __init__.py       # Python Package Marker
│   │   ├── main.py           # FastAPI Anwendungsentry Point
│   │   ├── config.py         # Konfigurationseinstellungen
│   │   ├── database.py       # Datenbankverbindungen (PostgreSQL, MongoDB)
│   │   ├── redis_client.py   # Redis Client Konfiguration
│   │   ├── models.py         # SQLAlchemy/Pydantic Datenmodelle
│   │   ├── schemas.py        # API Schema Definitionen
│   │   ├── routes.py         # API Endpunkt Definitionen
│   │   └── helper.py         # Hilfsfunktionen
│   ├── requirements.txt      # Python Abhängigkeiten
│   ├── .pylintrc            # Pylint Konfiguration für Code-Qualität
│   └── Dockerfile           # Container-Definition für Backend
│
├── frontend/                  # Vue.js 3 Frontend
│   ├── src/                  # Quellcode
│   │   ├── components/       # Wiederverwendbare Vue-Komponenten
│   │   │   ├── articles/     # Artikel-bezogene Komponenten
│   │   │   └── layout/       # Layout-Komponenten (Header, Footer)
│   │   │       ├── HeaderMain.vue    # Hauptnavigation
│   │   │       └── FooterMain.vue    # Footer-Komponente
│   │   ├── views/            # Seiten-Komponenten
│   │   │   ├── ViewHome.vue          # Startseite
│   │   │   ├── ViewLogin.vue         # Anmeldeseite
│   │   │   ├── ViewRegister.vue      # Registrierungsseite
│   │   │   ├── ViewPosts.vue         # Beiträge-Übersicht
│   │   │   ├── ViewPostDetail.vue    # Detailansicht für Beiträge
│   │   │   ├── ViewCreatePost.vue    # Beitrag erstellen
│   │   │   ├── ViewStatistics.vue    # Statistiken
│   │   │   └── ViewStatisticsNew.vue # Erweiterte Statistiken
│   │   ├── services/         # API-Service Layer
│   │   │   ├── service.auth.ts      # Authentifizierungsdienste
│   │   │   └── service.blog.ts      # Blog-/Post-Dienste
│   │   ├── model/            # TypeScript Interfaces/Types
│   │   │   ├── User.ts       # Benutzer-Modell
│   │   │   ├── Post.ts       # Beitrag-Modell
│   │   │   └── Token.ts      # Token-Modell
│   │   ├── router/           # Vue Router Konfiguration
│   │   │   └── index.ts      # Routing-Definitionen
│   │   ├── plugins/          # Vue.js Plugins
│   │   │   ├── index.ts      # Plugin-Registration
│   │   │   ├── vuetify.ts    # Vuetify Konfiguration
│   │   │   └── webfontloader.ts # Web Font Loader
│   │   ├── assets/           # Statische Assets
│   │   │   └── settings.scss # SCSS Styling
│   │   ├── enums/            # TypeScript Enums
│   │   │   └── EnumExample.ts # Beispiel Enum
│   │   ├── App.vue           # Haupt-App-Komponente
│   │   ├── main.ts           # Anwendungsentry Point
│   │   └── shims-vue.d.ts    # TypeScript Vue Declarations
│   ├── public/               # Öffentliche Assets
│   │   └── favicon.ico       # Website-Icon
│   ├── package.json          # Node.js Abhängigkeiten und Skripte
│   ├── vite.config.ts        # Vite Build-Tool Konfiguration
│   ├── tsconfig.json         # TypeScript Konfiguration
│   ├── eslint.config.js      # ESLint Code-Qualität Konfiguration
│   ├── index.html            # HTML Entry Point
│   └── README.md             # Frontend-spezifische Dokumentation
│
├── docker-compose.yml         # Multi-Container Orchestrierung
├── README.md                  # Projektdokumentation (diese Datei)
└── .gitignore                # Git Ignore-Regeln
```

### Technologie-Stack

**Backend (Python)**

- **FastAPI**: Modernes, schnelles Web-Framework für APIs
- **SQLAlchemy**: ORM für PostgreSQL-Datenbankoperationen
- **PyMongo**: MongoDB Client für Dokumentendatenbank
- **Redis**: In-Memory Datenbank für Caching und Sessions
- **Pydantic**: Datenvalidierung und -serialisierung
- **Python-JOSE**: JWT Token-Behandlung für Authentifizierung

**Frontend (TypeScript/Vue.js)**

- **Vue.js 3**: Progressive JavaScript Framework
- **Vuetify**: Material Design Komponentenbibliothek
- **Vue Router**: Client-seitige Navigation
- **Axios**: HTTP Client für API-Kommunikation
- **TypeScript**: Typisierte JavaScript-Superset
- **Vite**: Schneller Build-Tool und Dev-Server

**Datenbanken & Infrastructure**

- **PostgreSQL**: Relationale Datenbank für strukturierte Daten
- **MongoDB**: NoSQL-Datenbank für flexible Dokumente
- **Redis**: In-Memory-Store für Caching und Session-Management
- **Docker**: Containerisierung für konsistente Entwicklungsumgebung

### Datenbank-Setup

Das Projekt verwendet drei verschiedene Datenbanksysteme:

1. **PostgreSQL** (Port 5432)

   - Hauptdatenbank für relationale Daten
   - Benutzer: `user`, Passwort: `password`
   - Datenbank: `mydatabase`

2. **MongoDB** (Port 27017)

   - NoSQL-Datenbank für dokumentenbasierte Daten
   - Root-Benutzer: `user`, Passwort: `password`

3. **Redis** (Port 6379)
   - In-Memory-Datenbank für Caching und Sessions
   - Passwort: `password`

### Anwendungsstart

**Mit Docker Compose (empfohlen):**

```bash
docker-compose up -d
```

**Lokale Entwicklung:**

Backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 80
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

### Architektur-Überlegungen

**Microservice-Ansatz**: Jeder Service (Backend, Frontend, Datenbanken) läuft in einem eigenen Container, was Skalierbarkeit und Wartbarkeit verbessert.

**API-First Design**: Das Backend stellt eine RESTful API bereit, die vom Frontend konsumiert wird. Dies ermöglicht es, später mobile Apps oder andere Clients hinzuzufügen.

**Datenbankaufteilung**:

- PostgreSQL für strukturierte, relationale Daten (Benutzer, Posts, etc.)
- MongoDB für flexible, dokumentenbasierte Daten
- Redis für schnelle Zugriffe auf Sessions und Caching

**Entwicklungsfreundlich**: Hot-Reload für beide Anwendungen (Frontend & Backend) während der Entwicklung.
