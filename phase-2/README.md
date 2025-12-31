# Hackathon TODO App 🚀

A modern full-stack todo application with authentication, built for hackathons.

![Tech Stack](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)

## ✨ Features

### 🔐 Authentication
- User registration with email validation
- Secure login with JWT tokens
- Password hashing with bcrypt
- Protected routes and API endpoints

### ✅ Task Management
- Create, read, update, delete tasks
- Mark tasks as complete with checkboxes
- Real-time search functionality
- Status badges (Pending, In Progress, Completed)
- Task descriptions and timestamps

### 🎨 Beautiful UI
- Modern orange/tan color scheme
- Responsive design
- Loading states and error handling
- Delete confirmation modals
- Clean, minimal aesthetic

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (Neon)
- **ORM**: SQLModel
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt
- **Validation**: Pydantic

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **API Client**: Fetch API
- **State Management**: React Hooks

### Database
- **Development**: SQLite (local)
- **Production**: Neon PostgreSQL (serverless)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Git

### Local Development

#### 1. Clone Repository
```bash
git clone <your-repo-url>
cd phase-2
```

#### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration

# Run backend
python -m uvicorn app.main:app --reload
```

Backend runs at: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

#### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run frontend
npm run dev
```

Frontend runs at: http://localhost:3000

## 📦 Deployment

### Complete Deployment Guide
See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete step-by-step instructions.

### Quick Deployment

#### 1. Database (Neon)
```bash
# Go to https://console.neon.tech
# Create project: "hackathon-todo"
# Copy connection string
```

#### 2. Backend (Railway)
```bash
# Go to https://railway.app
# Deploy from GitHub
# Set environment variables
# Deploy!
```

#### 3. Frontend (Vercel)
```bash
# Go to https://vercel.com
# Import GitHub repository
# Set NEXT_PUBLIC_API_URL
# Deploy!
```

## 📁 Project Structure

```
phase-2/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/v1/            # API endpoints
│   │   │   ├── auth.py        # Authentication routes
│   │   │   └── tasks.py       # Task CRUD routes
│   │   ├── models/            # Database models
│   │   │   ├── user.py        # User model
│   │   │   └── task.py        # Task model
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── db/                # Database configuration
│   │   ├── config.py          # App configuration
│   │   └── main.py            # FastAPI app
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables (local)
│   ├── .env.example           # Environment template
│   ├── railway.json           # Railway config
│   └── Procfile              # Process file
│
├── frontend/                  # Next.js frontend
│   ├── app/                   # App router pages
│   │   ├── page.tsx          # Login page
│   │   ├── register/         # Registration page
│   │   ├── dashboard/        # Main dashboard
│   │   └── tasks/            # Task pages
│   ├── components/           # Reusable components
│   │   └── tasks/            # Task components
│   ├── lib/                  # Utilities
│   │   └── task-api.ts       # API client
│   ├── types/                # TypeScript types
│   ├── .env.local            # Environment variables (local)
│   └── vercel.json           # Vercel config
│
├── DEPLOYMENT_GUIDE.md       # Complete deployment guide
├── NEON_SETUP.md            # Neon database setup
├── QUICK_START.md           # Quick start guide
└── README.md                # This file
```

## 🔌 API Endpoints

### Authentication
```
POST /api/auth/register  - Create new account
POST /api/auth/login     - Login and get JWT token
```

### Tasks (Protected)
```
GET    /api/tasks        - List all user tasks
POST   /api/tasks        - Create new task
GET    /api/tasks/{id}   - Get single task
PUT    /api/tasks/{id}   - Update task
DELETE /api/tasks/{id}   - Delete task
```

### System
```
GET /                    - API info
GET /health             - Health check
GET /docs               - Swagger UI
GET /redoc              - ReDoc
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🔒 Security Features

- ✅ Password hashing with bcrypt
- ✅ JWT token authentication
- ✅ Protected API routes
- ✅ User data isolation
- ✅ SQL injection prevention (SQLModel)
- ✅ XSS protection (React)
- ✅ CORS configuration
- ✅ Environment variable security

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(2000),
    status VARCHAR(20) DEFAULT 'pending',
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## 🎯 Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRY_HOURS=24
ENV=production
DEBUG=False
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

## 📝 Development

### Adding New Features
1. Create feature branch
2. Implement backend endpoint
3. Create frontend component
4. Test locally
5. Deploy to staging
6. Merge to main

### Code Style
- Backend: Follow PEP 8
- Frontend: ESLint + Prettier
- TypeScript: Strict mode enabled

## 🐛 Troubleshooting

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md#troubleshooting) for common issues and solutions.

## 📚 Documentation

- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Complete deployment instructions
- [Neon Setup](NEON_SETUP.md) - Database setup guide
- [Quick Start](QUICK_START.md) - Quick reference guide
- [API Docs](http://localhost:8000/docs) - Swagger UI (when running)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License - feel free to use for your projects!

## 🙏 Acknowledgments

- FastAPI for amazing backend framework
- Next.js for powerful frontend framework
- Neon for serverless PostgreSQL
- Railway for easy backend deployment
- Vercel for frontend hosting

## 📞 Support

- Create an issue in the repository
- Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for deployment help
- Review API docs at `/docs` endpoint

---

**Built with ❤️ for Hackathons**

Made by: [Your Name]
Project: Hackathon TODO App
Year: 2025

---

## 🎉 Live Demo

- **Frontend**: https://your-app.vercel.app
- **Backend API**: https://your-app.railway.app
- **API Docs**: https://your-app.railway.app/docs

Happy Coding! 🚀
