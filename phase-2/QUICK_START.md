# Quick Start Guide - Hackathon TODO App

Complete setup guide for the hackathon todo application with Neon database.

## 🚀 Quick Setup (5 minutes)

### 1. Neon Database Setup

```bash
# 1. Go to https://console.neon.tech
# 2. Create project: "hackathon-todo"
# 3. Copy the connection string (looks like this):
postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Update .env file
# Replace DATABASE_URL with your Neon connection string:
DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies (if not done)
pip install -r requirements.txt

# Start backend server
python -m uvicorn app.main:app --reload
```

Server will start at: **http://localhost:8000**
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 3. Frontend Setup

```bash
# Open new terminal
# Navigate to frontend
cd frontend

# Install dependencies (if not done)
npm install

# Start development server
npm run dev
```

Frontend will start at: **http://localhost:3000**

## ✅ Verify Setup

1. **Backend Health Check**:
   ```bash
   curl http://localhost:8000/health
   # Should return: {"status":"ok","database":"connected"}
   ```

2. **Test Registration**:
   - Go to: http://localhost:3000
   - Click "Register here"
   - Create account with email & password
   - Should redirect to login

3. **Test Login**:
   - Enter credentials
   - Should redirect to dashboard

4. **Test Task Creation**:
   - Click "ADD" button
   - Fill task details
   - Click "Create Task"
   - Task should appear in dashboard

## 🎨 Features

✅ **Authentication**
- User registration & login
- JWT-based authentication
- Secure password hashing

✅ **Task Management**
- Create tasks
- View all tasks
- Edit tasks
- Delete tasks
- Mark as complete (checkbox)
- Search tasks
- Status badges (Pending, In Progress, Completed)

✅ **Beautiful UI**
- Orange/tan color scheme
- Responsive design
- Loading states
- Error handling
- Delete confirmation modals
- Real-time search

## 📁 Project Structure

```
phase-2/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/v1/         # API endpoints
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── main.py         # App entry point
│   ├── .env                # Environment variables
│   └── requirements.txt    # Python dependencies
│
└── frontend/               # Next.js frontend
    ├── app/                # App router pages
    ├── components/         # Reusable components
    ├── lib/                # API client & utilities
    └── types/              # TypeScript types
```

## 🔧 Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://...  # Neon connection string
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRY_HOURS=24
ENV=development
DEBUG=True
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🐛 Troubleshooting

### Backend won't start
- Check if port 8000 is available
- Verify DATABASE_URL is correct
- Check virtual environment is activated

### Frontend won't start
- Check if port 3000 is available
- Run `npm install` again
- Clear `.next` folder: `rm -rf .next`

### Database connection failed
- Verify Neon project is active
- Check connection string has `?sslmode=require`
- Ensure no extra spaces in .env

### Can't register/login
- Check backend is running
- Verify CORS is configured (localhost:3000)
- Check browser console for errors

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Login & get JWT token

### Tasks (Requires JWT)
- `GET /api/tasks` - List all tasks
- `POST /api/tasks` - Create task
- `GET /api/tasks/{id}` - Get task by ID
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

## 🎯 Development Workflow

1. **Make changes to backend**:
   - Edit files in `backend/app/`
   - Server auto-reloads (--reload flag)
   - Check http://localhost:8000/docs for API

2. **Make changes to frontend**:
   - Edit files in `frontend/`
   - Next.js auto-reloads
   - Changes reflect immediately

3. **Database changes**:
   - Modify models in `backend/app/models/`
   - Restart backend to recreate tables (dev only)
   - For production: use Alembic migrations

## 🚢 Deployment Tips

- Set `DEBUG=False` in production
- Use proper JWT secret (32+ chars)
- Update CORS origins for production URL
- Use Alembic for database migrations
- Consider using Vercel for frontend
- Backend can deploy to Railway, Render, or fly.io

## 📖 Documentation

- Detailed setup: `NEON_SETUP.md`
- API documentation: http://localhost:8000/docs
- Neon docs: https://neon.tech/docs

---

**Happy Coding! 🎉**
