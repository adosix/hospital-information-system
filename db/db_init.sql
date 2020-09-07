
CREATE TABLE hotel_reservation_system_app_post (
    id          INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,
    roomNumber  INT NOT NULL,
    sleeps      INT NOT NULL,
    price       INT NOT NULL,
    wifi        BOOLEAN,
    tv          BOOLEAN,
    parking_slot_included BOOLEAN

);

DESCRIBE hotel_reservation_system_app_post;
SELECT * FROM hotel_reservation_system_app_post;
SHOW TABLES;