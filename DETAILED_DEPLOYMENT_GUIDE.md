# Complete Step-by-Step Deployment Guide for Vercel

## Overview
This guide will walk you through deploying the HostelHub application from your GitHub repository to Vercel with a production PostgreSQL database.

**Total Time:** 30-45 minutes
**Cost:** Free (with paid database option)

---

## STEP 1: Create a PostgreSQL Database

You have several options. We recommend **Railway.app** for ease of use.

### Option A: Railway.app (RECOMMENDED - Easiest)

1. Go to https://railway.app
2. Click "Start a New Project"
3. Click "Provision PostgreSQL"
4. A PostgreSQL database will be created automatically
5. Click on "PostgreSQL" in the project
6. Go to "Connect" tab
7. Copy the full connection string (it looks like: `postgresql://user:password@host:port/dbname`)
8. Save this string - you'll use it in Step 3

### Option B: Vercel Postgres (Integrated with Vercel)

1. Go to https://vercel.com
2. Create a project first (we'll do that in Step 2)
3. In project settings → "Storage"
4. Click "Create Database" → Select "Postgres"
5. Name it "hostel_db"
6. Copy the connection string provided
7. Use this string in Step 3

### Option C: Supabase (Easiest PostgreSQL Alternative)

1. Go to https://supabase.com
2. Click "Start your project"
3. Sign in with GitHub
4. Create a new organization and project
5. Go to "Settings" → "Database"
6. Copy the connection string (URI format)
7. Use this string in Step 3

### Option D: PlanetScale (MySQL, not PostgreSQL - use if above don't work)

1. Go to https://planetscale.com
2. Create account and new database
3. Go to "Passwords" section
4. Create a new password
5. Choose "MySQLJS" format
6. Copy the connection string
7. Note: You may need to modify database.py slightly for MySQL

**→ For this guide, we'll use Railway.app as it's the easiest**

---

## STEP 2: Set Up Vercel and Import Project

### 2.1 Create Vercel Account

1. Go to https://vercel.com
2. Click "Sign Up"
3. Click "Continue with GitHub"
4. Authorize Vercel to access your GitHub account
5. You'll be logged into Vercel

### 2.2 Import Your GitHub Repository

1. On Vercel dashboard, click "Add New" → "Project"
2. Under "Import Git Repository", search for "UMS-hostel"
3. Click on your repository: `venuyadav17/UMS-hostel`
4. Click "Import"

You'll see the "Configure Project" screen:
- **Project Name:** UMS-hostel (or any name you like)
- **Framework Preset:** Other (FastAPI is not in dropdown, but it works)
- **Root Directory:** ./ (leave as default)

5. **DON'T click "Deploy" yet!** We need to add environment variables first.

---

## STEP 3: Add Environment Variables

### 3.1 Generate Secret Key

Open your terminal/command prompt and run:

```bash
openssl rand -hex 32
```

This will output something like:
```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

**Copy this value** - you'll use it next.

### 3.2 Add Variables in Vercel

1. You should still be on the "Configure Project" page
2. Scroll down to "Environment Variables"
3. Click to expand the environment variables section

**Add First Variable:**
- Name: `DATABASE_URL`
- Value: (paste the PostgreSQL connection string from Step 1)
  - Example: `postgresql://postgres:abc123@db.railway.internal:5432/railway`
- Click "Add"

**Add Second Variable:**
- Name: `SECRET_KEY`
- Value: (paste the result from `openssl rand -hex 32`)
  - Example: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`
- Click "Add"

Now you have both environment variables set.

---

## STEP 4: Deploy to Vercel

1. Click the "Deploy" button
2. Vercel will build and deploy your application
3. This usually takes 2-5 minutes
4. You'll see a progress bar with "Building..." and then "✓ Production"
5. Once complete, you'll get a deployment URL like:
   ```
   https://ums-hostel.vercel.app
   ```

**Your app is now live!** 🎉

But we need to initialize the database first before it works.

---

## STEP 5: Initialize the Database

When you visit the deployed app for the first time, the tables should auto-create. But you need to create test users.

### Option A: Run Locally with Production Database (RECOMMENDED)

1. On your local machine, open a terminal in the project folder:
   ```bash
   cd c:\Users\atike\OneDrive\Desktop\PEP\UMS-hostel
   ```

2. Set the DATABASE_URL to your production database:
   
   **On Windows PowerShell:**
   ```powershell
   $env:DATABASE_URL = "postgresql://user:password@host:port/dbname"
   ```
   
   **Replace with your actual connection string from Step 1**

3. Run the test user creation script:
   ```bash
   python create_test_users.py
   ```

4. You should see:
   ```
   Database connection successful!
   ✅ Test user 'testuser' created successfully!
   ✅ Admin user 'admin' created successfully!
   ```

### Option B: Use Vercel Shell (Advanced)

If you have Vercel CLI installed, you can sync your environment and run scripts, but Option A is simpler.

---

## STEP 6: Test Your Deployed App

1. Open your browser and go to your Vercel URL:
   ```
   https://ums-hostel.vercel.app
   ```

2. You should see the Login page

3. Try logging in with **Admin Account:**
   - Username: `admin`
   - Password: `admin123`
   - You should see the Admin Dashboard

4. Try the other **Student Account:**
   - Username: `testuser`
   - Password: `password123`
   - You should see the Student Portal

5. Test creating a hostel:
   - Click "Add New Hostel"
   - Enter name: "Test Hostel"
   - Enter description: "Test description"
   - Click "Publish Hostel"
   - You should see success message

6. Test adding rooms:
   - Select your hostel from dropdown
   - Enter number of rooms: 2
   - Enter room numbers: 101, 102
   - Set type: AC
   - Set seater: 3 Seater
   - Set price: 10000
   - Click "Add Rooms"
   - Should show "Successfully added 2 rooms!"

7. Test student booking:
   - Logout
   - Login as `testuser`
   - You should see available rooms
   - Click "Book Now" on a room
   - Complete the booking
   - Should show your booked room details

**If all tests pass, your app is successfully deployed!** ✅

---

## STEP 7: Configure Custom Domain (Optional)

If you want your own domain instead of vercel.app:

1. Go to your Vercel project settings
2. Click "Domains"
3. Enter your domain name
4. Follow the DNS configuration steps
5. Your app will be available at your custom domain

---

## STEP 8: Update Your Local Environment (Optional)

Update your `.env` file locally to use production database for testing:

1. Open `.env` in your project
2. Add:
   ```
   DATABASE_URL=postgresql://user:password@host:port/dbname
   SECRET_KEY=your-secret-key-from-openssl
   ```

3. Now when you run locally, it will use production database (useful for testing)

---

## Troubleshooting

### Issue: Build Failed on Vercel

**Check the build logs:**
1. Go to your Vercel project
2. Click "Deployments"
3. Click on the failed deployment
4. Scroll down to see the error logs
5. Common issues:
   - Missing dependencies in requirements.txt
   - Invalid DATABASE_URL format
   - Python version compatibility

**Solution:** Fix the issue locally, commit, and push to GitHub. Vercel will auto-redeploy.

### Issue: "Connection refused" or Can't Connect to Database

**Causes:**
- DATABASE_URL is wrong
- Database server is down
- IP is not whitelisted

**Solution:**
1. Verify DATABASE_URL format is correct
2. Check database provider's status
3. In Railway/Vercel Postgres, ensure public access is enabled
4. Whitelist all IPs (usually done automatically)

### Issue: "Can't find module 'database'" or Import Errors

**Cause:** Python path issues

**Solution:**
- This is usually fixed by the api/index.py we created
- If still having issues, check that all files are in git:
  ```bash
  git status
  ```
- Commit and push any missing files

### Issue: Static Files Not Loading (CSS/JS not working)

**Cause:** Frontend files not uploaded

**Solution:**
1. Ensure `frontend/` folder is committed to git:
   ```bash
   git add frontend/
   git commit -m "Add frontend files"
   git push
   ```
2. Redeploy on Vercel

### Issue: Database Tables Not Created

**Solution:**
1. The tables should auto-create when the app runs
2. If not, run locally with production DATABASE_URL:
   ```bash
   python backend/apply_migration.py
   ```
3. Or manually run in your database client:
   ```sql
   CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       username VARCHAR UNIQUE NOT NULL,
       email VARCHAR UNIQUE NOT NULL,
       hashed_password VARCHAR NOT NULL,
       role VARCHAR DEFAULT 'student',
       is_active BOOLEAN DEFAULT TRUE
   );
   ```

---

## Making Updates After Deployment

### To make code changes:

1. Make your changes locally
2. Test them:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
3. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```
4. Vercel will automatically redeploy! ✨

