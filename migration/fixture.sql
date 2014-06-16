-- Cogenda app inital data script --
INSERT INTO USERS(username, password, email, active) VALUES('tim.tang', 'secret', 'tang.jilong@gmail.com', 1);

INSERT INTO RESOURCES(name, type, vendor, url, status, upload_date, active) VALUES('jd.setup.v001.doc', '1', 'AliYun', 'http://asdfsafsadfsdafsdafsdafsdafsadfsdaf',  1, '2014-06-16 12:00:12', 1);
INSERT INTO RESOURCES(name, type, vendor, url, status, upload_date, active) VALUES('jd.setup.v001.doc', '1', 'AWS S3', 'http://123421342142142314234234132432423432', 1, '2014-06-16 12:00:12', 1);