# Deployment Checklist ✅

Quick checklist for deploying your hackathon todo app to production.

## Pre-Deployment

- [ ] Code committed to GitHub
- [ ] All features tested locally
- [ ] Environment variables documented
- [ ] README updated with project info
- [ ] .gitignore includes .env files

---

## Step 1: Database (Neon) - 5 mins

- [ ] Go to https://console.neon.tech
- [ ] Create account (sign in with GitHub)
- [ ] Create new project: "hackathon-todo"
- [ ] Copy connection string
- [ ] Save connection string securely
- [ ] Verify database is active

**Connection String Format:**
```
postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
```

---

## Step 2: Backend (Railway) - 10 mins

### Files Created ✅
- [x] `backend/railway.json`
- [x] `backend/Procfile`
- [x] `backend/.env.example`

### Railway Deployment Steps
- [ ] Go to https://railway.app
- [ ] Sign in with GitHub
- [ ] Click "New Project"
- [ ] Select "Deploy from GitHub repo"
- [ ] Connect your GitHub repository
- [ ] Select `phase-2/backend` as root directory

### Environment Variables to Add
- [ ] `DATABASE_URL` = (your Neon connection string)
- [ ] `JWT_SECRET_KEY` = (32+ character secret key)
- [ ] `JWT_ALGORITHM` = HS256
- [ ] `JWT_EXPIRY_HOURS` = 24
- [ ] `ENV` = production
- [ ] `DEBUG` = False
- [ ] `PORT` = 8000

### Verify Deployment
- [ ] Build completes successfully
- [ ] Copy Railway URL (e.g., `https://your-app.up.railway.app`)
- [ ] Test health endpoint: `/health`
- [ ] Check API docs: `/docs`

**Backend URL:** _____________________________________

---

## Step 3: Frontend (Vercel) - 5 mins

### Files Created ✅
- [x] `frontend/vercel.json`
- [x] `frontend/.env.local` (local only, not committed)

### Vercel Deployment Steps
- [ ] Go to https://vercel.com
- [ ] Sign in with GitHub
- [ ] Click "Add New..." → "Project"
- [ ] Import your GitHub repository
- [ ] Framework: Next.js (auto-detected)
- [ ] Root Directory: `phase-2/frontend`

### Environment Variables to Add
- [ ] `NEXT_PUBLIC_API_URL` = (your Railway backend URL)

### Verify Deployment
- [ ] Build completes successfully
- [ ] Copy Vercel URL (e.g., `https://your-app.vercel.app`)
- [ ] Visit site and test UI

**Frontend URL:** _____________________________________

---

## Step 4: Connect Everything

### Update Backend CORS
- [ ] Go to Railway → Your project → Variables
- [ ] OR update `backend/app/main.py` allowed_origins:
  ```python
  allowed_origins = [
      "http://localhost:3000",
      "https://your-app.vercel.app",
      "https://your-app-*.vercel.app"  # Preview deployments
  ]
  ```
- [ ] Redeploy backend (if code changed)

### Verify CORS
- [ ] Frontend can call backend APIs
- [ ] No CORS errors in browser console

---

## Step 5: Testing

### Complete User Flow Test
- [ ] Visit your Vercel URL
- [ ] Click "Register here"
- [ ] Create new account (use real email format)
- [ ] Login with credentials
- [ ] Create a task
- [ ] Edit a task
- [ ] Mark task as complete (checkbox)
- [ ] Search for tasks
- [ ] Delete a task
- [ ] Logout and login again
- [ ] Verify data persists

### Backend Testing
- [ ] `/health` shows "connected"
- [ ] `/docs` loads Swagger UI
- [ ] All endpoints return proper responses
- [ ] Authentication works
- [ ] Database queries successful

### Database Verification
- [ ] Go to Neon console
- [ ] Check Tables → `users` table exists
- [ ] Check Tables → `tasks` table exists
- [ ] View data in tables
- [ ] Verify user isolation working

---

## Step 6: Polish & Share

### Documentation
- [ ] Update README with live URLs
- [ ] Add screenshots to README
- [ ] Document any deployment issues
- [ ] Update project description

### Share Your App
- [ ] Test on mobile device
- [ ] Share URL with team/friends
- [ ] Collect feedback
- [ ] Fix any critical bugs

### Monitoring Setup
- [ ] Check Railway dashboard (logs, metrics)
- [ ] Check Vercel analytics
- [ ] Check Neon database usage
- [ ] Set up alerts (optional)

---

## Live URLs (Fill after deployment)

### Production URLs
- **Frontend**: https://_________________________________
- **Backend API**: https://_________________________________
- **API Docs**: https://_________________________________/docs
- **Database**: Neon Dashboard (https://console.neon.tech)

### GitHub Repository
- **Repo URL**: https://_________________________________

---

## Troubleshooting

### Backend deployment fails
- [ ] Check build logs in Railway
- [ ] Verify all environment variables set
- [ ] Check `requirements.txt` is valid
- [ ] Ensure Python version compatible

### Frontend can't connect to backend
- [ ] Verify `NEXT_PUBLIC_API_URL` is correct
- [ ] Check backend CORS includes Vercel URL
- [ ] Test backend URL directly in browser
- [ ] Check browser console for errors

### Database connection issues
- [ ] Verify `DATABASE_URL` format is correct
- [ ] Check `?sslmode=require` is present
- [ ] Ensure Neon project is active
- [ ] Test connection from Railway logs

### CORS errors
- [ ] Add Vercel URL to backend CORS
- [ ] Include wildcard for preview: `https://*.vercel.app`
- [ ] Redeploy backend after changes
- [ ] Clear browser cache

---

## Post-Deployment

### Security Review
- [ ] JWT secret is strong (32+ characters)
- [ ] DEBUG is False in production
- [ ] No .env files committed
- [ ] Database credentials secure
- [ ] CORS properly configured

### Performance Check
- [ ] Frontend loads quickly
- [ ] API responses are fast
- [ ] No console errors
- [ ] Mobile responsive works

### Backup & Recovery
- [ ] Document deployment steps
- [ ] Save all environment variables securely
- [ ] Note all platform credentials
- [ ] Test rollback process

---

## Next Steps

- [ ] Add custom domain (optional)
- [ ] Set up CI/CD (auto-deploy on push)
- [ ] Add analytics/monitoring
- [ ] Implement additional features
- [ ] Scale resources if needed

---

## Support Resources

- **Railway**: https://railway.app/help
- **Vercel**: https://vercel.com/support
- **Neon**: https://neon.tech/docs
- **Deployment Guide**: See `DEPLOYMENT_GUIDE.md`

---

**Deployment Status**

- [ ] Database: Deployed ✅
- [ ] Backend: Deployed ✅
- [ ] Frontend: Deployed ✅
- [ ] Connected: Working ✅
- [ ] Tested: Verified ✅

**Date Deployed**: _____________________

**Deployed By**: _____________________

---

🎉 **Congratulations! Your app is live!** 🎉
