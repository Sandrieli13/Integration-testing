/*Create Student Database*/

CREATE TABLE stuUsers(
	sName			VARCHAR(25) NOT NULL,
	sEmail			VARCHAR(50) NOT NULL,
	sTelephone		VARCHAR(11) NOT NULL,
	cunyEMPLD	INTEGER(9) NOT NULL,
	sYear			VARCHAR(10) NOT NULL,
	sMajor			VARCHAR(3) NOT NULL,
	sGPA			DECIMAL(6,2),
	sGradDate		VARCHAR(10) NOT NULL,
	sExplore		VARCHAR(3),
	sComments	VARCHAR(1000),
	PRIMARY KEY (cunyEMPLD)
	);
	
/*Create a Student Interests Table*/

CREATE TABLE stuInterest(
			cunyEMPLD INTEGER(9) NOT NULL,
			sInterests VARCHAR(50),
			FOREIGN KEY (cunyEMPLD) REFERENCES stuUsers (cunyEMPLD) ON DELETE CASCADE);

/*Create Student Skills Table*/

CREATE TABLE stuSkills(cunyEMPLD INTEGER(9) NOT NULL, 
						sSkills VARCHAR(50), 
						skillLevel VARCHAR(20), 
						FOREIGN KEY (cunyEMPLD) REFERENCES stuUsers(cunyEMPLD) ON DELETE CASCADE);
	
/*Create Student Certification table*/

CREATE TABLE stuCerts(cunyEMPLD	INTEGER(9) NOT NULL,
						sCerts VARCHAR(50), 
						certExp VARCHAR(10), 
						FOREIGN KEY (cunyEMPLD) REFERENCES stuUsers (cunyEMPLD) ON DELETE CASCADE);

	
/*Create fake students*/ 
	
INSERT INTO stuUsers VALUES("Alan Turing", "atur@stu.bmcc.cuny.edu", "1234567890", 12345678, "SOPHM", "CIS", "3.80", "12/16/23", "Y", "I want to be notified about postings!");
INSERT INTO stuUsers VALUES("Ada Lovelace", "adalove@stu.bmcc.cuny.edu", "2223334444", 44477789, "FRESH", "CS", 3.50, "05/30/2024", "N", NULL);
INSERT INTO stuUsers VALUES("Grace Hooper", "grace_hoop@stu.bmcc.cuny.edu", "4551112222", 99999888, "FRESH", "CIS", 3.65,  "12/16/2024", "N", "I want to learn more about career positions.");

/*Create fake interests for fake students */

INSERT INTO stuInterest VALUES(12345678, "SoftwareDev");
INSERT INTO stuInterest VALUES(12345678, "DataSci");
INSERT INTO stuInterest VALUES(12345678, "DBAdmin");
INSERT INTO stuInterest VALUES(44477789, "DataSci");
INSERT INTO stuInterest VALUES(44477789, "CloudSolu");
INSERT INTO stuInterest VALUES(99999888, "SoftwareDev");
INSERT INTO stuInterest VALUES(99999888, "DBAdmin");
INSERT INTO stuInterest VALUES(99999888, "AI/MachineL");

/*Create Fake Skills for fake students*/

INSERT INTO stuSkills VALUES(12345678, "C++", "Expert") ;
INSERT INTO stuSkills VALUES(12345678, "HTML", "Intermediate");
INSERT INTO stuSkills VALUES(12345678, "OOP", "Expert");
INSERT INTO stuSkills VALUES(44477789, "Java", "Novice");
INSERT INTO stuSkills VALUES(44477789, "Algorithms", "Novice");
INSERT INTO stuSkills VALUES(99999888, "WebDev", "Intermediate") ;
INSERT INTO stuSkills VALUES(99999888, "UI/UX", "Novice");

/*Create Fake certs for fake students*/

INSERT INTO stuCerts VALUES(12345678, "CompTIA A+", "12/20/2023");
INSERT INTO stuCerts VALUES(44477789, "Google Certified", "06/15/2024");

