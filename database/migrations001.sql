CREATE TABLE IF NOT EXISTS Companies (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(255) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS Stores (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(255) DEFAULT NULL,
  address varchar(255) DEFAULT NULL,
  parent_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY parent_id (parent_id),
  CONSTRAINT stores_ibfk_1 FOREIGN KEY (parent_id) REFERENCES Companies (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS Users (
  id int(11) NOT NULL AUTO_INCREMENT,
  email varchar(255) DEFAULT NULL,
  username varchar(255) DEFAULT NULL,
  password varchar(255) DEFAULT NULL,
  roles varchar(255) DEFAULT NULL,
  parent_id int(11) DEFAULT NULL,
  store_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY parent_id (parent_id),
  KEY store_id (store_id),
  CONSTRAINT users_ibfk_1 FOREIGN KEY (parent_id) REFERENCES Companies (id),
  CONSTRAINT users_ibfk_2 FOREIGN KEY (store_id) REFERENCES Stores (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS ManualGroups (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(255) DEFAULT NULL,
  parent_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY parent_id (parent_id),
  CONSTRAINT manualgroups_ibfk_1 FOREIGN KEY (parent_id) REFERENCES Companies (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS Manuals (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(255) DEFAULT NULL,
  parent_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY parent_id (parent_id),
  CONSTRAINT manuals_ibfk_1 FOREIGN KEY (parent_id) REFERENCES ManualGroups (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS TagGroups (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(255) DEFAULT NULL,
  search_name varchar(255) DEFAULT NULL,
  mandatoryFixture tinyint(1) DEFAULT NULL,
  mandatoryProduct tinyint(1) DEFAULT NULL,
  parent_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY parent_id (parent_id),
  CONSTRAINT taggroups_ibfk_1 FOREIGN KEY (parent_id) REFERENCES Companies (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS Tags (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(255) DEFAULT NULL,
  parent_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY parent_id (parent_id),
  CONSTRAINT tags_ibfk_1 FOREIGN KEY (parent_id) REFERENCES TagGroups (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



CREATE TABLE IF NOT EXISTS Assets (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(255) DEFAULT NULL,
  search_name varchar(255) DEFAULT NULL,
  creation_date datetime DEFAULT NULL,
  type varchar(50) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS Fixtures (
  id int(11) NOT NULL,
  fixtureId varchar(255) DEFAULT NULL,
  search_fixtureId varchar(255) DEFAULT NULL,
  parent_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY parent_id (parent_id),
  CONSTRAINT fixtures_ibfk_1 FOREIGN KEY (id) REFERENCES Assets (id),
  CONSTRAINT fixtures_ibfk_2 FOREIGN KEY (parent_id) REFERENCES Companies (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS AssociationTagsToFixture (
  tag_id int(11) DEFAULT NULL,
  fixture_id int(11) DEFAULT NULL,
  KEY tag_id (tag_id),
  KEY fixture_id (fixture_id),
  CONSTRAINT associationtagstofixture_ibfk_1 FOREIGN KEY (tag_id) REFERENCES Tags (id),
  CONSTRAINT associationtagstofixture_ibfk_2 FOREIGN KEY (fixture_id) REFERENCES Fixtures (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS Products (
  id int(11) NOT NULL,
  productId varchar(255) DEFAULT NULL,
  search_productId varchar(255) DEFAULT NULL,
  parent_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY parent_id (parent_id),
  CONSTRAINT products_ibfk_1 FOREIGN KEY (id) REFERENCES Assets (id),
  CONSTRAINT products_ibfk_2 FOREIGN KEY (parent_id) REFERENCES Companies (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS AssociationTagsToProducts (
  tag_id int(11) DEFAULT NULL,
  product_id int(11) DEFAULT NULL,
  KEY tag_id (tag_id),
  KEY product_id (product_id),
  CONSTRAINT associationtagstoproducts_ibfk_1 FOREIGN KEY (tag_id) REFERENCES Tags (id),
  CONSTRAINT associationtagstoproducts_ibfk_2 FOREIGN KEY (product_id) REFERENCES Products (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS Images (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(255) DEFAULT NULL,
  imageWidth int(11) DEFAULT NULL,
  imageHeight int(11) DEFAULT NULL,
  servingURL varchar(255) DEFAULT NULL,
  parent_id int(11) DEFAULT NULL,
  asset_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY parent_id (parent_id),
  KEY asset_id (asset_id),
  CONSTRAINT images_ibfk_1 FOREIGN KEY (parent_id) REFERENCES Companies (id),
  CONSTRAINT images_ibfk_2 FOREIGN KEY (asset_id) REFERENCES Assets (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS Devices (
  id int(11) NOT NULL AUTO_INCREMENT,
  deviceId varchar(255) DEFAULT NULL,
  tokenId varchar(255) DEFAULT NULL,
  parent_id int(11) DEFAULT NULL,
  store_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY parent_id (parent_id),
  KEY store_id (store_id),
  CONSTRAINT devices_ibfk_1 FOREIGN KEY (parent_id) REFERENCES Companies (id),
  CONSTRAINT devices_ibfk_2 FOREIGN KEY (store_id) REFERENCES Stores (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS Guidelines (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(255) DEFAULT NULL,
  search_name varchar(255) DEFAULT NULL,
  description varchar(255) DEFAULT NULL,
  search_description varchar(255) DEFAULT NULL,
  dueDate datetime DEFAULT NULL,
  photoRequired tinyint(1) DEFAULT NULL,
  publicationDate datetime DEFAULT NULL,
  parent_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY parent_id (parent_id),
  CONSTRAINT guidelines_ibfk_1 FOREIGN KEY (parent_id) REFERENCES Companies (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS GuidelineConversations (
  id int(11) NOT NULL AUTO_INCREMENT,
  messageCount int(11) DEFAULT NULL,
  unread tinyint(1) DEFAULT NULL,
  updateDate datetime DEFAULT NULL,
  parent_id int(11) DEFAULT NULL,
  store_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY parent_id (parent_id),
  KEY store_id (store_id),
  CONSTRAINT guidelineconversations_ibfk_1 FOREIGN KEY (parent_id) REFERENCES Guidelines (id),
  CONSTRAINT guidelineconversations_ibfk_2 FOREIGN KEY (store_id) REFERENCES Stores (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS GuidelineFeedbacks (
  id int(11) NOT NULL AUTO_INCREMENT,
  creationDate datetime DEFAULT NULL,
  feedback varchar(255) DEFAULT NULL,
  parent_id int(11) DEFAULT NULL,
  store_id int(11) DEFAULT NULL,
  user_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY parent_id (parent_id),
  KEY store_id (store_id),
  KEY user_id (user_id),
  CONSTRAINT guidelinefeedbacks_ibfk_1 FOREIGN KEY (parent_id) REFERENCES Guidelines (id),
  CONSTRAINT guidelinefeedbacks_ibfk_2 FOREIGN KEY (store_id) REFERENCES Stores (id),
  CONSTRAINT guidelinefeedbacks_ibfk_3 FOREIGN KEY (user_id) REFERENCES Users (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS GuidelineFeedbackPhotos (
  id int(11) NOT NULL AUTO_INCREMENT,
  dashboardImageName varchar(255) DEFAULT NULL,
  imageName int(11) DEFAULT NULL,
  imageHeight int(11) DEFAULT NULL,
  imageWidth int(11) DEFAULT NULL,
  servingURL varchar(255) DEFAULT NULL,
  parent_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY parent_id (parent_id),
  CONSTRAINT guidelinefeedbackphotos_ibfk_1 FOREIGN KEY (parent_id) REFERENCES GuidelineFeedbacks (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS GuidelineFeedbackPhotoThumbs (
  id int(11) NOT NULL AUTO_INCREMENT,
  dashboardImageName varchar(255) DEFAULT NULL,
  imageName varchar(255) DEFAULT NULL,
  imageHeight int(11) DEFAULT NULL,
  imageWidth int(11) DEFAULT NULL,
  servingURL varchar(255) DEFAULT NULL,
  parent_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY parent_id (parent_id),
  CONSTRAINT guidelinefeedbackphotothumbs_ibfk_1 FOREIGN KEY (parent_id) REFERENCES GuidelineConversations (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS Canvases (
  id int(11) NOT NULL AUTO_INCREMENT,
  backgroundName varchar(255) DEFAULT NULL,
  backgroundId int(11) DEFAULT NULL,
  backgroundHeight int(11) DEFAULT NULL,
  backgroundWidth int(11) DEFAULT NULL,
  imageRatio float DEFAULT NULL,
  `order` int(11) DEFAULT NULL,
  parent_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY parent_id (parent_id),
  CONSTRAINT canvases_ibfk_1 FOREIGN KEY (parent_id) REFERENCES Guidelines (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE IF NOT EXISTS Hotspots (
  id int(11) NOT NULL AUTO_INCREMENT,
  assetId int(11) DEFAULT NULL,
  imageRatio float DEFAULT NULL,
  `order` int(11) DEFAULT NULL,
  posx float DEFAULT NULL,
  posy float DEFAULT NULL,
  quantity int(11) DEFAULT NULL,
  productImageName varchar(255) DEFAULT NULL,
  productName varchar(255) DEFAULT NULL,
  search_productName varchar(255) DEFAULT NULL,
  productNumber varchar(255) DEFAULT NULL,
  search_productNumber varchar(255) DEFAULT NULL,
  parent_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY parent_id (parent_id),
  CONSTRAINT hotspots_ibfk_1 FOREIGN KEY (parent_id) REFERENCES Canvases (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

