# Budget-App

#### Video Demo:  https://youtu.be/your-video-link-here
#### Description:

## Project Overview
Budget App is a web application built with Flask and SQLite that helps users manage their personal finances. The application allows users to track their income, expenses, and savings in an intuitive and visually appealing interface. With features like transaction categorization, filtering by date, and real-time savings calculation, users can easily monitor their financial health.

## Features

### 1. **User Authentication**
- Secure user registration and login system
- Password hashing for enhanced security
- Session management for maintaining user state

### 2. **Transaction Management**
- Add new transactions with detailed information:
  - Category (Rent, Food, Transport, Light, Water, WiFi, Health Insurance, Fun, Other)
  - Amount
  - Date (Year, Month, Day)
  - Optional notes
- Delete unwanted transactions
- View all transactions in a clean, organized table

### 3. **Salary Management**
- Set and update monthly salary
- Real-time calculation of savings (Salary - Total Expenses)

### 4. **Dashboard with Filtering**
- Filter transactions by:
  - Year, Month, Day
  - Category

### 5. **Financial Summary**
- Display total expenses
- Show current savings
- Present salary information

## Technical Implementation

### Backend (Flask)
- **Framework**: Flask web framework
- **Database**: SQLite with CS50 SQL wrapper
- **Session Management**: Flask-Session for secure user sessions

### Database Schema
- **users**: Stores user information (id, username, password hash, salary)
- **transactions**: Stores all financial transactions (id, user_id, category, amount, date fields, note)

### Frontend
- **HTML/Jinja2**: Dynamic templating
- **CSS**: Custom styling with CSS variables for consistent theming
- **Responsive Design**: Works on various screen sizes

## Design Choices

### Color Scheme
The application uses a pastel color scheme with purple and blue tones:
- **Purple Theme**: Used for expense tracking tables
- **Blue Theme**: Used for salary information tables
- **Color Coding**: Red for negative savings, green for positive savings

### User Experience
- **Intuitive Navigation**: Clear menu structure with Dashboard, Transactions, and Logout options
- **Visual Feedback**: Color-coded savings and hover effects
- **Form Validation**: Client and server-side validation for data integrity

## File Structure
project/
├── app.py # Main Flask application
├── database.db # SQLite database
├── helpers.py # Custom helper functions
├── requirements.txt # Python dependencies
├── static/
│ └── styles.css # CSS stylesheet
└── templates/
├── layout.html # Base template
├── index.html # Home page
├── login.html # Login page
├── register.html # Registration page
├── dashboard.html # Dashboard with filtering
└── transactions.html # Transaction management

text

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `flask run`
3. Open browser and navigate to: `http://localhost:5000`

## Learning Outcomes
This project demonstrates:
- Full-stack web development with Flask
- Database design and management
- User authentication and session management
- Frontend-backend integration
- Responsive web design principles
- Financial calculation logic implementation

## Future Enhancements
Potential improvements include:
- Monthly budget setting and tracking
- Expense charts and visualizations
- Export functionality (CSV/PDF)
- Recurring transactions
- Mobile application version
- Multi-currency support
