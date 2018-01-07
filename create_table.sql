CREATE DATABASE IF NOT EXISTS company;

USE company;

DROP TABLE IF EXISTS reviews;

CREATE TABLE IF NOT EXISTS test
(
  review_date DATE,
  review_title VARCHAR(255),
  jobtitle VARCHAR(255),
  currently_employed ENUM('True', 'False'),
  fulltime ENUM('True', 'False'),
  min_years_employment INT,
  region VARCHAR(255),
  region_code INT,
  sub_region VARCHAR(255),
  sub_region_code INT,
  country VARCHAR(255),
  country_code_2 VARCHAR(2),
  country_code_3 VARCHAR(3),
  US_state_code VARCHAR(5),
  city VARCHAR(255),
  location_raw VARCHAR(255),
  rating_overall INT,
  rating_Senior_Management INT,
  rating_Work_Life_Balance INT,
  rating_Culture_and_Values INT,
  rating_Compensation_and_Benefits INT,
  rating_Career_Opportunities INT,
  ceo_opinion ENUM('Approves', 'Disapproves', 'No opinion'),
  ceo_opinion_num INT,
  recommends ENUM('True', 'False'),
  recommends_num INT,
  company_outlook ENUM('Positive', 'Neutral', 'Negative'),
  company_outlook_num INT,
  pros TEXT,
  cons TEXT,
  advice TEXT
);
