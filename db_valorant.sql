-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 24, 2026 at 08:27 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_valorant`
--

-- --------------------------------------------------------

--
-- Table structure for table `tournaments`
--

CREATE TABLE `tournaments` (
  `id` int NOT NULL,
  `nama_tournament` varchar(255) NOT NULL,
  `deskripsi` text,
  `tanggal_dibuat` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `link_tournament` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tournaments`
--

INSERT INTO `tournaments` (`id`, `nama_tournament`, `deskripsi`, `tanggal_dibuat`, `link_tournament`) VALUES
(11, 'Jadwal Valorant Champions Tour', '\r\nSEMUA WILAYAH\r\nStage 1\r\n1 April - 24 Mei', '2026-04-11 13:12:47', 'https://valorantesports.com/id-ID'),
(12, 'VCT ASIA PASIFIC 2026 II Stage 1', 'Valorant Champions Tour 2026\r\n⋅\r\nStage 1\r\n⋅\r\nPacific\r\nVCT 2026: Pacific Stage 1\r\nPart of the Valorant Champions Tour, Riot\'s official 2026 tournament circuit.\r\nDates\r\nApr 3, 2026 - May 17, 2026\r\nPrize\r\nTBD\r\nLocation\r\n Thiskyhall Sala Convention Center, Ho Chi Minh City', '2026-04-12 09:16:35', 'https://www.vlr.gg/event/2775/vct-2026-pacific-stage-1'),
(13, 'MASTER TORONTO 2026', 'Swiss Stage: June 7th - 11th, 2025\r\n8 team Swiss System Format\r\n2nd and 3rd place teams from the International Leagues\r\nOpening round matches a 2nd place team against a 3rd place team from another region\r\nAll matches are Bo3\r\nTop 4 teams proceed to Playoffs\r\nBottom 4 teams are eliminated\r\nPlayoffs: June 13th - 22nd, 2025\r\n8 team Double-Elimination bracket\r\n4 teams from the Swiss Stage\r\nThe 4 winners from each International League\r\nAll matches (excl. Lower Bracket Final and Grand Final) are Bo3\r\nLower Bracket Final and Grand Final are Bo5', '2026-04-13 08:16:13', 'https://liquipedia.net/valorant/VCT/2025/Stage_2/Masters');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','user') DEFAULT 'user',
  `is_online` int DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`, `is_online`) VALUES
(1, 'admin_dzaky', 'Admin123', 'admin', 0),
(3, 'ZAKYYY', 'Zaky123', 'user', 0),
(4, 'Bagasbagus', 'Bagus123', 'user', 0),
(5, 'Asepjarwo', 'Jarwo123', 'user', 0),
(6, 'RANZ', 'Fahran123', 'user', 0),
(7, 'rafifauzan', 'rafi123', 'user', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tournaments`
--
ALTER TABLE `tournaments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tournaments`
--
ALTER TABLE `tournaments`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
