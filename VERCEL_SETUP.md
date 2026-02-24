# Vercel Deployment Configuration

This document explains the Vercel deployment setup for HostelHub.

## Files Created for Vercel

### 1. **vercel.json**
- Main Vercel configuration file
- Specifies routes, functions configuration, and build commands
- Routes all API requests to `/api/index.py`
- Routes static files from `/frontend/static/`

### 2. **api/index.py**
- Serverless function entry point for all API requests
- Modified FastAPI app that works with Vercel's serverless runtime
- Handles all routes: API endpoints, frontend HTML serving, static files
- Auto-creates database tables on startup

### 3. **requirements.txt** (Updated)
- Dependencies needed for Vercel deployment
- Includes all FastAPI, database, and authentication packages

### 4. **.env.example**
- Template for environment variables
- Shows what variables need to be set in Vercel
- Users copy this and create `.env` for local development

### 5. **.gitignore** (Updated)
- Prevents sensitive files from being committed to GitHub
- Excludes `.env`, `__pycache__`, venv, etc.

### 6. **backend/database.py** (Updated)
- Now reads DATABASE_URL from environment variable
- Falls back to local PostgreSQL if not set
- Enables same code to work locally and on Vercel

### 7. **backend/auth.py** (Updated)
- Now reads SECRET_KEY from environment variable
- Falls back to dev key if not set
- Ensures security in production

## How It Works

```
User Request
    ↓
Vercel Router (vercel.json)
    ↓
    ├─ /api/* → api/index.py
    ├─ /static/* → frontend/static/
    └─ /* → api/index.py (for frontend routes)
    ↓
FastAPI App (api/index.py)
    ↓
    ├─ API Routes → Database
    └─ Frontend Routes → HTML/CSS/JS files
```

## Environment Variables on Vercel

When you deploy to Vercel, you must set these environment variables in the Vercel dashboard:

1. **DATABASE_URL** - PostgreSQL connection string
   ```
   postgresql://username:password@hostname:5432/hostel_db
   ```

2. **SECRET_KEY** - JWT secret (should be a random 64-character string)
   ```
   Generate with: openssl rand -hex 32
   ```

Without these, the app will try to use local defaults and fail.

## Database Initialization

The first time you deploy:
1. The tables are auto-created when the app first runs
2. Run `python create_test_users.py` with the production DATABASE_URL to create test users
3. Or create users through the admin registration form

## Local Development

For local development without Vercel:
1. Use the original backend setup: `cd backend && uvicorn main:app --reload`
2. Environment variables come from `.env` file or system env
3. No need to use Vercel locally

## Serverless Limitations

Vercel's Python serverless has some limitations:
- Cold starts (first request may be slow)
- Memory limit (3GB for standard)
- Timeout limit (60 seconds for standard)
- No persistent storage (use database)

For this application, these are fine because:
- Database is persistent
- Requests are typically fast
- No large file uploads

## Scaling

If you need:
- **More memory**: Upgrade Vercel Pro plan
- **Longer timeouts**: Upgrade Vercel Pro plan or optimize code
- **More requests**: Vercel scales automatically
- **Better cold starts**: Use Vercel Pro for serverless concurrency

## Monitoring

On Vercel dashboard you can:
- View real-time logs
- Monitor function executions
- Check error rates
- Track deployment history

## Rollback

To rollback to a previous version:
1. Go to Vercel project deployments
2. Click on a previous deployment
3. Click "Redeploy"

Or revert your GitHub code and push again.

## Conclusion

The setup allows the FastAPI application to run as serverless functions on Vercel while keeping all your code and frontend intact. The database remains separate but connected via connection string.
