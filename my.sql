CREATE TABLE entries (
  id int(11) NOT NULL AUTO_INCREMENT,
  ip varchar(16) NOT NULL,
  requests int(11) DEFAULT NULL,
  reputation tinyint(1) DEFAULT NULL,
  CHANGED timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CREATED timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
)