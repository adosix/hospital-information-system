/*
    Table dropping
*/
use hospital_data;
DROP TABLE IF EXISTS hospital_is_compensation_request;
DROP TABLE IF EXISTS hospital_is_medical_record;
ALTER TABLE hospital_is_Medical_record
DROP CONSTRAINT Ticket;
DROP TABLE IF EXISTS hospital_is_ticket;
DROP TABLE IF EXISTS hospital_is_medical_problem;
DROP TABLE IF EXISTS hospital_is_doctor;
DROP TABLE IF EXISTS hospital_is_compensated_operations;
DROP TABLE IF EXISTS hospital_is_insurance_worker;
DROP TABLE IF EXISTS hospital_is_admin;
DROP TABLE IF EXISTS hospital_is_patient;
DROP TABLE IF EXISTS hospital_is_user ;
