# DevPulse — Modern Django Blog Application

DevPulse is a full-featured, responsive blog web application built with **Django 5.1**, **Bootstrap 5**, **Django REST Framework**, and **CKEditor 5**.

---

## Key Features

- **User Authentication & Profiles**: Built-in authentication (signup, login, logout, password reset) with customizable user profiles (bio, avatar, location, website).
- **Blog Posts (CRUD)**: Create, view, edit, and delete articles with rich HTML content, status controls (`draft` vs `published`), cover images, view counts, and likes.
- **Author & Admin Permissions**: Only article authors or administrators can edit or delete their respective posts.
- **Categories & Many-to-Many Tags**: Organize articles by category and filter by multiple tags.
- **Nested Comments**: Logged-in users can participate in discussions with nested comment replies. Comment deletion is supported for comment authors, post authors, and admins.
- **WYSIWYG Rich Text Editor**: Integrated CKEditor 5 for editing post content in both the dashboard and Django admin.
- **Live Search & Pagination**: Search posts by title, body, category, or tag with page-by-page listing.
- **Post Liking System**: Interactive AJAX like/unlike toggle with real-time counter updates.
- **Custom Admin Panel**: Richly customized Django admin interface with list displays, filters, search fields, inline comments, and bulk publishing actions.
- **REST API**: Built-in RESTful API endpoints (`/api/posts/`, `/api/categories/`, `/api/tags/`) via Django REST Framework.
- **RSS Feed**: Syndicated RSS feed at `/feed/` for subscribing to published posts.
- **Flexible Database Switching**: Uses SQLite for rapid local development and `dj-database-url` for 1-step deployment to PostgreSQL.

---

## Project Structure

```
blog application_CAi/
├── blog/                      # Main blog application app
│   ├── management/commands/   # Custom management commands (seed_data.py)
│   ├── admin.py               # Customized Django admin interfaces
│   ├── api.py                 # DRF serializers & viewsets
│   ├── api_urls.py            # REST API endpoints
│   ├── context_processors.py  # Global categories and tags processor
│   ├── feeds.py               # RSS feed generator
│   ├── forms.py               # Authentication, profile, post, comment forms
│   ├── models.py              # Profile, Category, Tag, Post, Comment models
│   ├── signals.py             # Automatic Profile creation on User signup
│   ├── urls.py                # Blog URL routes
│   └── views.py               # Class-based & function views
├── blog_project/              # Project configuration package
│   ├── settings.py            # Project settings (SQLite/PostgreSQL config)
│   └── urls.py                # Root URL router
├── static/                    # Custom CSS & static assets
│   └── css/style.css
├── templates/                 # HTML Templates with Bootstrap 5
│   ├── base.html              # Base layout (navbar, search, footer)
│   ├── blog/                  # Post list, post detail, post form, dashboard
│   └── registration/          # Login, signup, profile, password reset
├── media/                     # Uploaded media (avatars, featured images)
├── requirements.txt           # Python dependencies
├── manage.py                  # Django CLI runner
└── README.md                  # Project documentation
```

---

## Quick Start & Setup Instructions

### 1. Prerequisites
- Python 3.11+ installed

### 2. Set Up Virtual Environment & Dependencies
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Seed Initial Data
Run the custom seed data command to populate initial categories, tags, demo authors, superuser, articles, and comments:
```bash
python manage.py seed_data
```

> **Default Demo Credentials:**
> - **Admin Superuser**: Username: `admin` | Password: `admin123`
> - **Demo Author**: Username: `alex_dev` | Password: `password123`

### 5. Run Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## Key URLs

| Page / Feature | URL Path |
| --- | --- |
| Homepage / Blog List | `http://127.0.0.1:8000/` |
| Creator Dashboard | `http://127.0.0.1:8000/dashboard/` |
| Create Article | `http://127.0.0.1:8000/post/new/` |
| Django Admin Panel | `http://127.0.0.1:8000/admin/` |
| REST API Root | `http://127.0.0.1:8000/api/posts/` |
| RSS Feed | `http://127.0.0.1:8000/feed/` |
| Login / Register | `http://127.0.0.1:8000/login/` \| `http://127.0.0.1:8000/signup/` |

---

## Switching to PostgreSQL

To connect to a PostgreSQL database for production:
Set the `DATABASE_URL` environment variable:
```bash
export DATABASE_URL="postgres://db_user:db_password@localhost:5432/blog_db"
```
Or create a `.env` file in the root directory:
```env
DATABASE_URL=postgres://db_user:db_password@localhost:5432/blog_db
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,localhost
```
Then execute migrations: `python manage.py migrate`.
