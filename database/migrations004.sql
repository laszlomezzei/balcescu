ALTER TABLE Stores ADD CONSTRAINT stores_storegroups_ibfk_2 FOREIGN KEY(store_group_id) REFERENCES StoreGroups(id);

ALTER TABLE Users ADD CONSTRAINT users_storegroups_ibfk_3 FOREIGN KEY(store_group_id) REFERENCES StoreGroups(id);

CREATE TABLE IF NOT EXISTS GuidelineGroups (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(255) DEFAULT NULL,
  isArchived tinyint(1) NOT NULL DEFAULT 0,
  parent_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY parent_id (parent_id),
  CONSTRAINT guidelinegroups_ibfk_1 FOREIGN KEY (parent_id) REFERENCES Companies (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


ALTER TABLE Guidelines ADD COLUMN guideline_group_id INT(11) NULL;

ALTER TABLE Guidelines ADD CONSTRAINT guidelines_guidelinegroups_ibfk_2 FOREIGN KEY(guideline_group_id) REFERENCES GuidelineGroups(id);
