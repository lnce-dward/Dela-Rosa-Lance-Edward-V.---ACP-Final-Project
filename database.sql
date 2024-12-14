--you can paste it to the terminal



-- Create Database
CREATE DATABASE Mirai_DB;
-- Call database
USE Mirai_DB;
-- Create Tables
CREATE TABLE User_TB (
user_id INT(11) NOT NULL AUTO_INCREMENT,
username VARCHAR(255) NOT NULL UNIQUE,
password VARCHAR(255) NOT NULL,
email VARCHAR(255),
PRIMARY KEY (user_id)
);

CREATE TABLE User_Profile_TB (
profile_id INT(11) NOT NULL AUTO_INCREMENT,
user_id INT(11),
full_name VARCHAR(255),
address VARCHAR(255),
phone_number VARCHAR(20),
gender VARCHAR(10),
dob DATE,
medical_history VARCHAR(255),
PRIMARY KEY (profile_id),
FOREIGN KEY (user_id) REFERENCES User_TB(user_id)
);

CREATE TABLE PhysicalHealth_TB (
physical_health_id INT(11) NOT NULL AUTO_INCREMENT,
user_id INT(11) NOT NULL,
date DATE NOT NULL DEFAULT CURDATE(),
activity_type VARCHAR(255) NOT NULL,
duration INT(11) NOT NULL,
calories_burned INT(11) NOT NULL,
bmi_status VARCHAR(50),
blood_pressure VARCHAR(20),
heart_rate INT(11),
weight FLOAT,
height FLOAT,
PRIMARY KEY (physical_health_id),
FOREIGN KEY (user_id) REFERENCES User_TB(user_id));

CREATE TABLE MentalHealth_TB (
mental_health_id INT(11) NOT NULL AUTO_INCREMENT,
user_id INT(11),
mood INT(11),
stress_level INT(11),
symptoms TEXT,
journaling TEXT,
date DATE,
cognitive_exercises ENUM('Puzzle', 'Memory Game', 'Sudoku', 'Brain
Training', 'Other'),
PRIMARY KEY (mental_health_id),
FOREIGN KEY (user_id) REFERENCES User_TB(user_id)
);
