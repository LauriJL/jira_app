# PreLegal

Jira sw development Kanban board for PreLegal — tools that help users create legal documents.

## Status

**In progress** — this project is under active development and is expected to be completed in 1 week (by 15 October 2026).

## Mutual NDA creator

A web application that creates a Mutual Non-Disclosure Agreement for a user. The user
enters key information in a form, the site displays the Mutual NDA with that information
filled in, and the user can download the completed document as a Markdown file.

- **Backend:** Python / Django (`backend/`)
- **Frontend:** React (Vite) (`frontend/`)
- **Templates:** Common Paper markdown templates (`templates/`), catalogued in
  `catalog.json` and licensed under CC BY 4.0.

### Run the backend

```console
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The API is served at `http://localhost:8000`. The generation endpoint is
`POST /api/nda/generate/`.

### Run the frontend

```console
cd frontend
npm install
npm run dev
```

The app is served at `http://localhost:3000` and calls the backend at
`VITE_API_URL` (defaults to `http://localhost:8000`).

### Tests

```console
cd backend
python manage.py test
```
