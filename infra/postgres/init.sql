-- Aero-Metrics (APIx) Database Initialisation Script
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Reference Routes & Weights
CREATE TABLE IF NOT EXISTS route_weights (
    route_code VARCHAR(10) PRIMARY KEY,
    origin VARCHAR(3) NOT NULL,
    destination VARCHAR(3) NOT NULL,
    weight NUMERIC(6, 4) NOT NULL,
    effective_from DATE NOT NULL,
    effective_to DATE,
    weight_source VARCHAR(100)
);

-- Lead-Time Horizon Weights
CREATE TABLE IF NOT EXISTS lead_time_weights (
    horizon VARCHAR(5) PRIMARY KEY,
    lead_time_days INTEGER NOT NULL,
    weight NUMERIC(4, 2) NOT NULL,
    description VARCHAR(100)
);
