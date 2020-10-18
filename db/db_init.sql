/* Table creations */
use hospital_data;

CREATE TABLE hospital_is_user(
    id INTEGER NOT NULL primary key AUTO_INCREMENT,
    First_name varchar(255) NOT NULL,
    Last_name varchar(255) NOT NULL,
    Password varchar(255) NOT NULL,
    Email varchar(255) CHECK ( REGEXP_LIKE(Email, '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}') ),
    TelNum varchar(255) CHECK ( REGEXP_LIKE(TelNum, '^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$')),
    State varchar(255),
    City varchar(255),
    Street varchar(255)
);
ALTER TABLE hospital_is_user AUTO_INCREMENT=10000;
 CREATE TABLE hospital_is_insurance_worker(
     id INTEGER NOT NULL PRIMARY KEY REFERENCES hospital_is_user(id),
     CONSTRAINT User FOREIGN KEY (id) REFERENCES hospital_is_user(id)

 );
 CREATE TABLE hospital_is_patient(
     id INTEGER NOT NULL PRIMARY KEY REFERENCES hospital_is_user(id),
     CONSTRAINT usr FOREIGN KEY (id) REFERENCES hospital_is_user(id)
 );
 CREATE TABLE hospital_is_doctor(
     id INTEGER NOT NULL PRIMARY KEY REFERENCES hospital_is_user(id),
     CONSTRAINT usr2 FOREIGN KEY (id) REFERENCES hospital_is_user(id)
 );
 CREATE TABLE hospital_is_admin(
     id INTEGER NOT NULL PRIMARY KEY REFERENCES hospital_is_user(id),
     CONSTRAINT usr3 FOREIGN KEY (id) REFERENCES hospital_is_user(id)
 );
 CREATE TABLE hospital_is_compensated_operations(
    Operation varchar(255) NOT NULL primary key ,
    Description varchar(1024),
    Creator INTEGER NOT NULL,

    CONSTRAINT Insurance_worker FOREIGN KEY (Creator) REFERENCES hospital_is_insurance_worker(id)
 );
 CREATE TABLE hospital_is_medical_problem(
    id INTEGER NOT NULL primary key ,
    Patient_ID INTEGER NOT NULL,
    Doctor_ID INTEGER NOT NULL,
    Title varchar(255) NOT NULL,
    Description varchar(1024)  NOT NULL,
    Status  varchar(255) NOT NULL,

    CONSTRAINT Doctor FOREIGN KEY (Doctor_ID) REFERENCES hospital_is_doctor(id),
    CONSTRAINT Patient FOREIGN KEY (Patient_ID) REFERENCES hospital_is_patient(id)
 );
  CREATE TABLE hospital_is_ticket(
    id INTEGER NOT NULL primary key,
    Medical_problem_ID INTEGER NOT NULL ,
    Doctor_ID INTEGER NOT NULL ,
    Operation  varchar(255) NOT NULL,
    Status  varchar(255) NOT NULL,
    Description varchar(1024),

    CONSTRAINT Examining_doctor FOREIGN KEY (Doctor_ID) REFERENCES hospital_is_doctor(id),
    CONSTRAINT Medical_problem FOREIGN KEY (Medical_problem_ID) REFERENCES hospital_is_medical_problem(id)
 );
   CREATE TABLE hospital_is_medical_record(
    id INTEGER NOT NULL primary key ,
    Ticket_ID INTEGER NOT NULL ,
    Title  varchar(255) NOT NULL,
    Description  varchar(1024) NOT NULL,
    Images varchar(255),

    CONSTRAINT Ticket FOREIGN KEY (Ticket_ID) REFERENCES hospital_is_ticket(id)

 );
 CREATE TABLE hospital_is_compensation_request(
    id INTEGER NOT NULL PRIMARY KEY REFERENCES hospital_is_ticket(id),
    Status varchar(255) NOT NULL
 );
  
  CREATE TABLE hospital_is_post(
    id INTEGER NOT NULL PRIMARY KEY REFERENCES hospital_is_ticket(id),
    title varchar(100) NOT NULL,
    content varchar(100) NOT NULL,
    date_posted varchar(100) NOT NULL,
    author varchar(100) NOT NULL
 );

