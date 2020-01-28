#################################################################################################################
#                                                  L O G B O O K                                                #
#                                                 Database - Setup                                              #
#                                             Author - Marcel Haßlinger                                         #
#                                        Copyright - (c) 2019 / License: MIT                                    #
#                   Description: Databas tables including primary-, secondary- and foreign-keys                 #
#################################################################################################################

CREATE TABLE `user`
(
  `id` CHAR(9) PRIMARY KEY,
  `first_name` VARCHAR(35),
  `last_name` VARCHAR(35),
  `email` VARCHAR(254) UNIQUE,
  `password` CHAR(64),
  `role_id` INT,
  `status` BOOLEAN DEFAULT FALSE
);

CREATE TABLE `role`
(
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(10) UNIQUE,
  `description` VARCHAR(35)
);

CREATE TABLE `car`
(
  `id` VARCHAR(10) PRIMARY KEY,
  `brand` VARCHAR(35),
  `model` VARCHAR(35),
  `fuel` VARCHAR(10),
  `vin` CHAR(17),
  `owner` VARCHAR(35),
  `mot` DATE,
  `wheel` VARCHAR(10),
  `status` BOOLEAN DEFAULT FALSE
);

CREATE TABLE `fleet`
(
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(35) UNIQUE
);

CREATE TABLE `fleet_pool`
(
  `fleet_id` INT,
  `car_id` VARCHAR(10),
  PRIMARY KEY (`fleet_id`, `car_id`)
);

CREATE TABLE `fleet_user`
(
  `fleet_id` INT,
  `user_id` CHAR(9),
  PRIMARY KEY (`fleet_id`, `user_id`)
);

CREATE TABLE `journey`
(
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `car_id` VARCHAR(10),
  `time_start` DATETIME,
  `time_end` DATETIME,
  `address_id_start` INT,
  `address_id_end` INT,
  `reason` VARCHAR(35),
  `visited` VARCHAR(35),
  `km_start` INT,
  `km_business` INT,
  `km_commute` INT,
  `km_private` INT,
  `km_end` INT,
  `bill_id` INT,
  `user_id` CHAR(9)
);

CREATE TABLE `bill`
(
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `liter` DOUBLE,
  `amount` DOUBLE,
  `liter_avg` DOUBLE,
  `amount_other` DOUBLE,
  `picture` BLOB
);

CREATE TABLE `address`
(
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(35),
  `group` VARCHAR(10),
  `street` VARCHAR(35),
  `number` VARCHAR(10),
  `zipcode` CHAR(5),
  `city` VARCHAR(35),
  `user_id` CHAR(9),
  INDEX (`name`)
);

CREATE TABLE `log`
(
  `timestamp` DATETIME,
  `user_id` CHAR(9),
  `info` VARCHAR(255),
  PRIMARY KEY (`timestamp`, `user_id`)
);

ALTER TABLE `user` ADD FOREIGN KEY (`role_id`) REFERENCES `role` (`id`);

ALTER TABLE `journey` ADD FOREIGN KEY (`car_id`) REFERENCES `car` (`id`);

ALTER TABLE `journey` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

ALTER TABLE `journey` ADD FOREIGN KEY (`address_id_start`) REFERENCES `address` (`id`);

ALTER TABLE `journey` ADD FOREIGN KEY (`address_id_end`) REFERENCES `address` (`id`);

ALTER TABLE `journey` ADD FOREIGN KEY (`bill_id`) REFERENCES `bill` (`id`);

ALTER TABLE `fleet_pool` ADD FOREIGN KEY (`fleet_id`) REFERENCES `fleet` (`id`);

ALTER TABLE `fleet_pool` ADD FOREIGN KEY (`car_id`) REFERENCES `car` (`id`);

ALTER TABLE `log` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

ALTER TABLE `address` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

ALTER TABLE `fleet_user` ADD FOREIGN KEY (`fleet_id`) REFERENCES `fleet` (`id`);

ALTER TABLE `fleet_user` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);
