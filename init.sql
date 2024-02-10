CREATE DATABASE appDB;
USE appDB;
CREATE TABLE `ADMIN`(
	`username` CHAR(15) PRIMARY KEY,
    `password` CHAR(12) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `ADMIN` VALUES
	('root','12345678');
SELECT* FROM ADMIN;

CREATE TABLE `CUSTOMER`(
	`username` CHAR(15) PRIMARY KEY,
    `password` CHAR(12) NOT NULL,
    `address` VARCHAR(30) NOT NULL,
    `phone` CHAR(15) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `CUSTOMER` VALUES
	('David','123','cannon park','00000000'),
    ('Jordan','123','mansion','111111111');
SELECT* FROM CUSTOMER;
    
CREATE TABLE `RESTAURANT`(
	`username` CHAR(15) PRIMARY KEY,
    `password` CHAR(12) NOT NULL,
    `address` VARCHAR(30) NOT NULL,
    `phone` CHAR(15) NOT NULL,
    `img_res` VARCHAR(50)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `RESTAURANT` VALUES
	('Student union','123','Inside the warwick campus','telephone1','static/images/res_2.jpg'),
	('IMC','123','Beside the warwick campus','telephone2','static/images/res_1.jpg');
SELECT* FROM RESTAURANT;

CREATE TABLE `DISHES`(
	`dishname` CHAR(15) PRIMARY KEY,
	`restaurant` CHAR(15) NOT NULL,
	`dishinfo` VARCHAR(50) ,
    `nutriention` VARCHAR(30),
    `price` DECIMAL(5,2) NOT NULL,
	`sales` INT(5) NOT NULL,
    `imgsrc` VARCHAR(50),
    `isSpecialty` BOOLEAN,
	FOREIGN KEY (restaurant)
    REFERENCES RESTAURANT(username)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO DISHES VALUES
	('Spicy Fish', 'Student union', 'Songjiang Sea Bass', 'Protein, Vitamins', 26.00, 0, 'static/images/img_2.jpg', 0),
    ('Beef', 'Student union', 'Delicious', 'Protein, Vitamins', 14.50, 0, 'static/images/img_5.jpg', 1),
	('Beef noodle', 'IMC', ' Spicy and Sour', 'Protein, Vitamins', 13.00, 1, 'static/images/img_7.jpg', 0);
SELECT* FROM DISHES;

CREATE TABLE `SHOPPINGCART`(
	`username` CHAR(15),
    `restaurant` CHAR(15),
    `dishname` CHAR(15),
    `price` DECIMAL(5,2) NOT NULL,
    `img_res` VARCHAR(50),
	FOREIGN KEY (username)
    REFERENCES CUSTOMER(username),
	FOREIGN KEY (restaurant)
    REFERENCES RESTAURANT(username),
	FOREIGN KEY (dishname)
    REFERENCES DISHES(dishname),
    PRIMARY KEY (username,restaurant,dishname)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `SHOPPINGCART` VALUES
	('David','Student union','Spicy fish',26.00,'static/images/img_2.jpg');
SELECT* FROM SHOPPINGCART;

CREATE TABLE `ORDER_COMMENT`(
	`orderID` CHAR(15) PRIMARY KEY,
	`username` CHAR(15) NOT NULL,
	`restaurant` VARCHAR(15) NOT NULL,
    `isFinished` BOOLEAN,
    CHECK(isFinished=1 or isFinished =0),
    `cost` DECIMAL(5,2) NOT NULL,
	`c_rank` TINYINT(1),
    CHECK(c_rank BETWEEN 1 AND 5),
    `text` VARCHAR(50),
    `transactiontime` TIMESTAMP(0) NOT NULL,
    CHECK(transactiontime BETWEEN '1970-01-01 00:00:01' AND '2038-01-19 03:14:07'),
    FOREIGN KEY (username)
    REFERENCES CUSTOMER(username),
	FOREIGN KEY (restaurant)
    REFERENCES RESTAURANT(username)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO ORDER_COMMENT VALUES
	('1444000', 'David', 'Student union', 1, 26.00, 1, '1', '2020-11-7 13:14:07'),
    ('1445000', 'David', 'Student union', 1, 14.50, 3, '2', '2020-10-13 20:29:13'),
	('1446000', 'Jordan', 'IMC', 0, 13.00, 5, '3', '2020-10-27 15:45:21');
SELECT* FROM ORDER_COMMENT;