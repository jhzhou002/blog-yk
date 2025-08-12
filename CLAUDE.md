# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django-based responsive blog website project (blog-yk) designed to support both PC and mobile access. The project is currently in the planning/specification phase with detailed requirements documented in Chinese.

## Technology Stack

- **Backend**: Django 4.x (MVC pattern)
- **Frontend**: Bootstrap 5 + custom CSS/JS
- **Database**: MySQL 8.x
- **Object Storage**: Qiniu Cloud (七牛云) for media files
- **Deployment**: Baota Panel (宝塔面板) with Nginx + Gunicorn + Supervisor
- **Optional**: Redis for caching and session storage

## Architecture

The project follows Django's MVC pattern with a single app structure:
- **blog_app**: Contains all functionality including articles, categories, tags, search, comments, user management, and admin backend

## Database Configuration

Based on the specification document:
- Host: 101.35.218.174
- Username: tongyong
- Database: blog_test
- Note: Password is specified in the Chinese documentation

## Qiniu Cloud Storage Configuration

- Access Key: nfxmZVGEHjkd8Rsn44S-JSynTBUUguTScil9dDvC
- Bucket: youxuan-images
- Storage folder: blog-yk/
  - Article images: blog-yk/images/
  - User avatars: blog-yk/avatar/
- Region: East China - Zhejiang

## Key Features to Implement

### User-facing Features
- Article display with pagination
- Article detail pages with view counting
- Category and tag-based browsing
- Full-text search functionality
- Comment system with moderation
- User registration and authentication
- Responsive design (mobile-first)

### Admin Features
- Article management (CRUD, draft/publish)
- Category and tag management
- Comment moderation
- User management
- System settings for Qiniu Cloud integration

## Development Notes

- The project has been refactored to use a single Django app (`blog_app`)
- All models are consolidated in `blog_app/models.py` 
- Database migrations need to be created and run by the developer
- Media files should be uploaded to Qiniu Cloud with proper renaming conventions
- Security measures include CSRF protection, XSS prevention, and HTTPS support
- Performance optimizations include Redis caching and database indexing

## Important Files

- `blog_app/models.py`: All database models (User Profile, Post, Category, Tag, Comment, SiteSettings)
- `blog_app/views.py`: All view functions (blog, auth, dashboard)
- `blog_app/urls.py`: All URL configurations
- `blog_app/admin.py`: Django admin configuration
- `blog_app/forms.py`: All forms (authentication, blog management)
- `个人博客.md`: Comprehensive project specification in Chinese
- `README.md`: Project documentation

## Development Commands

After setting up the environment:
```bash
python manage.py makemigrations blog_app
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```