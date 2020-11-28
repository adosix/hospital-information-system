/*
    Table dropping
*/
use hospital_data;
DROP TABLE IF EXISTS hospital_is_post ;
DROP TABLE IF EXISTS hospital_is_compensation_request;
DROP TABLE IF EXISTS hospital_is_picture;
DROP TABLE IF EXISTS hospital_is_medical_record;
DROP TABLE IF EXISTS hospital_is_ticket;
DROP TABLE IF EXISTS hospital_is_medical_problem;
DROP TABLE IF EXISTS hospital_is_doctor;
DROP TABLE IF EXISTS hospital_is_compensated_operations;
DROP TABLE IF EXISTS hospital_is_insurance_worker;
DROP TABLE IF EXISTS hospital_is_admin;
DROP TABLE IF EXISTS hospital_is_patient;
DROP TABLE IF EXISTS hospital_is_user ;
DROP TABLE IF EXISTS users_profile;
DELETE FROM auth_user;
