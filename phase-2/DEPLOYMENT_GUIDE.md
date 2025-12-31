# Complete Deployment Guide - Hackathon TODO App

Deploy your complete full-stack todo application to production (100% FREE).

## 🎯 Deployment Stack

- **Database**: Neon PostgreSQL (Free tier)
- **Backend**: Railway (Free tier) or Render (Free tier)
- **Frontend**: Vercel (Free tier)

Total Cost: **FREE** ✅

---

## Step 1: Database Deployment (Neon)

### 1.1 Create Neon Account
```
1. Go to: https://console.neon.tech
2. Sign up with GitHub
3. Click "Create a project"
```

### 1.2 Project Setup
```
Project name: hackathon-todo
Database name: todo_db
Region: Select closest region
PostgreSQL version: 16
```

### 1.3 Copy Connection String
After project creation, copy the connection string:
```
postgresql://user:password@ep-xxx-xxx.region.aws.neon.tech/todo_db?sslmode=require
```

**Save this - you'll need it for backend deployment!**

✅ Database Status: READY

---

## Step 2: Backend Deployment (Railway)

### 2.1 Prepare Backend

Create `railway.json` in `backend/` folder:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

Create `Procfile` in `backend/` folder:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Update `backend/.env.example`:
```env
# Database Configuration
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRY_HOURS=24

# Application Configuration
ENV=production
DEBUG=False
```

### 2.2 Deploy to Railway

1. **Create Railway Account**:
   - Go to: https://railway.app
   - Click "Login with GitHub"
   - Authorize Railway

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - If first time: Connect your GitHub account
   - Search and select your repository
   - Select `phase-2/backend` as root directory

3. **Configure Environment Variables**:
   Click on your deployment → Variables → Add variables:
   ```
   DATABASE_URL = postgresql://user:password@ep-xxx.neon.tech/todo_db?sslmode=require
   JWT_SECRET_KEY = your-super-secret-32-char-minimum-key
   JWT_ALGORITHM = HS256
   JWT_EXPIRY_HOURS = 24
   ENV = production
   DEBUG = False
   PORT = 8000
   ```

4. **Configure CORS** (Important!):
   You'll update this after frontend deployment with your Vercel URL.

5. **Get Backend URL**:
   - After deployment, Railway will give you a URL like:
   ```
   https://your-app.up.railway.app
   ```
   - **Save this URL!**

6. **Verify Deployment**:
   ```
   Visit: https://your-app.up.railway.app/health
   Should show: {"status":"ok","database":"connected"}
   ```

✅ Backend Status: DEPLOYED

---

## Step 3: Frontend Deployment (Vercel)

### 3.1 Prepare Frontend

Create `vercel.json` in `frontend/` folder:
```json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "outputDirectory": ".next"
}
```

Update `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=https://your-app.up.railway.app
```

### 3.2 Deploy to Vercel

1. **Create Vercel Account**:
   - Go to: https://vercel.com
   - Click "Sign Up"
   - Choose "Continue with GitHub"

2. **Import Project**:
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Vercel will auto-detect Next.js

3. **Configure Project**:
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `frontend`
   - Click "Edit" next to Root Directory
   - Select `phase-2/frontend`

4. **Environment Variables**:
   Click "Environment Variables" and add:
   ```
   Name: NEXT_PUBLIC_API_URL
   Value: https://your-app.up.railway.app
   ```

5. **Deploy**:
   - Click "Deploy"
   - Wait 1-2 minutes for build
   - Vercel will give you a URL like:
   ```
   https://your-app.vercel.app
   ```

✅ Frontend Status: DEPLOYED

---

## Step 4: Connect Everything

### 4.1 Update Backend CORS

Go back to Railway → Your Backend → Variables

Update or add CORS origins:
```python
# In app/main.py, CORS should allow your Vercel URL
```

Add environment variable in Railway:
```
ALLOWED_ORIGINS = https://your-app.vercel.app,https://your-app-git-*.vercel.app,https://*.vercel.app
```

Or directly update `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-app.vercel.app",
        "https://*.vercel.app"  # For preview deployments
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)
```

**Redeploy backend** after CORS update.

### 4.2 Update Frontend API URL

If you didn't add environment variable in Vercel:
- Go to Vercel Dashboard
- Select your project
- Settings → Environment Variables
- Add:
  ```
  NEXT_PUBLIC_API_URL = https://your-app.up.railway.app
  ```
- Redeploy from Deployments tab

---

## Step 5: Test Complete Deployment

