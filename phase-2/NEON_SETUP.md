# Neon Database Setup Guide

This guide will help you set up Neon PostgreSQL database for the hackathon-todo project.

## Prerequisites
- Neon account (https://neon.tech)
- Project already has `psycopg2-binary` installed ✅

## Step 1: Create Neon Project

1. Go to https://console.neon.tech
2. Click "Create a project"
3. Enter project details:
   - **Project name**: `hackathon-todo`
   - **Database name**: `todo_db` (default is fine)
   - **Region**: Select closest to you for best performance
   - **PostgreSQL version**: 16 (latest)

4. Click "Create project"

## Step 2: Get Connection String

After creating the project, Neon will show you a connection string. It looks like:

```
postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/todo_db?sslmode=require
```

**Important**: Copy this connection string immediately as the password is only shown once!

## Step 3: Update Backend Configuration

1. Open `backend/.env` file

2. Replace the DATABASE_URL with your Neon connection string:

```env
# Database Configuration - Neon PostgreSQL
DATABASE_URL=postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/todo_db?sslmode=require

# JWT Configuration
JWT_SECRET_KEY=test-secret-key-minimum-32-characters-long-for-hs256
JWT_ALGORITHM=HS256
JWT_EXPIRY_HOURS=24

# Application Configuration
ENV=development
DEBUG=True
```

3. Save the file

## Step 4: Initialize Database Tables

The backend will automatically create tables on startup (in development mode).

1. Navigate to backend directory:
```bash
cd backend
```

2. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. Run the backend:
```bash
python -m uvicorn app.main:app --reload
```

The database tables will be created automatically on first run!

## Step 5: Verify Database Connection

1. Check backend logs for successful connection
2. Visit: http://localhost:8000/health
   - Should show: `{"status": "ok", "database": "connected"}`

3. Check Neon Console:
   - Go to your project dashboard
   - Click "Tables" in sidebar
   - You should see 2 tables:
     - `users`
     - `tasks`

## Troubleshooting

### Connection Failed
- ✅ Check if connection string is correct (no extra spaces)
- ✅ Ensure `sslmode=require` is at the end
- ✅ Verify Neon project is not suspended (free tier)

### Tables Not Created
- ✅ Make sure `DEBUG=True` in .env
- ✅ Check backend logs for errors
- ✅ Restart backend server

### Password Not Working
- ✅ Neon passwords contain special characters - make sure they're URL encoded
- ✅ If lost, reset database password in Neon console

## Connection String Format

```
postgresql://<user>:<password>@<host>/<database>?sslmode=require
```

Example:
```
postgresql://myuser:mypass123@ep-cool-mouse-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

## Neon Free Tier Limits

- ✅ **Storage**: 0.5 GB
- ✅ **Compute**: 0.25 vCPU
- ✅ **Connections**: 100 concurrent
- ✅ **Branches**: 10
- ✅ **Always-on**: No (suspends after inactivity)

Perfect for development and hackathon projects!

## Next Steps

After database is set up:

1. ✅ Start backend: `python -m uvicorn app.main:app --reload`
2. ✅ Start frontend: `npm run dev` (in frontend directory)
3. ✅ Test registration and login
4. ✅ Create some tasks to verify database persistence

## Support

- Neon Documentation: https://neon.tech/docs
- Neon Discord: https://discord.gg/neon
- Project Issues: File in GitHub repo

---

**Note**: Never commit `.env` file to version control! It's already in `.gitignore`.
