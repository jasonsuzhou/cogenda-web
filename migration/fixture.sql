-- Cogenda app inital data script --
DELETE FROM USERS;
DELETE FROM RESOURCES;

INSERT INTO USERS(username, password, company, email, mobile, role, resource, notes, active, created_date, updated_date) VALUES('cogenda', '94cd03f50e150548a0d81f9abda83ae0', 'Cogenda INC.', 'support@cogenda.com', '1234567890', '1', '', 'This is Admin', 1, DATETIME('now'), DATETIME('now'));

INSERT INTO RESOURCES(name, type, vendor, url, status, uploaded_date, active) VALUES('jd.setup.v001.doc', '1', 'AliYun', 'http://asdfsafsadfsdafsdafsdafsdafsadfsdaf',  1, DATETIME('now'), 1);
INSERT INTO RESOURCES(name, type, vendor, url, status, uploaded_date, active) VALUES('jd.setup.v002.doc', '1', 'AWS S3', 'http://123421342142142314234234132432423432', 1, DATETIME('now'), 1);
