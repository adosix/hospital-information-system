/* Table creations */


CREATE TABLE hospital_information_system_app_User(
    User_ID INTEGER NOT NULL primary key,
    First_name varchar(255) NOT NULL,
    Last_name varchar(255) NOT NULL,
    Password varchar(255) NOT NULL,
    Email varchar(255) CHECK ( REGEXP_LIKE(Email, '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}') ),
    TelNum varchar(255) CHECK ( REGEXP_LIKE(TelNum, '^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$')),
    State varchar(255),
    City varchar(255),
    Street varchar(255)
);
 CREATE TABLE hospital_information_system_app_Insurance_worker(
     Insurance_worker_ID INTEGER NOT NULL PRIMARY KEY REFERENCES hospital_information_system_app_User(User_ID)
 );
 CREATE TABLE hospital_information_system_app_Patient(
     Patient_ID INTEGER NOT NULL PRIMARY KEY REFERENCES hospital_information_system_app_User(User_ID)
 );
 CREATE TABLE hospital_information_system_app_Doctor(
     Doctor_ID INTEGER NOT NULL PRIMARY KEY REFERENCES hospital_information_system_app_User(User_ID)
 );
 CREATE TABLE hospital_information_system_app_Admin(
     Admin_ID INTEGER NOT NULL PRIMARY KEY REFERENCES hospital_information_system_app_User(User_ID)
 );
 CREATE TABLE hospital_information_system_app_Compensated_operations(
    Operation varchar(255) NOT NULL primary key,
    Description varchar(1024),
    Creator INTEGER NOT NULL,

    CONSTRAINT Insurance_worker FOREIGN KEY (Creator) REFERENCES hospital_information_system_app_Insurance_worker(Insurance_worker_ID)
 );
 CREATE TABLE hospital_information_system_app_Medical_problem(
    Medical_problem_ID INTEGER NOT NULL primary key,
    Patient_ID INTEGER NOT NULL,
    Doctor_ID INTEGER NOT NULL,
    Title varchar(255) NOT NULL,
    Description varchar(1024)  NOT NULL,
    Status  varchar(255) NOT NULL,

    CONSTRAINT Doctor FOREIGN KEY (Doctor_ID) REFERENCES hospital_information_system_app_Doctor(Doctor_ID),
    CONSTRAINT Patient FOREIGN KEY (Patient_ID) REFERENCES hospital_information_system_app_Patient(Patient_ID)
 );

  CREATE TABLE hospital_information_system_app_Ticket(
    Ticket_ID INTEGER NOT NULL primary key,
    Medical_problem_ID INTEGER NOT NULL ,
    Doctor_ID INTEGER NOT NULL ,
    Operation  varchar(255) NOT NULL,
    Status  varchar(255) NOT NULL,
    Description varchar(1024),

    CONSTRAINT Examining_doctor FOREIGN KEY (Doctor_ID) REFERENCES hospital_information_system_app_Doctor(Doctor_ID),
    CONSTRAINT Medical_problem FOREIGN KEY (Medical_problem_ID) REFERENCES hospital_information_system_app_Medical_problem(Medical_problem_ID)
 );
   CREATE TABLE hospital_information_system_app_Medical_record(
    Medical_record_ID INTEGER NOT NULL primary key,
    Ticket_ID INTEGER NOT NULL ,
    Title  varchar(255) NOT NULL,
    Description  varchar(1024) NOT NULL,
    Images varchar(255),

    CONSTRAINT Ticket FOREIGN KEY (Ticket_ID) REFERENCES hospital_information_system_app_Ticket(Ticket_ID)

 );
 CREATE TABLE hospital_information_system_app_Compensation_request(
    Ticket_ID INTEGER NOT NULL PRIMARY KEY REFERENCES hospital_information_system_app_Ticket(Ticket_ID),
    Status varchar(255) NOT NULL
 );