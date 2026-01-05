# Heroku Deployment Guide for PlanIt!

## Prerequisites
- Heroku account (free tier available at https://www.heroku.com)
- Heroku CLI installed (https://devcenter.heroku.com/articles/heroku-cli)
- Git repository set up

## Step-by-Step Deployment

### 1. Install Heroku CLI
```bash
# On Windows, download from https://devcenter.heroku.com/articles/heroku-cli
# Or use chocolatey:
choco install heroku-cli
```

### 2. Login to Heroku
```bash
heroku login
```

### 3. Create a Heroku App
```bash
heroku create planit-yourname
# Or use an existing app:
heroku apps:create
```

### 4. Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

The `DATABASE_URL` will be automatically set as an environment variable.

### 5. Set Environment Variables
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(50))')
heroku config:set ALLOWED_HOSTS=planit-yourname.herokuapp.com
heroku config:set SECURE_SSL_REDIRECT=True
heroku config:set SESSION_COOKIE_SECURE=True
heroku config:set CSRF_COOKIE_SECURE=True

# Email settings (optional)
heroku config:set EMAIL_HOST_USER=your-email@gmail.com
heroku config:set EMAIL_HOST_PASSWORD=your-app-password
```

### 6. Run Database Migrations
```bash
heroku run python manage.py migrate
```

### 7. Create Superuser (Admin)
```bash
heroku run python manage.py createsuperuser
```

### 8. Collect Static Files (if needed)
```bash
heroku run python manage.py collectstatic --noinput
```

### 9. Deploy to Heroku
```bash
git push heroku main
# Or if your branch is 'master':
git push heroku master
```

### 10. View Logs
```bash
heroku logs --tail
```

### 11. Open Your App
```bash
heroku open
```

---

## Files Already Configured for Heroku

✅ **Procfile** - Tells Heroku how to run the app
✅ **runtime.txt** - Specifies Python version
✅ **requirements.txt** - All production dependencies
✅ **settings.py** - Environment variable configuration
✅ **.env.example** - Template for environment variables

---

## Important Notes

### Environment Variables
- **SECRET_KEY**: Change from default! Use a strong, random key
- **DEBUG**: Must be `False` in production
- **DATABASE_URL**: Automatically set by Heroku PostgreSQL addon
- **Email Settings**: Configure Gmail or SendGrid for notifications

### Database
- Default is SQLite (fine for testing)
- For production, use PostgreSQL (recommended)
- Heroku addon: `heroku-postgresql:hobby-dev` (free tier)

### Static Files
- WhiteNoise is configured to serve static files
- Run `collectstatic` if you add new static files
- CSS/JS are automatically compressed and minified

### Security
- `SECURE_SSL_REDIRECT`: Forces HTTPS
- `SESSION_COOKIE_SECURE`: Secure session cookies
- `CSRF_COOKIE_SECURE`: Secure CSRF tokens

---

## Troubleshooting

### "Error: remote rejected"
```bash
git add .
git commit -m "deployment updates"
git push origin main  # Push to GitHub first
git push heroku main   # Then push to Heroku
```

### "No such table" error
```bash
heroku run python manage.py migrate
```

### Static files not loading
```bash
heroku run python manage.py collectstatic --noinput
heroku restart
```

### View detailed logs
```bash
heroku logs --tail  # Real-time logs
heroku logs         # Last 100 lines
```

---

## Post-Deployment

1. **Verify Admin Panel**: https://your-app-name.herokuapp.com/admin/
2. **Test CRUD Operations**: Create, read, update, delete tasks
3. **Monitor Logs**: `heroku logs --tail`
4. **Scale Dynos** (if needed): `heroku ps:scale web=2`

---

## Connect to Heroku Database (Optional)

```bash
# Open PostgreSQL shell
heroku pg:psql

# Common commands:
\dt                 # List tables
SELECT * FROM tasks_task;  # Query tasks
\q                  # Exit
```

---

## Continuous Deployment (Optional)

Connect your GitHub repo to Heroku for automatic deployments:

1. Go to your Heroku app dashboard
2. Click "Deploy" tab
3. Connect to GitHub
4. Enable automatic deploys from main branch

---

## Additional Resources

- [Heroku Django Documentation](https://devcenter.heroku.com/articles/django-app-configuration)
- [Heroku PostgreSQL Documentation](https://devcenter.heroku.com/articles/heroku-postgresql)
- [Procfile Reference](https://devcenter.heroku.com/articles/procfile)
- [Config Variables](https://devcenter.heroku.com/articles/config-vars)
