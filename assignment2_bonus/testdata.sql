CREATE DATABASE assignment_database;

CREATE TABLE DiseaseType (
    id INT NOT NULL,
    description VARCHAR(140) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Country (
    cname VARCHAR(50) NOT NULL,
    population BIGINT NOT NULL,
    PRIMARY KEY (cname)
);

CREATE TABLE Disease (
    disease_code VARCHAR(50),
    pathogen VARCHAR(20) NOT NULL,
    description VARCHAR(140) NOT NULL,
    id INT,
    PRIMARY KEY (disease_code),
    FOREIGN KEY (id)
        REFERENCES DiseaseType (id)
);

CREATE TABLE Discover (
    cname VARCHAR(50),
    disease_code VARCHAR(50),
    first_enc_date DATE NOT NULL,
    PRIMARY KEY (disease_code , cname),
    FOREIGN KEY (disease_code)
        REFERENCES Disease (disease_code),
    FOREIGN KEY (cname)
        REFERENCES Country (cname)
);

CREATE TABLE Users (
    email VARCHAR(60),
    name VARCHAR(30) NOT NULL,
    surname VARCHAR(40) NOT NULL,
    salary INT NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE,
    cname VARCHAR(50),
    PRIMARY KEY (email),
    FOREIGN KEY (cname)
        REFERENCES Country (cname)
);

CREATE TABLE PublicServant (
    email VARCHAR(60),
    department VARCHAR(50) NOT NULL,
    PRIMARY KEY (email),
    FOREIGN KEY (email)
        REFERENCES Users (email)
);

CREATE TABLE Doctor (
    email VARCHAR(60),
    degree VARCHAR(20) NOT NULL,
    PRIMARY KEY (email),
    FOREIGN KEY (email)
        REFERENCES Users (email)
);

CREATE TABLE Specialize (
    id INT,
    email VARCHAR(60),
    PRIMARY KEY (id , email),
    FOREIGN KEY (id)
        REFERENCES DiseaseType (id),
    FOREIGN KEY (email)
        REFERENCES Doctor (email)
);

CREATE TABLE Record (
    email VARCHAR(60),
    cname VARCHAR(50),
    disease_code VARCHAR(50),
    total_deaths INT NOT NULL,
    total_patients INT NOT NULL,
    PRIMARY KEY (disease_code , cname , email),
    FOREIGN KEY (disease_code)
        REFERENCES Disease (disease_code),
    FOREIGN KEY (cname)
        REFERENCES Country (cname),
    FOREIGN KEY (email)
        REFERENCES PublicServant (email)
);


INSERT INTO 
	DiseaseType(id, description)
VALUES
	(1,'infectious diseases'),
    (2,'virology'),
	(3,'cardiovascular'),
    (4,'respiratory'),
    (5,'locomotor'),
    (6,'endocrine'),
    (7,'mental'),
    (8,'digestive system'),
    (9,'oncogenic'),
    (10,'dermatological'),
    (11,'autoimmune');
    
INSERT INTO 
	Country(cname, population)
VALUES
	('Australia',25499884),
    ('China', 1493323776),
    ('India',1380004385),
    ('United States',331002651),
    ('France',65273511),
	('Indonesia',273523615),
    ('Russia',145834462),
    ('Japan', 126476461),
    ('Germany',83783942),
    ('Turkey', 84339067),
    ('Kazakhstan', 18776707);
    
INSERT INTO 
	Disease(disease_code, pathogen, description, id)
VALUES
	('covid-19','virus','coronavirus',1),
	('myoc','virus','myocarditis',2),
    ('pneu','bacteria','pneumonia',3),
    ('arth','bacteria','arthritis',4),
    ('diab','bacteria','diabetes',5),
    ('chrk','bacteria','chronic kidney',5),
    ('aut','virus','autism',6),
    ('ibs','bacteria','IBS',7),
    ('hep','virus','hepatitis',8),
    ('trp','fungi','trichophytosis',9),
    ('ads','bacteria','addison',10),
    ('cpox','virus','chickenpox',11);
    
INSERT INTO 
	Discover(cname, disease_code, first_enc_date)
VALUES
    ('Indonesia','myoc','1837-11-20'),
	('China','covid-19','2019-02-01'),
    ('France','pneu','1881-01-10'),
    ('Germany','arth','1965-01-09'),
    ('Australia','diab','1889-04-01'),
    ('Australia','chrk','1995-05-01'),
    ('United States','aut','1971-06-12'),
    ('India','ibs','1945-07-01'),
    ('Russia','hep','2003-08-11'),
    ('Japan','trp','2000-01-01'),
    ('Japan','ads','1917-02-01'),
    ('China','cpox','1897-03-01');

INSERT INTO 
	Users(email, name, surname, salary, phone, cname)
VALUES
	('sofi.lee@gmail.com','Sofi','Lee', 130000, '0850188', 'United States'),
    ('denis.sand@gmail.com','Denis','Sand', 150000, '0850288', 'Australia'),
    ('alex.turner@gmail.com','Alex','Turner', 130000, '0850588', 'Indonesia'),
    ('bekzhan.ozdemir@gmail.com','Bekzhan','Ozdemir', 200000, '0850688', 'Turkey'),
    ('gulnaz.assylbek@gmail.com','Gulnaz','Assylbek', 150000, '0850788', 'Kazakhstan'),
    ('lucas.turner@gmail.com','Lucas','Turner', 130000, '0850888', 'France'),
    ('guli.sharma@gmail.com','Guli','Sharma', 100000, '0850988', 'India'),
    ('haru.tanaka@gmail.com','Haru','Tanaka', 150000, '0851088', 'Japan'),
    ('bektemis.kudaibergen@gmail.com','Bektemis','Kudaibergen', 110000, '0851188', 'Kazakhstan'),
    ('sky.becker@gmail.com','Sky','Becker', 100000, '0851288', 'Germany'),
    ('noah.pavlov@gmail.com','Noah','Pavlov', 155000, '0851388', 'Russia'),
    ('alibek.gani@gmail.com','Alibek','Gani', 100000, '0851488', 'Kazakhstan'),
    ('emma.shevsova@gmail.com','Emma','Shevsova', 200000, '0851588', 'Russia'),
    ('hannah.bahng@gmail.com','Hannah','Bahng', 180000, '0851688', 'Australia'), 
    ('tom.miller@gmail.com','Tom','Miller', 110000, '0850388', 'United States'),
    ('olivia.shen@gmail.com','Olivia','Shen', 190000, '0850488', 'China'),
    ('nurgul.bolat@gmail.com','Nurgul','Bolat', 110000, '0851788', 'Kazakhstan'),
    ('evelyn.park@gmail.com','Evelyn','Park', 300000, '0851888', 'United States'),
    ('dana.cetin@gmail.com','Dana','Cetin', 235000, '0851988', 'Turkey'),     
	('christopher.aubert@gmail.com','Christopher','Aubert', 155000, '0852088', 'France'); 
    
INSERT INTO 
	PublicServant(email, department)
VALUES
	('sofi.lee@gmail.com','Dept1'),
    ('denis.sand@gmail.com', 'Dept1'),
    ('alex.turner@gmail.com','Dept1'),
    ('bekzhan.ozdemir@gmail.com','Dept3'),
    ('gulnaz.assylbek@gmail.com','Dept3'),
    ('lucas.turner@gmail.com','Dept2'),
    ('guli.sharma@gmail.com','Dept2'),
    ('haru.tanaka@gmail.com','Dept3'),
    ('bektemis.kudaibergen@gmail.com','Dept4'),
    ('sky.becker@gmail.com','Dept4');

INSERT INTO 
	Doctor(email, degree)
VALUES
	('olivia.shen@gmail.com','Bachelor'),
	('noah.pavlov@gmail.com','Bachelor'),   
    ('hannah.bahng@gmail.com','Master'), 
    ('tom.miller@gmail.com','Master'),
    ('alibek.gani@gmail.com','Bachelor'),
    ('emma.shevsova@gmail.com','Master'),
	('nurgul.bolat@gmail.com','Master'),
    ('evelyn.park@gmail.com','Bachelor'),
    ('dana.cetin@gmail.com','Doctorate'),     
	('christopher.aubert@gmail.com','Bachelor'); 
    
INSERT INTO 
	Specialize(id, email)
VALUES
	(4,'olivia.shen@gmail.com'),
    (7,'olivia.shen@gmail.com'),
    (8,'olivia.shen@gmail.com'),
	(2,'noah.pavlov@gmail.com'),   
    (3,'noah.pavlov@gmail.com'), 
    (4,'noah.pavlov@gmail.com'), 
    (5,'noah.pavlov@gmail.com'), 
    (1,'hannah.bahng@gmail.com'), 
    (1,'tom.miller@gmail.com'),
    (2,'alibek.gani@gmail.com'),
    (6,'alibek.gani@gmail.com'),
    (9,'emma.shevsova@gmail.com'),
	(2,'nurgul.bolat@gmail.com'),
	(3,'nurgul.bolat@gmail.com'),
	(7,'nurgul.bolat@gmail.com'),
    (2,'evelyn.park@gmail.com'),
    (10,'dana.cetin@gmail.com'),     
	(11,'christopher.aubert@gmail.com'), 
    (2,'christopher.aubert@gmail.com'); 
    
INSERT INTO 
	Record(email, cname, disease_code, total_deaths, total_patients)
VALUES
	('sofi.lee@gmail.com','Germany', 'ibs', 49, 3110),
	('sofi.lee@gmail.com','India', 'hep', 49, 3110),
	('sofi.lee@gmail.com','Australia', 'trp', 49, 3110),
    ('denis.sand@gmail.com', 'China', 'covid-19', 47890, 505678),
	('denis.sand@gmail.com', 'China', 'pneu', 12670, 55678),
    ('alex.turner@gmail.com','France', 'covid-19', 7892, 56800),
    ('bekzhan.ozdemir@gmail.com','Turkey', 'covid-19', 4562, 230567),
	('bekzhan.ozdemir@gmail.com','France', 'covid-19', 44562, 2305670),
    ('gulnaz.assylbek@gmail.com','Kazakhstan', 'covid-19', 32678, 580560),
    ('lucas.turner@gmail.com','Germany', 'pneu', 132000, 757200),
	('lucas.turner@gmail.com','China', 'covid-19', 562000, 2708000),
	('lucas.turner@gmail.com','Indonesia', 'covid-19', 13800, 78000),
	('lucas.turner@gmail.com','Germany', 'ads', 130, 19402),
    ('guli.sharma@gmail.com','India', 'arth', 35, 20000),
    ('haru.tanaka@gmail.com','United States', 'covid-19', 489902, 3459064),
    ('bektemis.kudaibergen@gmail.com','Japan', 'diab', 4500, 100003),
    ('sky.becker@gmail.com','Indonesia', 'cpox', 34890, 211083),
	('sofi.lee@gmail.com','Germany', 'myoc', 456, 65867),
    ('denis.sand@gmail.com', 'France', 'chrk', 769, 76819),
    ('alex.turner@gmail.com','Turkey', 'aut', 6, 1769),
    ('bekzhan.ozdemir@gmail.com','India', 'covid-19', 745678, 35787970),
    ('gulnaz.assylbek@gmail.com','Indonesia', 'covid-19', 57790, 400900),
    ('gulnaz.assylbek@gmail.com','Russia', 'covid-19', 145678, 934678),
    ('gulnaz.assylbek@gmail.com','Japan', 'covid-19', 110003, 877252);

ALTER TABLE Disease DROP CONSTRAINT disease_id_fkey;
ALTER TABLE DiseaseType ADD CONSTRAINT disease_id_fkey FOREIGN KEY (id) REFERENCES DiseaseType (id) ON DELETE CASCADE;
ALTER TABLE Discover DROP CONSTRAINT discover_disease_code_fkey;
ALTER TABLE Discover ADD CONSTRAINT discover_disease_code_fkey FOREIGN KEY (disease_code) REFERENCES Disease (disease_code) ON DELETE CASCADE;
ALTER TABLE Discover DROP CONSTRAINT discover_cname_fkey;
ALTER TABLE Discover ADD CONSTRAINT discover_cname_fkey FOREIGN KEY (cname) REFERENCES Country (cname) ON DELETE CASCADE;
ALTER TABLE Record DROP CONSTRAINT record_cname_fkey;
ALTER TABLE Record ADD CONSTRAINT record_cname_fkey FOREIGN KEY (cname) REFERENCES Country (cname) ON DELETE CASCADE;
ALTER TABLE Users DROP CONSTRAINT users_cname_fkey;
ALTER TABLE Users ADD CONSTRAINT users_cname_fkey FOREIGN KEY (cname) REFERENCES Country (cname) ON DELETE CASCADE;
ALTER TABLE Doctor DROP CONSTRAINT doctor_email_fkey ;
ALTER TABLE Doctor ADD CONSTRAINT doctor_email_fkey FOREIGN KEY (email) REFERENCES Users (email) ON DELETE CASCADE ;
ALTER TABLE PublicServant DROP CONSTRAINT publicservant_email_fkey ;
ALTER TABLE PublicServant ADD CONSTRAINT publicservant_email_fkey FOREIGN KEY (email) REFERENCES Users (email) ON DELETE CASCADE ;
ALTER TABLE Specialize DROP CONSTRAINT specialize_email_fkey ;
ALTER TABLE Specialize ADD CONSTRAINT specialize_email_fkey FOREIGN KEY (email) REFERENCES Users (email) ON DELETE CASCADE ;
ALTER TABLE Record DROP CONSTRAINT record_email_fkey ;
ALTER TABLE Record ADD CONSTRAINT record_email_fkey FOREIGN KEY (email) REFERENCES Users (email) ON DELETE CASCADE ;
ALTER TABLE Specialize DROP CONSTRAINT specialize_id_fkey ;
ALTER TABLE Specialize ADD CONSTRAINT specialize_id_fkey FOREIGN KEY (id) REFERENCES DiseaseType (id) ON DELETE CASCADE;
ALTER TABLE Record DROP CONSTRAINT record_disease_code_fkey ;
ALTER TABLE Record ADD CONSTRAINT record_disease_code_fkey FOREIGN KEY (disease_code) REFERENCES Disease (disease_code) ON DELETE CASCADE ;
