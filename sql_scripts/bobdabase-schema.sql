-- Assuming the database "bobdabase" and user "root" have been created externally

-- Create schema_version table and populate it
CREATE TABLE schema_version (version INT PRIMARY KEY, updated_at TIMESTAMP DEFAULT NOW());
INSERT INTO schema_version (version) VALUES (1);

-- Create episodes table
CREATE TABLE episodes (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255),
  broadcast_date DATE
);
COMMENT ON TABLE episodes IS 'Stores the painting title and date of each episode for The Joy of Painting.';

-- Create subjects table
CREATE TABLE subjects (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255)
);
COMMENT ON TABLE subjects IS 'Stores the subjects of the episodes and the painting title of the episode for The Joy of Painting.';

-- Create colors table
CREATE TABLE colors (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50),
  hex_code VARCHAR(7)
);
COMMENT ON TABLE colors IS 'Stores the hex_code of the many different colors used as well as painting title of each episode for The Joy of Painting.';

-- Create episodes_subjects junction table
CREATE TABLE episodes_subjects (
  episode_id INTEGER,
  subject_id INTEGER,
  PRIMARY KEY (episode_id, subject_id),
  FOREIGN KEY (episode_id) REFERENCES episodes(id),
  FOREIGN KEY (subject_id) REFERENCES subjects(id)
);
COMMENT ON TABLE episodes_subjects IS 'Junction table that stores the references between subjects and episodes for The Joy of Painting.';

-- Create episodes_colors junction table
CREATE TABLE episodes_colors (
  episode_id INTEGER,
  color_id INTEGER,
  PRIMARY KEY (episode_id, color_id),
  FOREIGN KEY (episode_id) REFERENCES episodes(id),
  FOREIGN KEY (color_id) REFERENCES colors(id)
);
COMMENT ON TABLE episodes_subjects IS 'Junction table that stores the references between colors and episodes for The Joy of Painting.';

-- Set permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO root;
