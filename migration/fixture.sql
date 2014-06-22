-- Cogenda app inital data script --
INSERT INTO USERS(username, password, company, email, mobile, role, resource, notes, active, created_date, updated_date) VALUES('Tim', '123', 'Arctic INC.', 'tang.jilong@gmail.com', '1234567890', '1', '', 'This is notes~', 1, DATETIME('now'), DATETIME('now'));

INSERT INTO RESOURCES(name, type, vendor, url, status, uploaded_date, active) VALUES('jd.setup.v001.doc', '1', 'AliYun', 'http://asdfsafsadfsdafsdafsdafsdafsadfsdaf',  1, DATETIME('now'), 1);
INSERT INTO RESOURCES(name, type, vendor, url, status, uploaded_date, active) VALUES('jd.setup.v002.doc', '1', 'AWS S3', 'http://123421342142142314234234132432423432', 1, DATETIME('now'), 1);
