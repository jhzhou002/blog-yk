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

The project follows Django's MVC pattern with these planned modules:
- **blog**: Articles, categories, tags, search, comments
- **accounts**: User registration, login, profile management  
- **common**: Utilities and configuration
- **dashboard**: Admin backend

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

- The project currently contains only documentation files
- No Django code has been implemented yet
- Database schema is detailed in the Chinese specification document
- Media files should be uploaded to Qiniu Cloud with proper renaming conventions
- Security measures should include CSRF protection, XSS prevention, and HTTPS
- Performance optimizations should include Redis caching and database indexing

## Important Files

- `个人博客.md`: Comprehensive project specification in Chinese with detailed requirements, database schema, and technical architecture
- `README.md`: Basic project identification

## Next Steps for Development

1. Initialize Django project structure
2. Set up database models based on the specified schema
3. Configure Qiniu Cloud integration
4. Implement Bootstrap-based responsive templates
5. Develop core functionality modules
6. Set up deployment configuration for Baota Panel