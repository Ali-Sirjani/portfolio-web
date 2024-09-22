
# Ali Sirjani's Portfolio Website

This is the official repository for my personal portfolio website built with Django. The portfolio showcases my work, skills, and blog posts related to web development and programming.

## Features

- **Home Page**: Introduces myself as a Backend Developer specializing in web technologies.
- **Blog Section**: Share insights, tutorials, and experiences on various topics like web development, business, and more.
- **Projects Section**: Displays my key projects, including detailed descriptions and links to live demos or GitHub repositories.
- **User Profile**: Users can create an account, log in, and customize their profile. Features include authentication via Google, thanks to `django-allauth`.
- **Dark Mode**: Users can toggle between light and dark mode for better readability.

## Tech Stack

- **Frontend**: Bootstrap5, crispy-forms for responsive and aesthetic designs.
- **Backend**: Django 5, PostgreSQL as the main database.
- **Authentication**: Google OAuth integration for user login using `django-allauth`.
- **SEO & Metadata**: `django-meta` is integrated to improve SEO performance by easily handling meta tags for social sharing and search engines.
- **Third-party integrations**:
  - `ckeditor`: For rich text editing.
  - `django-filters`: For filtering and sorting through projects and blog posts.
  - `jalali_date`: For displaying date formats in Persian (Farsi).
  - `debug_toolbar`: For enhanced debugging during development.

## Screenshots

![1](https://github.com/user-attachments/assets/fa7cf776-0f70-42c7-b826-aa4fe23781c1)

![blog posts](https://github.com/user-attachments/assets/bb39444a-f938-48f8-97f5-bb25c22bf862)

![site1](https://github.com/user-attachments/assets/c0599bde-25ed-4a22-8eea-12a490f8fde0)

## Installation

To set up and run the Website Online Shop project, follow these steps:

1. **Create a .env File:**
   Create a `.env` file in the project's root directory and configure the following environment variables:

   ```plaintext
   DOCKER_COMPOSE_DJANGO_SECRET_KEY=your-secret-key
   DOCKER_COMPOSE_DJANGO_DEBUG=debug-value
   ```

2. **Run Docker Compose:**
   Start the Docker containers using Docker Compose:

   ```bash
   docker-compose up
   ```

3. **Apply Migrations:**

   ```bash
   docker-compose exec web python manage.py makemigrations
   docker-compose exec web python manage.py migrate
   ```

4. **Run the Server:**
   The project should now be accessible at `http://localhost:8000/`. You can explore the website and begin your online shopping experience.
