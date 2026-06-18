# ATLAS System - Backend

An IT ticketing and issue tracking system built with FastAPI and PostgreSQL, featuring an automated internal Knowledge Base and custom SLA policy enforcement thresholds.

## Core Setup Accomplished

*   **Database Engine Mapping:** Integrated SQLAlchemy object-relational mapping to fully track 11 custom relational tables, data entities, and cascade properties.
*   **Alembic Migrations Configuration:** Enabled localized migration scripts that look up credentials securely via a `.env` environment variables wrapper.
*   **Security & Network Access:** Bound native PostgreSQL encrypted password verification layer to an IPv4 TCP/IP network connection to fully bypass Linux user-matching peer constraints.
*   **Cross-Origin Resource Sharing (CORS):** White-listed common frontend loopback network addresses to provide secure endpoint testing for the React application.
*   **Pre-populated Seeding Pipeline:** Provided an automated operational data generation pipeline to allow automated population of standard SLA thresholds, departments, and support category nodes.

## Local Infrastructure Launch

### 1. Local Dependencies Installation
Navigate to your backend directory and activate your localized virtual environment workspace:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Live Operational Migration Execution
Ensure your PostgreSQL instance is running locally with a database named `atlas_db`, then apply tracking files:
```bash
alembic upgrade head
```

### 3. Pipeline Data Seeding
Run the standalone data generation script to inject mock data points for testing:
```bash
python seed.py
```

### 4. Running the Development Server
```bash
uvicorn app.main:app --reload
```
The live API documentation can be accessed in your browser at: `http://127.0.0`
