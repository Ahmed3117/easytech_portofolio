# EasyTech Portfolio API

A Django REST API for managing a portfolio website showcasing projects, features, and client testimonials.

## Features

- **Comprehensive Portfolio API**: Endpoints for About information, Projects, Features, and Clients
- **Consolidated Endpoints**: Single endpoint to fetch all portfolio data at once
- **Analytics API**: Stats and counts endpoint for portfolio elements
- **Filtering & Sorting**: Support for filtering, searching, and ordering data
- **Modern Admin Interface**: Customizable Django admin with theme support

## API Endpoints

### Main Endpoints

- `/api/portfolio-data/` - Combined endpoint for About, Projects, and Features
- `/api/stats-count/` - Statistics and counts for portfolio elements
- `/api/about/` - About information
- `/api/projects/` - Projects with filtering by type and search support
- `/api/project-types/` - List of available project types
- `/api/features/` - Features with search support
- `/api/clients/` - Clients with filtering by rating and specialization

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd easytech
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the API at http://127.0.0.1:8000/api/ and the admin interface at http://127.0.0.1:8000/admin/

## Project Structure

- `about/` - Main app containing models and API views
- `core/` - Project settings and main URL configuration
- `media/` - User-uploaded files (images)

## Technologies

- Django 5.1
- Django REST Framework
- Django Admin Interface (customizable admin)
- SQLite (development) / PostgreSQL (production)

## Testing

A Postman collection is included for testing the API endpoints.
Import `easytech_portfolio_api.postman_collection.json` into Postman to get started.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 