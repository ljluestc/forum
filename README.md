# Forum App (Flask + React on Railway)

A real-time forum displaying book prices from AbeBooks.

## Setup
1. **Backend**: `cd backend`, set `.env` with `DATABASE_URL` and `SECRET_KEY`.
2. **Frontend**: `cd frontend`, set `.env` with `REACT_APP_API_URL`, run `npm install`.
3. **Run Locally**: 
   - Backend: `python app.py`
   - Frontend: `npm start`
4. **Deploy on Railway**:
   - Push to GitHub.
   - Link repo to Railway, set `DATABASE_URL` (PostgreSQL), `PORT=5000`.

## Notes
- Uses Flask-SocketIO for real-time book price updates.
- Scrapes AbeBooks (replace with real ISBNs).