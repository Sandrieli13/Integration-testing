/*Create Event Database */

CREATE TABLE eventsAttendance(
	cunyEMPLD		INTEGER(9) NOT NULL,
	eventName		VARCHAR(75) NOT NULL,
	eventDate			VARCHAR(20) NOT NULL,
	eventLocation		VARCHAR(75),
	eventTime			VARCHAR(20),
	FOREIGN KEY (cunyEMPLD) REFERENCES stuUsers(cunyEMPLD) ON DELETE CASCADE);
	
INSERT INTO eventsAttendance (cunyEMPLD, eventName, eventDate, eventLocation, eventTime)
VALUES	(12345678, 'International Admissions Information Session', 'July 20, 2023', 'Zoom', '12:30pm - 1:30pm');
INSERT INTO eventsAttendance (cunyEMPLD, eventName, eventDate, eventLocation, eventTime)
VALUES	(12345678, 'Admissions Information Session Special Guest: Year Up at BMCC', 'July 19, 2023', '70 Murray St., Room 203', '2:30pm - 1:30pm');
INSERT INTO eventsAttendance (cunyEMPLD, eventName, eventDate, eventLocation, eventTime)
VALUES	(44477789, 'Writing Center Workshop:Interpreting vs.Retelling', 'July 24, 2023', 'Zoom', '11:00am - 12:00pm');
INSERT INTO eventsAttendance (cunyEMPLD, eventName, eventDate, eventLocation, eventTime)
VALUES	(99999888, 'BMCC Spotlight Series', 'July 18, 2023', 'Zoom', '2:00pm - 4:00pm');