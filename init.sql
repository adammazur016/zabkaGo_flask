-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: db:3306
-- Generation Time: Mar 26, 2024 at 01:10 PM
-- Wersja serwera: 8.3.0
-- Wersja PHP: 8.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `app_db`
--

CREATE DATABASE IF NOT EXISTS app_db;
USE app_db;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `places`
--

CREATE TABLE `places` (
  `id` int NOT NULL,
  `long` double NOT NULL,
  `lat` double NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `places`
--

INSERT INTO `places` (`id`, `long`, `lat`, `name`, `description`) VALUES
(1, 12, 13, 'zabka', 'pilsudskiego'),
(2, 17.615812, 50.754552, 'zabkatestdb', ''),
(3, 17.616051, 50.754149, 'test3', ''),
(4, 17.015884034062445, 51.0940211383086, 'Test6', 'Zaporoska 42A, 53-416 Wrocław'),
(5, 17.613560460684557, 50.754277918741785, 'zabka', 'Moniuszki 59, 49-340 Lewin Brzeski'),
(6, 17.615609668247327, 50.751976875524704, 'zabka', 'Kościuszki 37D, 49-340 Lewin Brzeski'),
(7, 17.617025112052747, 50.74918563321704, 'zabka', 'Rynek 3-8/LOK. A, 49-340 Lewin Brzeski');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `login` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `api_key` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `login`, `password`, `api_key`) VALUES
(1, 'adam', 'zaq1@WSX', 'adasdsad'),
(8, 'test', 'test', '12345'),
(11, 'adam12', '123', '12345adamapi');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `visits`
--

CREATE TABLE `visits` (
  `user_id` int NOT NULL,
  `place_id` int NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `visits`
--

INSERT INTO `visits` (`user_id`, `place_id`, `date`) VALUES
(1, 1, '2024-03-19');

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `places`
--
ALTER TABLE `places`
  ADD PRIMARY KEY (`id`);

--
-- Indeksy dla tabeli `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `login` (`login`,`api_key`),
  ADD UNIQUE KEY `login_2` (`login`);

--
-- Indeksy dla tabeli `visits`
--
ALTER TABLE `visits`
  ADD KEY `user_id` (`user_id`,`place_id`),
  ADD KEY `place_id` (`place_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `places`
--
ALTER TABLE `places`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `visits`
--
ALTER TABLE `visits`
  ADD CONSTRAINT `visits_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `visits_ibfk_2` FOREIGN KEY (`place_id`) REFERENCES `places` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
