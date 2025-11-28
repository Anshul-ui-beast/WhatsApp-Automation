-- USE tgc;

-- CREATE TABLE agents (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(255),
--     agency_name VARCHAR(255),
--     phone_whatsapp VARCHAR(50),
--     email VARCHAR(255),
--     source VARCHAR(100),
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- CREATE TABLE buyers (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(255),
--     phone_whatsapp VARCHAR(50),
--     budget_min INT,
--     budget_max INT,
--     location_pref VARCHAR(255),
--     strategy VARCHAR(255),
--     notes TEXT,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- CREATE TABLE properties (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     title VARCHAR(255),
--     price DECIMAL(15,2) NULL,
--     location VARCHAR(255),
--     source VARCHAR(100), -- scraper, whatsapp_agent, manual
--     agent_id INT NULL,
--     raw_description TEXT,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     INDEX (price),
--     INDEX (location)
-- );

-- CREATE TABLE messages (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     direction ENUM('outbound','inbound'),
--     whatsapp_number VARCHAR(50),
--     role ENUM('agent','buyer') NULL,
--     template_name VARCHAR(255) NULL,
--     message_text TEXT,
--     status VARCHAR(50) NULL, -- sent, delivered, read, failed
--     meta_message_id VARCHAR(255) NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- ALTER TABLE messages
-- ADD classification VARCHAR(50) NULL;

-- ALTER TABLE agents
-- ADD lead_status VARCHAR(50) DEFAULT 'new';

-- SELECT * FROM messages ORDER BY id DESC;

-- SELECT * FROM messages;
-- SELECT * FROM agents;
-- SELECT * FROM buyers;

-- SHOW TABLES FROM tgc;

-- SELECT direction, whatsapp_number, message_text, status, created_at
-- FROM messages
-- ORDER BY id DESC
-- LIMIT 5;

-- SELECT name, phone_whatsapp, lead_status
-- FROM agents
-- ORDER BY id DESC;

ALTER TABLE buyers
ADD COLUMN status VARCHAR(50) DEFAULT 'new';

