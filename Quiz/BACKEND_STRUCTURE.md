# AI Quiz Platform - Backend Structure (Python FastAPI)

## Directory Layout

```
backend_py/
├── Dockerfile
├── requirements.txt
├── .env.example
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── db.py                # Database connection setup
│   ├── models.py            # SQLModel database models
│   ├── lib/
│   │   ├── redis_client.py  # Redis setup + OTP uniqueness checks
│   │   ├── emailjs_client.py # EmailJS HTTP client
│   ├── services/
│   │   ├── otp_service.py   # OTP generation, verification, rate-limiting
│   │   ├── quiz_service.py  # (To be created) Quiz randomization logic
│   │   ├── sandbox_service.py # (To be created) Code execution wrapper
│   ├── routes/
│   │   ├── auth.py          # Register, Login, Verify OTP, CSRF
│   │   ├── questions.py     # (To be created) Get random questions
│   │   ├── submissions.py   # (To be created) Submit code, receive jobs
│   │   ├── admin.py         # (To be created) Admin endpoints
│   │   ├── leaderboard.py   # (To be created) Leaderboard queries
│   ├── middleware/
│   │   ├── jwt_middleware.py # (To be created) JWT verification
│   │   ├── anti_cheat.py    # (To be created) Tab-switch, copy-paste detection
│   │   ├── rate_limit.py    # (To be created) Rate limiter middleware
│   ├── workers/
│   │   ├── sandbox_worker.py # (To be created) Celery: execute code in sandbox
│   │   ├── plagiarism_worker.py # (To be created) Celery: AST-based plagiarism check
├── celery_app.py             # Celery configuration + task registry
├── docker-compose.yml        # (At root: services for Postgres, Redis, backend, worker, frontend)
```

## Flow Overview

1. **Registration**: User registers → OTP sent via EmailJS → OTP verified → User account created
2. **Login**: User logs in → JWT tokens issued
3. **Quiz Start**: User selects language + level → Backend fetches randomized questions → Quiz displayed
4. **Code Submission**: User submits code → Celery job queued → Worker runs code in sandbox → AI feedback generated
5. **Results**: Backend computes score, stores in DB, updates leaderboard

## Key Implementation Notes

### OTP System
- Alphanumeric (6 chars): `A9K3X7`, `Z12PQR`, etc.
- Non-repeating: Last 20k hashes stored in Redis set + HMAC-deterministic check
- Bcrypt-hashed in DB
- 5-minute expiry
- Rate-limited: 3 per hour per email
- Max 5 attempts before lockout

### Database (PostgreSQL)
- Tables: `User`, `OTP`, `Question`, `Quiz`, `Submission`, `Leaderboard`, `AuditLog`
- Migrations: Use Alembic (to be set up)

### Redis (Caching + Job Queue)
- Stores OTP uniqueness set
- BullMQ (Node.js) replaced by Celery + Redis
- Broker: Redis DB 1
- Backend: Redis DB 2

### Sandbox Execution (Docker-in-Docker)
- Languages: Python, Java, C, C++, R, JavaScript
- Timeout: 2 seconds per testcase
- Memory: 256MB
- Network/filesystem: Disabled
- Worker: Celery task that calls Docker API

### Admin Credentials
- Username: `vish123`
- Password: `1914581`

## Setup (Windows cmd)

1. Copy `.env.example` to `.env` in `backend_py/`
2. Start Docker: `docker-compose up --build`
3. Backend available at `http://localhost:4000`
4. Frontend available at `http://localhost:3000`

## API Endpoints

### Auth
- `GET /api/auth/csrf` → Get CSRF token
- `POST /api/auth/register` → Register user + send OTP
- `POST /api/auth/verify-otp` → Verify OTP (requires CSRF token in header)
- `POST /api/auth/login` → Login (returns JWT access/refresh tokens)

### Questions (To be created)
- `GET /api/questions/random?language=python&level=beginner&count=10` → Get randomized questions

### Submissions (To be created)
- `POST /api/submissions` → Submit code (queues Celery job)

### Admin (To be created)
- `POST /api/admin/questions` → Add question
- `GET /api/admin/questions` → List all questions
- `PUT /api/admin/questions/{id}` → Edit question
- `DELETE /api/admin/questions/{id}` → Delete question

## Testing the Backend Locally

```bash
# Start services
docker-compose up --build

# In another terminal, test registration
curl -X POST http://localhost:4000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"pass123"}'
```

## To Complete

- [ ] Alembic migrations
- [ ] Question randomization service
- [ ] Sandbox worker + Docker execution
- [ ] AI feedback service (OpenAI integration)
- [ ] Admin routes
- [ ] Anti-cheat middleware
- [ ] Leaderboard endpoints
- [ ] Email template customization
