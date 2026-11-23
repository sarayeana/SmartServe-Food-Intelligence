
-- =====================================================
-- SMARTSERVE FOOD INTELLIGENCE
-- DATABASE CREATION
-- MySQL 8.0+
-- =====================================================

CREATE DATABASE IF NOT EXISTS smartserve_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE smartserve_db;

-- Confirm selected database
SELECT DATABASE() AS active_database;