### 5.1 Backend Health Check
```
Visit: https://your-app.up.railway.app/health
Expected: {"status":"ok","database":"connected"}
```

### 5.2 API Documentation
```
Visit: https://your-app.up.railway.app/docs
Should show Swagger UI with all endpoints
```

### 5.3 Frontend Testing
```
1. Visit: https://your-app.vercel.app
2. Register new account
3. Login
4. Create tasks
5. Test all features (edit, delete, search, checkbox)
```

### 5.4 Database Verification
```
1. Go to Neon console
2. Check Tables → should see users and tasks tables
3. Check data in tables
```

---

## 🎉 Deployment Complete!

Your app is now live at:
- **Frontend**: https://your-app.vercel.app
- **Backend API**: https://your-app.up.railway.app
- **API Docs**: https://your-app.up.railway.app/docs
- **Database**: Neon Cloud

---

## 📊 Deployment Checklist

- [ ] Neon database created and connected
- [ ] Backend deployed to Railway
- [ ] Backend health check passing
- [ ] Frontend deployed to Vercel
- [ ] Environment variables configured
- [ ] CORS updated with production URLs
- [ ] Registration working
- [ ] Login working
- [ ] Tasks CRUD working
- [ ] Search working
- [ ] Checkboxes working

---

## 🔧 Troubleshooting

### Backend deployment fails
- Check `requirements.txt` is present
- Verify Python version compatibility
- Check Railway build logs
- Ensure all environment variables are set

### Frontend can't connect to backend
- Check `NEXT_PUBLIC_API_URL` is correct
- Verify CORS is configured correctly
- Check browser console for errors
- Test backend URL directly in browser

### Database connection fails
- Verify DATABASE_URL is correct
- Check Neon project is active (not suspended)
- Ensure `?sslmode=require` is in connection string
- Check Neon usage limits

### CORS errors
- Add your Vercel URL to backend CORS
- Include wildcard for preview deployments: `https://*.vercel.app`
- Redeploy backend after CORS changes

---

## 🚀 CI/CD (Automatic Deployments)

### Vercel
✅ **Auto-deploys** on every push to main branch
✅ **Preview deployments** for pull requests
✅ **Rollback** to previous deployments anytime

### Railway
✅ **Auto-deploys** on every push (if GitHub connected)
✅ **Environment-specific** deployments
✅ **Instant rollback**

---

## 📈 Monitoring

### Railway Dashboard
- View logs in real-time
- Monitor resource usage
- Check deployment history
- View metrics

### Vercel Analytics
- Page views
- Performance metrics
- Error tracking
- User analytics

### Neon Dashboard
- Database size
- Query performance
- Connection count
- Storage usage

---

## 💰 Free Tier Limits

### Neon (Database)
- ✅ 0.5 GB storage
- ✅ 100 concurrent connections
- ✅ 10 branches
- ⚠️ Suspends after inactivity (wakes on first request)

### Railway (Backend)
- ✅ $5 free credit/month
- ✅ 500 hours execution time
- ✅ 100 GB bandwidth
- ⚠️ Requires credit card for verification

### Vercel (Frontend)
- ✅ 100 GB bandwidth
- ✅ Unlimited deployments
- ✅ 6,000 build minutes
- ✅ No credit card needed

---

## 🔐 Security Checklist

- [ ] JWT secret is strong (32+ characters)
- [ ] DEBUG=False in production
- [ ] CORS only allows your domain
- [ ] Database connection uses SSL
- [ ] Passwords are hashed (bcrypt)
- [ ] Environment variables not in code
- [ ] .env files in .gitignore

---

## 📱 Custom Domain (Optional)

### Vercel
1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. SSL certificate auto-generated

### Railway
1. Go to Settings → Networking
2. Add custom domain
3. Update DNS CNAME record
4. SSL certificate auto-generated

---

## 🎯 Next Steps

1. **Share your app** - Send link to team/users
2. **Monitor usage** - Check dashboards regularly
3. **Add features** - Deploy updates automatically
4. **Scale up** - Upgrade plans when needed
5. **Add analytics** - Track user behavior

---

## 📞 Support Resources

- **Railway**: https://railway.app/help
- **Vercel**: https://vercel.com/support
- **Neon**: https://neon.tech/docs
- **Community**: Discord servers for each platform

---

**Congratulations! Your app is now live! 🎉**

Share your deployment URLs:
- Frontend: ___________________________
- Backend: ____________________________
- Docs: _______________________________
