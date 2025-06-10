-- schema.sql for PostgreSQL

-- Drop tables in reverse order of creation to avoid foreign key conflicts
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS Banks;

-- Create Banks Table
-- This table stores the unique bank names.
CREATE TABLE Banks (
    bank_id SERIAL PRIMARY KEY,  -- SERIAL is an auto-incrementing integer in PostgreSQL
    bank_name VARCHAR(100) NOT NULL UNIQUE
);

-- Create Reviews Table
-- This table stores all the review data, linking back to the Banks table.
CREATE TABLE Reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INTEGER,
    review_text TEXT,  -- TEXT can hold long strings of text
    rating INTEGER,
    review_date DATE,
    sentiment_label VARCHAR(20),
    sentiment_score NUMERIC(5, 4), -- NUMERIC is good for precise decimal values
    identified_themes VARCHAR(255),
    source VARCHAR(50),
    
    -- Establish the foreign key constraint
    FOREIGN KEY(bank_id) REFERENCES Banks(bank_id)
);


COMMENT ON TABLE Banks IS 'Stores information about the unique banks being analyzed.';
COMMENT ON TABLE Reviews IS 'Stores scraped and processed review data from the Google Play Store.';