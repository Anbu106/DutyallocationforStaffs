-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 16, 2024 at 04:07 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `exam_hall`
--

-- --------------------------------------------------------

--
-- Table structure for table `hall_admin`
--

CREATE TABLE `hall_admin` (
  `id` int(10) NOT NULL,
  `username` varchar(10) NOT NULL,
  `password` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `hall_admin`
--

INSERT INTO `hall_admin` (`id`, `username`, `password`) VALUES
(1, 'admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `hall_allocate`
--

CREATE TABLE `hall_allocate` (
  `id` int(11) NOT NULL,
  `sub_code` varchar(20) NOT NULL,
  `sub_name` varchar(40) NOT NULL,
  `date` varchar(20) NOT NULL,
  `hall_name` varchar(20) NOT NULL,
  `hall_image` varchar(100) NOT NULL,
  `staff_name` varchar(20) NOT NULL,
  `staff_user` varchar(20) NOT NULL,
  `staff_email` varchar(40) NOT NULL,
  `staff_mobile` bigint(20) NOT NULL,
  `r_date` varchar(20) NOT NULL,
  `staff_id` varchar(20) NOT NULL,
  `hod_name` varchar(20) NOT NULL,
  `semester` varchar(20) NOT NULL,
  `changee` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `hall_allocate`
--

INSERT INTO `hall_allocate` (`id`, `sub_code`, `sub_name`, `date`, `hall_name`, `hall_image`, `staff_name`, `staff_user`, `staff_email`, `staff_mobile`, `r_date`, `staff_id`, `hod_name`, `semester`, `changee`) VALUES
(1, 'SD111', 'Chemistry', '2024-04-11', 'HS12', '2da01999-9d64-4b92-bf0f-2ca87f84ddae_exam-room-plate.jpg', 'janaki raja ram', 'ST0000', 'huwaidom@gmail.com', 8838468320, 'March 11, 2024', 'HOD00', 'ramu raja p', '2', 1),
(2, 'EN12', 'Communication', '2024-04-05', '', '', '', '', '', 0, 'March 20, 2024', 'HOD00', 'ramu raja p', '5', 0),
(3, 'MA12', 'Maths', '2024-04-09', '', '', '', '', '', 0, 'March 20, 2024', 'HOD00', 'ramu raja p', '3', 0);

-- --------------------------------------------------------

--
-- Table structure for table `hall_dept`
--

CREATE TABLE `hall_dept` (
  `id` int(10) NOT NULL,
  `dept` varchar(20) NOT NULL,
  `r_date` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `hall_dept`
--

INSERT INTO `hall_dept` (`id`, `dept`, `r_date`) VALUES
(1, 'BBA', 'March 10, 2024'),
(2, 'B.com', 'March 10, 2024'),
(3, 'M.com', 'March 10, 2024'),
(4, 'MBA', 'March 10, 2024'),
(5, 'M.sc', 'March 10, 2024'),
(6, 'B.sc', 'March 10, 2024');

-- --------------------------------------------------------

--
-- Table structure for table `hall_exam`
--

CREATE TABLE `hall_exam` (
  `id` int(10) NOT NULL,
  `exam_name` varchar(50) NOT NULL,
  `sub_code` varchar(20) NOT NULL,
  `sub_name` varchar(50) NOT NULL,
  `dept` varchar(20) NOT NULL,
  `semester` varchar(20) NOT NULL,
  `date` varchar(20) NOT NULL,
  `r_date` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `hall_exam`
--


-- --------------------------------------------------------

--
-- Table structure for table `hall_exam1`
--

CREATE TABLE `hall_exam1` (
  `id` varchar(10) NOT NULL,
  `exam_name` varchar(20) NOT NULL,
  `r_date` varchar(20) NOT NULL,
  `dept` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `hall_exam1`
--

INSERT INTO `hall_exam1` (`id`, `exam_name`, `r_date`, `dept`) VALUES
('1', 'IAT-1', 'March 10, 2024', 'M.sc');

-- --------------------------------------------------------

--
-- Table structure for table `hall_hall`
--

CREATE TABLE `hall_hall` (
  `id` int(10) NOT NULL,
  `hall_name` varchar(20) NOT NULL,
  `capacity` varchar(20) NOT NULL,
  `dept` varchar(20) NOT NULL,
  `image` varchar(100) NOT NULL,
  `r_date` varchar(20) NOT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `hall_hall`
--

INSERT INTO `hall_hall` (`id`, `hall_name`, `capacity`, `dept`, `image`, `r_date`) VALUES
(1, 'HS12', '35', 'M.sc', '2da01999-9d64-4b92-bf0f-2ca87f84ddae_exam-room-plate.jpg', 'March 10, 2024'),
(2, 'HS11', '23', 'M.sc', 'c36358eb-e5bb-46ec-851b-0704d06fc2e3_logo.png', 'March 20, 2024');

-- --------------------------------------------------------

--
-- Table structure for table `hall_staff`
--

CREATE TABLE `hall_staff` (
  `id` int(10) NOT NULL,
  `staff_type` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` varchar(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `address` varchar(40) NOT NULL,
  `dept` varchar(20) NOT NULL,
  `staff_id` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `r_date` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `hall_staff`
--

INSERT INTO `hall_staff` (`id`, `staff_type`, `name`, `mobile`, `email`, `address`, `dept`, `staff_id`, `password`, `r_date`) VALUES
(1, 'staff', 'janaki raja ram', '8838468320', 'huwaidom@gmail.com', '12, new str', 'M.sc', 'ST0000', '1234', 'March 10, 2024'),
(2, 'hod', 'ramu raja p', '8838468320', 'huwaidom@gmail.com', '12, new str', 'M.sc', 'HOD00', '1234', 'March 10, 2024'),
(3, 'staff', 'ca na ra', '8148956634', 'kalirajan3079@gmail.com', '12, new str', 'M.sc', 'ST0001', '1234', 'March 20, 2024');
