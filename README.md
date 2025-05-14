# Blog Web Application with Flask

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0%2B-purple)

A complete blog web application built with Flask, featuring user authentication, blog post management, and comment functionality.

## Features

- **User Authentication**:
  - Registration with password hashing
  - Login/logout functionality
  - Admin privileges for post management

- **Blog Management**:
  - Create, edit, and delete blog posts (admin only)
  - Rich text editing with CKEditor
  - Blog post categorization

- **Comment System**:
  - Authenticated users can leave comments
  - Comments displayed on post pages

- **Additional Features**:
  - Contact form with email notifications
  - About page
  - Responsive design with Bootstrap 5

## Technologies Used

- **Backend**:
  - Python 3
  - Flask web framework
  - Flask-Login for authentication
  - SQLAlchemy for database management
  - SMTP for email notifications

- **Frontend**:
  - HTML5/CSS3
  - Bootstrap 5
  - Jinja2 templating
  - CKEditor for rich text editing

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/flask-blog-app.git
   cd flask-blog-app
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file with the following variables:
   ```
   API_KEY=your_secret_key
   DB_URI=sqlite:///posts.db
   EMAIL=your_email@gmail.com
   EMAIL_PASSWORD=your_email_password
   EMAIL_TO=recipient_email@example.com
   ```

5. Initialize the database:
   ```bash
   python
   >>> from app import app, db
   >>> with app.app_context():
   ...     db.create_all()
   ```

6. Run the application:
   ```bash
   python app.py
   ```

## Usage

- Access the application at `http://localhost:5002`
- Register as a new user or log in with existing credentials
- Admin user (ID=1) has privileges to create, edit, and delete posts
- All authenticated users can leave comments on posts
- Use the contact form to send messages (requires SMTP configuration)

## Database Models

- **User**: Stores user information (name, email, password)
- **BlogPost**: Contains blog post data (title, content, author, etc.)
- **Comment**: Stores comments on blog posts with author references

## License

This project is open-source and available under the MIT License.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## Contact

For questions or feedback, please use the contact form in the application or open an issue on GitHub.