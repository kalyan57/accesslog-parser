CREATE TABLE pentries (
  id SERIAL PRIMARY KEY,
  ip VARCHAR(16) NOT NULL,
  requests INT DEFAULT NULL,
  reputation SMALLINT DEFAULT NULL,
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  changed TIMESTAMP
)

CREATE OR REPLACE FUNCTION update_changed()
RETURNS TRIGGER AS $$
BEGIN
   NEW.changed = now(); 
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER upd_pentries_changed BEFORE UPDATE
    ON pentries FOR EACH ROW EXECUTE PROCEDURE 
    update_changed();