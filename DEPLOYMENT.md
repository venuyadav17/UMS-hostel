# Deploying to Vercel

This guide explains how to deploy the HostelHub application to Vercel.

## Prerequisites

1. **Vercel Account** - Sign up at https://vercel.com
2. **GitHub Account** - Repository must be on GitHub for Vercel deployment
3. **PostgreSQL Database** - You need a hosted PostgreSQL database (Vercel, PlanetScale, Railway, etc.)
4. **Git** - For version control

## Step 1: Prepare Your Database

You need a hosted PostgreSQL database. Popular options:
- **Vercel Postgres** (Recommended) - Free tier available
- **Railway.app** - Free credits included
- **PlanetScale** - MySQL alternative
- **Heroku Postgres** (Paid)
- **Amazon RDS** - AWS service

### Get your DATABASE_URL connection string

Once your database is created, you'll have a connection string like:
```
postgresql://username:password@hostname:5432/dbname
```

## Step 2: Prepare Your Git Repository

1. Initialize git (if not already done):
```bash
git init
git add .
git commit -m "Initial commit for Vercel deployment"
```

2. Push to GitHub:
```bash
git remote add origin https://github.com/your-username/UMS-hostel
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Vercel

1. Go to https://vercel.com and sign in with your GitHub account
2. Click "Add New..." → "Project"
3. Select your `UMS-hostel` repository
4. Click "Import"
5. In the "Configure Project" section:
   - **Framework**: FastAPI
   - Keep other settings as default

## Step 4: Add Environment Variables

Before deploying, add your environment variables:

1. In the Vercel project settings, go to **Settings** → **Environment Variables**
2. Add these variables:

```
DATABASE_URL = postgresql://username:password@hostname:5432/hostel_db
SECRET_KEY = (generate with: openssl rand -hex 32)
```

To generate a SECRET_KEY:
```bash
openssl rand -hex 32
```

3. Click "Save"

## Step 5: Deploy

1. Click "Deploy" button
2. Wait for the build to complete
3. Once deployment is successful, you'll get a URL like: `https://your-project.vercel.app`

## Step 6: Initialize Database

After deployment, you need to initialize the database tables and create test users.

1. SSH into your Vercel serverless environment or run initialization locally:

```bash
python backend/apply_migration.py
python create_test_users.py
```

**OR** You can visit your deployed app and the tables will auto-create on first API call.

## Testing the Deployment

1. Visit your Vercel URL: `https://your-project.vercel.app`
2. Try logging in with test credentials:
   - **Admin**: admin / admin123
   - **Student**: testuser / password123

## Common Issues & Solutions

### Issue: Database connection error
- **Solution**: Verify DATABASE_URL is correct in Vercel environment variables
- Check that your PostgreSQL database is accessible from the internet
- Whitelist Vercel's IP addresses (usually * for Vercel-hosted databases)

### Issue: Static files not loading
- **Solution**: Make sure `frontend/` directory is included in git
- Check that `vercel.json` is properly configured

### Issue: CORS errors
- **Solution**: CORS is already enabled for all origins in the backend, but you might need to check browser console for specific errors

### Issue: 502 Bad Gateway
- **Solution**: Check Vercel logs for backend errors
- Make sure all dependencies in `requirements.txt` are installed
- Verify database connection

## Updating the Application

To make changes and redeploy:

```bash
# Make your changes
git add .
git commit -m "Your changes"
git push origin main
```

Vercel will automatically redeploy on every push to the main branch.

## Environment-Specific Configuration

For local development:
```bash
cp .env.example .env
# Edit .env with your local PostgreSQL credentials
```

For Vercel:
- Set environment variables in Vercel dashboard (Settings → Environment Variables)
- They will be automatically injected during deployment

## Database Migrations

To run database migrations or scripts on Vercel:

Option 1: Use Vercel's Python runtime
- Create scripts in `api/` directory to run as serverless functions

Option 2: Run locally, then push
- Run migrations locally with correct DATABASE_URL
- Push changes to GitHub and deploy

## Additional Resources

- [Vercel FastAPI Docs](https://vercel.com/docs/frameworks/fastapi)
- [Vercel Python Support](https://vercel.com/docs/runtimes/python)
- [PostgreSQL Connection Strings](https://www.postgresql.org/docs/current/libpq-connect-string.html)

## Support

For issues with:
- **Vercel Deployment**: Check [Vercel Docs](https://vercel.com/docs)
- **FastAPI**: Check [FastAPI Docs](https://fastapi.tiangolo.com)
- **PostgreSQL**: Check your database provider's documentation
