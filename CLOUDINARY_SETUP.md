# Cloudinary Setup Guide

## Overview
Cloudinary has been configured for secure media file storage with all credentials stored as environment variables.

## ✅ What's Been Configured

### 1. Packages Installed
- `cloudinary` - Core Cloudinary SDK
- `django-cloudinary-storage` - Django integration for Cloudinary

### 2. Settings Updated
- Added Cloudinary apps to `INSTALLED_APPS`
- Configured Cloudinary with environment variables
- Set `DEFAULT_FILE_STORAGE` to use Cloudinary for media files

### 3. Environment Variables
- Created `.env` file with Cloudinary configuration
- Updated `.env.example` as a template
- All secrets are kept out of version control

## 🔐 Security Features

✅ **Credentials Hidden**: All API keys stored in `.env` (not tracked by git)
✅ **Example Template**: `.env.example` provides template without real credentials
✅ **Git Ignored**: `.env` is in `.gitignore` to prevent accidental commits

## 📝 Next Steps

### 1. Get Your Cloudinary Credentials

1. Go to [Cloudinary Console](https://cloudinary.com/console)
2. Sign up or log in to your account
3. Go to the Dashboard
4. Copy your credentials:
   - **Cloud Name**
   - **API Key**
   - **API Secret**

### 2. Update Your .env File

Open `.env` and replace the placeholder values:

```env
CLOUDINARY_CLOUD_NAME=your-actual-cloud-name
CLOUDINARY_API_KEY=your-actual-api-key
CLOUDINARY_API_SECRET=your-actual-api-secret
```

### 3. Deploy to Heroku

Set the environment variables on Heroku:

```bash
heroku config:set CLOUDINARY_CLOUD_NAME=your-cloud-name
heroku config:set CLOUDINARY_API_KEY=your-api-key
heroku config:set CLOUDINARY_API_SECRET=your-api-secret
```

Or use the Heroku Dashboard:
1. Go to your app settings
2. Click "Reveal Config Vars"
3. Add the three Cloudinary variables

### 4. Using Cloudinary in Your Models

Add image fields to your models:

```python
from cloudinary.models import CloudinaryField

class Task(models.Model):
    # ... existing fields ...
    image = CloudinaryField('image', blank=True, null=True)
    attachment = CloudinaryField('attachment', blank=True, null=True)
```

### 5. Using in Forms

```python
# forms.py
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'image', 'priority', 'due_date']
```

### 6. Displaying Images in Templates

```html
<!-- templates/tasks/task_detail.html -->
{% if task.image %}
    <img src="{{ task.image.url }}" alt="{{ task.title }}" class="img-fluid">
{% endif %}
```

## 📚 Cloudinary Features

### Automatic Optimizations
- Image compression
- Format conversion (WebP, AVIF)
- Lazy loading support
- Responsive images

### Transformations
```python
# In templates
{% load cloudinary %}
{% cloudinary task.image width=300 height=300 crop="fill" %}
```

### Upload Options
```python
# In views
from cloudinary.uploader import upload

result = upload(request.FILES['image'],
    folder="task_images",
    transformation=[
        {'width': 800, 'height': 600, 'crop': 'limit'},
        {'quality': 'auto'}
    ]
)
```

## 🧪 Testing

Test your Cloudinary setup:

```python
# In Django shell
python manage.py shell

from cloudinary.uploader import upload
result = upload("path/to/test/image.jpg")
print(result['secure_url'])
```

## ⚠️ Important Notes

### DO NOT:
- ❌ Commit `.env` file to git
- ❌ Share API credentials publicly
- ❌ Hardcode credentials in settings.py
- ❌ Push credentials to GitHub

### DO:
- ✅ Use environment variables for all secrets
- ✅ Update `.env.example` when adding new variables
- ✅ Set Heroku config vars for production
- ✅ Keep `.env` in `.gitignore`

## 📊 Monitoring

Monitor your Cloudinary usage:
1. Go to [Cloudinary Dashboard](https://cloudinary.com/console)
2. Check usage statistics
3. Free tier: 25 GB storage, 25 GB bandwidth/month

## 🔗 Resources

- [Cloudinary Documentation](https://cloudinary.com/documentation)
- [Django Integration Guide](https://cloudinary.com/documentation/django_integration)
- [Image Transformations](https://cloudinary.com/documentation/image_transformations)
- [Upload API](https://cloudinary.com/documentation/upload_images)

---

**Last Updated**: January 13, 2026
