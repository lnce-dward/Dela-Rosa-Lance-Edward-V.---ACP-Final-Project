# Mirai Health Tracker

## Project Overview
The **Mirai Health Tracker** is a Python-based application designed to promote better mental and physical health through data-driven insights and easy-to-use tracking tools. This application aligns with UN Sustainable Development Goal 3 (Good Health and Well-being) by providing an interactive dashboard for users to log and monitor their health metrics, set personal goals, and reflect on mental health conditions and lifestyle choices.

## Features

### 1. Login and Registration System
- Secure user authentication with encrypted passwords using `bcrypt`
- User-friendly registration interface with field validation
- Email verification system for account security
- Password strength requirements enforced

### 2. Interactive Dashboard
- Modern graphical interface built with `CustomTkinter`
- Intuitive navigation with sidebar tabs:
  - **Mental Health Tab**: Track mood, stress levels, and journal entries
  - **Physical Health Tab**: Monitor BMI, activities, and health metrics
  - **Profile Tab**: Manage personal information and health summary
- Real-time data visualization with interactive charts
- Daily, weekly, and monthly progress views

### 3. Mental Health Tracking
- Mood tracking on a 1-10 scale with emoji indicators
- Stress level monitoring with customizable factors
- Journal entries with rich text formatting
- Symptom logging and pattern recognition
- Cognitive exercises and mindfulness activities
- Historical data visualization and trend analysis

### 4. Physical Health Monitoring
- BMI calculator with health status indicators
- Activity tracker for various exercise types
- Calorie tracking and burn rate calculations
- Vital signs monitoring (blood pressure, heart rate)
- Progress charts and achievement tracking
- Custom workout plan integration

### 5. Data Management
- Secure MySQL database integration
- Automated data backup and recovery
- Export functionality for health reports
- Data privacy controls and encryption
- Cross-device synchronization capability

## Technical Details

### System Requirements
- Python 3.7 or higher
- MySQL Server 5.7 or higher
- Minimum 4GB RAM
- 500MB free disk space

### Dependencies
```
customtkinter>=5.2.0
mysql-connector-python>=8.0.0
bcrypt>=4.0.1
matplotlib>=3.7.0
```

### Database Configuration
1. Install MySQL Server
2. Create a new database:
   ```sql
   CREATE DATABASE MIRAI_DB;
   ```
3. Import the schema:
   ```bash
   mysql -u root -p MIRAI_DB < mirai_db.sql
   ```

### Installation Guide
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mirai-health-tracker.git
   cd mirai-health-tracker
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure database connection in `config.py`:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'your_username', --change base on what username you set
       'password': 'your_password', --as well as the password
       'database': 'MIRAI_DB'
   }
   ```

4. Run the application:
   ```bash
   python login.py
   ```

## GUI Usage Guide

### Login/Registration
1. Launch the application
2. For new users:
   - Click "Register"
   - Fill in required fields (username, email, password, etc.)
   - Verify email if required
   - Complete profile information
3. For existing users:
   - Enter username/email and password
   - Click "Login"

### Dashboard Navigation
1. **Mental Health Tracking**:
   - Select "Mental Health" tab
   - Use sliders to rate mood (1-10)
   - Input stress levels
   - Add journal entries
   - View historical data in graphs

2. **Physical Health Monitoring**:
   - Navigate to "Physical Health" tab
   - Enter height/weight for BMI
   - Log daily activities
   - Track vital signs
   - Monitor progress charts

3. **Profile Management**:
   - Access "Profile" tab
   - Update personal information
   - View health summary
   - Manage privacy settings
   - Export health reports

### Data Visualization
- Interactive charts show trends over time
- Color-coded indicators for health status
- Customizable date ranges for analysis
- Export options for data sharing

### Troubleshooting
- Check database connection if data isn't saving
- Verify Python version compatibility
- Ensure all dependencies are installed
- Contact support for persistent issues

## SDG 3 Alignment
This application supports UN Sustainable Development Goal 3 (Good Health and Well-being) through:

1. **Mental Health Support**
   - Regular mood and stress monitoring
   - Journal-based reflection tools
   - Early warning system for mental health issues
   - Access to mental wellness resources

2. **Physical Health Promotion**
   - Activity and exercise tracking
   - BMI and vital signs monitoring
   - Health status notifications
   - Personalized wellness recommendations

3. **Preventive Healthcare**
   - Regular health monitoring
   - Early detection of health issues
   - Data-driven health insights
   - Lifestyle improvement suggestions

4. **Healthcare Access**
   - Digital health tracking
   - Personal health data management
   - Health progress monitoring
   - Medical history documentation

## Support and Future Updates 
- Regular software updates
- Technical support via email
- Online documentation 
- Community forum for users 
- Bug reporting system

## Privacy and Security
- End-to-end data encryption
- Secure data storage
- Privacy policy adherence

## Contributing
We welcome contributions! Please see our contributing guidelines for more information.