### Environment Variables Changes:

1. Go to Vercel project settings
2. Click "Environment Variables"
3. Edit the variable
4. Vercel will prompt to redeploy
5. Click to redeploy

---

## Production Best Practices

### 1. Using Different Databases for Dev and Prod

You can set environment variables to use different databases:

**.env.local (local development)**
```
DATABASE_URL=postgresql://localhost/hostel_dev
SECRET_KEY=dev-key-not-secure
```

**Vercel Environment Variables (production)**
```
DATABASE_URL=postgresql://user:pass@prod-host/hostel_prod
SECRET_KEY=secure-production-key
```

### 2. Database Backups

- Railway.app: Automatic daily backups
- Vercel Postgres: Automatic backups included
- Supabase: Automatic backups included

Backup your database regularly or check your provider's backup settings.

### 3. Monitoring

1. Go to Vercel dashboard
2. Click your project
3. View real-time logs and analytics
4. Set up alerts for deployments

### 4. Scaling

As your app grows:
- Vercel Pro: More concurrency, longer timeouts
- Database upgrades: More connections, more storage

---

## Summary

You now have:
- ✅ Code on GitHub (https://github.com/venuyadav17/UMS-hostel)
- ✅ App deployed on Vercel (https://ums-hostel.vercel.app)
- ✅ Production PostgreSQL database
- ✅ Test users created
- ✅ Everything working end-to-end

**Your application is live and ready to use!** 🚀

For any issues, check the Troubleshooting section above or contact your database provider's support.
