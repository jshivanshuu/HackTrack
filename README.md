# HackTrack 🛡️

HackTrack is a highly responsive, continuous threat detection platform designed to mitigate simple web vulnerabilities and anomalies. It monitors your network in real-time, scanning logs for attack patterns (e.g., SQL Injection, XSS) and processing threats asynchronously using FastAPI's background tasks and an LLM-powered pipeline to generate actionable human-readable explanations.

## 🚀 Key Features

*   **API Gateway & Ingestion System**: Intercepts high-throughput web traffic metrics securely via API Keys.
*   **Asynchronous Detection Engine**: Non-blocking `BackgroundTasks` analyze raw logs out-of-band for threat pattern signatures.
*   **Rule-Based Analysis**: Fast tracking and detection mechanisms for standard SQL Injection (SQLi) and Cross-Site Scripting (XSS).
*   **Google Gemini AI Scrutiny**: Malicious payloads are dispatched to Gemini flash models to generate concise summary reports and fix-suggestions for developers. 
*   **Data Storage**: Utilizes SQLAlchemy with SQLite to persist network traffic data, authentication keys, and threat matrices efficiently.
*   **Interactive Cyber-Dashboard**: Built with React, Vite, and TailwindCSS providing graphical data tracking and a real-time command-line-styled terminal for tracking live incoming threats across two separate active views.

---

## 🏗️ System Architecture 

1. **Client SDK Layer**: Users integrate an SDK or express-middleware in their sites that captures HTTP request details (IP, Method, Payload) and forwards it to HackTrack.
2. **Backend**: FastAPI web server running locally that handles `/api/v1/ingest`.
3. **Database**: Lightweight Zero-Config SQLite setup `hacktrack.db`. 
4. **Dashboard**: Independent frontend that natively polls FastAPI for visualization using dynamic charts (Recharts) and glassmorphism UI styles.

---

## 🛠️ Installation & Setup

### Prerequisites
* Python 3.9+
* Node.js & npm (for the frontend React application)
* A valid Google Gemini API Key 

### 1. Backend Server Setup
1. Open a terminal and navigate to the backend directory:
   ```powershell
   cd backend
   ```
2. Spawn a virtual environment and activate it:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Install the dependencies:
   ```powershell
   pip install fastapi uvicorn sqlalchemy pydantic-settings python-multipart google-generativeai
   ```
4. Assign your API key in `backend/ai_service.py` to enable intelligent analysis overrides:
   ```python
   GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY") 
   ```
5. Initialize the SQLite DB Schema alongside test API Keys:
   ```powershell
   python init_db.py
   ```
6. Spin up the FastAPI Gateway!
   ```powershell
   uvicorn main:app --reload --port 8080
   ```

### 2. Frontend Real-Time Dashboard Setup
1. Open up a brand **new** terminal tab from the root HackTrack directory, navigating to the dashboard:
   ```powershell
   cd frontend
   ```
2. Install necessary JavaScript dependencies (TailwindCSS, React, Axios, Recharts, Lucide-React):
   ```powershell
   npm install
   ```
3. Launch the Vite Development Server:
   ```powershell
   npm run dev
   ```
*Access your secure HackTrack dashboard via http://localhost:5173/ !*

---

## 🧪 Simulating Traffic & Attacks

We have provided a native python simulation script `simulate_traffic.py` included in the root directory that randomly blasts the API Gateway with both normal generic endpoints (`/dashboard`, `/profile`) and highly targeted malicious payloads (Using XSS payload syntax or raw SQLi input syntax). 

To test your dashboard visualizations under stress:
1. Ensure your backend and frontend are actively running in separate terminals.
2. In a third terminal window:
   ```powershell
   .\backend\.venv\Scripts\activate
   python simulate_traffic.py
   ```
*(Note: Be sure `API_URL` matching the python script aligns with your Backend port choice (ie. 8080 or 8000).)*