-- Lecture 3: initial schemas

CREATE SCHEMA IF NOT EXISTS weather;
COMMENT ON SCHEMA weather IS 'Open-Meteo API weather data';

CREATE SCHEMA IF NOT EXISTS currency;
COMMENT ON SCHEMA currency IS 'NBG currency exchange data';

CREATE SCHEMA IF NOT EXISTS seismic;
COMMENT ON SCHEMA seismic IS 'USGS earthquake data';
