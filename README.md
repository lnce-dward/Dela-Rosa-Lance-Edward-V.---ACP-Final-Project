# Mirai Health Tracker

## Project Overview
The **Mirai Health Tracker** is a Python-based application designed to promote better mental and physical health through data-driven insights and easy-to-use tracking tools. This application provides an interactive dashboard for users to log and monitor their health metrics, set personal goals, and reflect on mental health conditions and lifestyle choices. By leveraging technology, it aims to empower individuals to take control of their well-being and make informed decisions.

## Features
### 1. Login and Registration System
- Secure login with encrypted passwords using `bcrypt`.
- Simple registration interface.

### 2. Dashboard
- A user-friendly graphical interface using `CustomTkinter`.
- Sidebar tabs for seamless navigation between features:
  - **Mental Health**: Journaling, mood tracking, stress levels, and cognitive exercises.
  - **Physical Health**: BMI calculator, activity and diet tracker, health metrics.
  - **Profile**: Editable personal information and health summary.

### 3. Database Integration
- Powered by MySQL for robust data management.
- Tracks user profiles, health metrics, and historical data for insights.

### 4. Health Insights and History
- Daily and historical health data visualization.
- Personalized recommendations based on user inputs.

### 5. Interactive Features
- Activity tracker for fitness goals.
- Diet tracker for calorie and meal tracking.
- Stress and mood tracking to enhance mental resilience.

## SDGs Addressed
### 1. Goal 3: Good Health and Well-being
- Promotes healthier lifestyles through mental and physical health monitoring.
- Empowers individuals to manage stress, improve fitness, and achieve wellness goals.

## Technical Details
- **Programming Language**: Python
- **Libraries and Frameworks**:
  - `CustomTkinter`: For building a modern and aesthetic GUI.
  - `MySQL`: Database for managing user and health data.
  - `bcrypt`: Secure password hashing.
- **File Structure**:
  - `login.py`: Handles user authentication and redirection to the dashboard.
  - `register.py`: Manages new user registration.
  - `dashboard.py`: Provides the main interface for health tracking.

## Installation and Usage
### Prerequisites
- Python 3.7 or higher.
- MySQL database server.
- Required Python libraries: `mysql-connector-python`, `bcrypt`, and `customtkinter`.

### Setup
1. Clone the repository or download the source files.
2. Configure the MySQL database using the provided `database.sql` file.
3. Install required Python libraries using:
   ```bash
   pip install -r requirements.txt
