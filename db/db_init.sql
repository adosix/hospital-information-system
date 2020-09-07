
CREATE TABLE hotel_reservation_system_app_post (
    id          INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,
    room_number  INT NOT NULL,
    sleeps      INT NOT NULL,
    price       INT NOT NULL,
    wifi        BOOLEAN,
    tv          BOOLEAN,
    parking_slot_included BOOLEAN

);

CREATE TABLE hotel_reservation_system_app_guests (
    id          INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,
    name        VARCHAR(40) NOT NULL

);

DESCRIBE hotel_reservation_system_app_post;
SELECT * FROM hotel_reservation_system_app_post;
SHOW TABLES;