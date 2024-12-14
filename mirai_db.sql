-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 14, 2024 at 02:19 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mirai_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `mentalhealth_tb`
--

CREATE TABLE `mentalhealth_tb` (
  `mental_health_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `mood` int(11) DEFAULT NULL,
  `stress_level` int(11) DEFAULT NULL,
  `symptoms` text DEFAULT NULL,
  `journaling` text DEFAULT NULL,
  `date` date DEFAULT NULL,
  `cognitive_exercises` enum('Puzzle','Memory Game','Sudoku','Brain Training','Other') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `physicalhealth_tb`
--

CREATE TABLE `physicalhealth_tb` (
  `physical_health_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `date` date NOT NULL DEFAULT curdate(),
  `activity_type` varchar(255) NOT NULL,
  `duration` int(11) NOT NULL,
  `calories_burned` int(11) NOT NULL,
  `bmi_status` varchar(50) DEFAULT NULL,
  `blood_pressure` varchar(20) DEFAULT NULL,
  `heart_rate` int(11) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `height` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `userprofile_tb`
--

CREATE TABLE `userprofile_tb` (
  `profile_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `medical_history` varchar(255) DEFAULT NULL,
  `email` varchar(225) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `userprofile_tb`
--

INSERT INTO `userprofile_tb` (`profile_id`, `user_id`, `full_name`, `address`, `phone_number`, `gender`, `dob`, `medical_history`, `email`) VALUES
(1, 1, 'Lance Edward Dela Rosa', NULL, '09667437998', 'male', '2003-11-06', NULL, 'lanceedwarddelarosa@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `user_tb`
--

CREATE TABLE `user_tb` (
  `user_id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_tb`
--

INSERT INTO `user_tb` (`user_id`, `username`, `password`, `email`) VALUES
(1, 'lanchinggg', '$2b$12$K.mCaUg/7Fd4MghUlRWhSOGMsu070VPtF73LpB7LLOMtnrdxcuanu', 'lanceedwarddelarosa@gmail.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `mentalhealth_tb`
--
ALTER TABLE `mentalhealth_tb`
  ADD PRIMARY KEY (`mental_health_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `physicalhealth_tb`
--
ALTER TABLE `physicalhealth_tb`
  ADD PRIMARY KEY (`physical_health_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `userprofile_tb`
--
ALTER TABLE `userprofile_tb`
  ADD PRIMARY KEY (`profile_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `user_tb`
--
ALTER TABLE `user_tb`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `mentalhealth_tb`
--
ALTER TABLE `mentalhealth_tb`
  MODIFY `mental_health_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `physicalhealth_tb`
--
ALTER TABLE `physicalhealth_tb`
  MODIFY `physical_health_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `userprofile_tb`
--
ALTER TABLE `userprofile_tb`
  MODIFY `profile_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `user_tb`
--
ALTER TABLE `user_tb`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `mentalhealth_tb`
--
ALTER TABLE `mentalhealth_tb`
  ADD CONSTRAINT `mentalhealth_tb_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_tb` (`user_id`);

--
-- Constraints for table `physicalhealth_tb`
--
ALTER TABLE `physicalhealth_tb`
  ADD CONSTRAINT `physicalhealth_tb_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_tb` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `userprofile_tb`
--
ALTER TABLE `userprofile_tb`
  ADD CONSTRAINT `userprofile_tb_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_tb` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
