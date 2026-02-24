# Quick Deployment Checklist for Vercel

## Before You Deploy

- [ ] Push code to GitHub repository
- [ ] Have PostgreSQL database credentials ready (hostname, username, password, database name)
- [ ] Generate a SECRET_KEY: `openssl rand -hex 32`

## Deployment Steps

1. **Sign in to Vercel**
   - Go to https://vercel.com
   - Sign in with your GitHub account

2. **Import Your Project**
   - Click "Add New..." → "Project"
   - Select your GitHub repository `UMS-hostel`
   - Click "Import"

3. **Configure Environment Variables**
   - Click "Environment Variables"
   - Add:
     - Name: `DATABASE_URL`
     - Value: `postgresql://username:password@hostname:5432/hostel_db`
   - Add:
     - Name: `SECRET_KEY`
     - Value: (your generated secret key from above)
   - Click "Add" for each variable

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete (usually 2-5 minutes)
   - Get your live URL (e.g., https://ums-hostel.vercel.app)

5. **Initialize Database** (One-time setup)
   - Run locally with your production DATABASE_URL:
   ```bash
   export DATABASE_URL="your-production-database-url"
   python create_test_users.py
   ```
   OR the tables will auto-create on first API call

6. **Test Your Deployment**
   - Visit your Vercel URL
   - Try logging in:
     - Admin: admin / admin123
     - Student: testuser / password123

## Database Providers (Recommended)

- **Railway.app** - Easy setup, free credits
- **Vercel Postgres** - Integrated with Vercel
- **PlanetScale** - Free MySQL alternative
- **Supabase** - Free PostgreSQL alternative

## Troubleshooting

If you get errors during deployment:

1. Check Vercel build logs for exact error messages
2. Verify DATABASE_URL format is correct
3. Ensure PostgreSQL database is accessible from the internet
4. Check that all files are committed to GitHub

## Future Deployments

Every time you push to GitHub main branch, Vercel will automatically redeploy!

```bash
git add .
git commit -m "Your changes"
git push origin main
```

That's it! Your app will be live within minutes.
