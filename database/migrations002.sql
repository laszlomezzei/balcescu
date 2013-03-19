CREATE TABLE IF NOT EXISTS StoreGroups (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(255) DEFAULT NULL,
  isArchived tinyint(255) NOT NULL DEFAULT 0,
  parent_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY user_id (parent_id),
  CONSTRAINT storegroups_ibfk_1 FOREIGN KEY (parent_id) REFERENCES Companies (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


ALTER TABLE Users ADD COLUMN isArchived TINYINT(1) NOT NULL DEFAULT 0;
ALTER TABLE Users ADD COLUMN store_group_id INT(11) NULL;


ALTER TABLE Stores ADD COLUMN isArchived TINYINT(1) NOT NULL DEFAULT 0;
ALTER TABLE Stores ADD COLUMN store_group_id INT(11) NULL;

