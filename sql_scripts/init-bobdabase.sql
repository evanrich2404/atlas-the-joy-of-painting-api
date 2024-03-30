-- init-db.sql
-- Run this script manually before the main schema setup

CREATE DATABASE bobdabase;

CREATE USER root WITH PASSWORD 'root';

-- Adjust permissions as needed
GRANT ALL PRIVILEGES ON DATABASE bobdabase TO root;
