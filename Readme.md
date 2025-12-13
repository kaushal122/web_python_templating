# DayTemp App

A Flask web application that provides personalized daily content and side hustle ideas based on user age and the day of the week. Includes user registration, login, logout, and a simple web scraping feature.

---

## Features

- **User Registration & Login**: Secure sign-up and login with email and password.
- **Personalized Content**: Shows motivational messages on weekdays and side hustle ideas on weekends.
- **Age Restriction**: Only users 18 and older can access content.
- **User List**: View all registered users (for admin/demo).
- **Web Scraping**: Enter a URL to fetch and display the page title and main text.
- **Styled with Tailwind CSS**.

---

## Folder Structure

```
daytemp_app/
│
├── app.py
├── app.db
├── .env
├── static/
│   └── app.css
└── templates/
    ├── index.html
    ├── signup.html
    ├── day.html
    ├── sidehustle.html
    └── users.html
```

---

## Setup Instructions

### 1. **Clone the Repository**

```sh
git clone <your-repo-url>
cd daytemp_app
```

### 2. **Create a Virtual Environment (Recommended)**

```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. **Install Dependencies**

```sh
pip install -r requirements.txt
```
If you don't have a `requirements.txt`, install manually:
```sh
pip install flask flask_sqlalchemy flask_login python-dotenv requests beautifulsoup4
```

### 4. **Set Up Environment Variables**

Create a `.env` file in the project root with:

```
DATABASE_URL=sqlite:///app.db
SECRET_KEY=your_secret_key
```

### 5. **Run the App**

```sh
python app.py
```

The app will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Usage

1. **Sign Up:**  
   Go to `/signup` and create a new account.

2. **Login:**  
   Enter your email and password on the main page.

3. **Get Personalized Content:**  
   - If it's a weekday, you'll see a motivational message.
   - If it's a weekend, you'll get a side hustle idea.

4. **Web Scraping:**  
   On the content page, enter a URL to fetch its title and main text.

5. **View Users:**  
   Visit `/users` to see all registered users.

6. **Logout:**  
   Click the logout link to end your session.

---

## Notes

- Make sure your `static/app.css` exists for custom styles.
- The database (`app.db`) is created automatically on first run.
- Passwords are stored in plain text for demo purposes—**do not use in production**.

---

## Screenshots

_Add screenshots of your app here if desired._

---

## License

MIT (or your chosen license)