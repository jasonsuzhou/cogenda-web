-- Cogenda app inital data script --
DELETE FROM USERS;
DELETE FROM RESOURCES;

INSERT INTO USERS(username, password, company, email, mobile, role, resource, notes, active, created_date, updated_date) VALUES('cogenda', '94cd03f50e150548a0d81f9abda83ae0', 'Cogenda INC.', 'support@cogenda.com', '1234567890', '3', '', 'This is Admin', 1, DATETIME('now'), DATETIME('now'));

INSERT INTO RESOURCES(name, type, vendor, url, status, uploaded_date, active) VALUES('jd.setup.v001.doc', '1', 'AliYun', 'http://cogenda-media.oss-cn-hangzhou.aliyuncs.com/media/123.png?Expires=1403359250&OSSAccessKeyId=DvSB6U5JdgjPj1Zr&Signature=vdtP0ldMD0yCskxmGcPxuF0oPuM%3D',  1, DATETIME('now'), 1);
INSERT INTO RESOURCES(name, type, vendor, url, status, uploaded_date, active) VALUES('jd.setup.v002.doc', '1', 'AWS S3', 'http://cogenda-media.oss-cn-hangzhou.aliyuncs.com/media/123.png?Expires=1403359250&OSSAccessKeyId=DvSB6U5JdgjPj1Zr&Signature=vdtP0ldMD0yCskxmGcPxuF0oPuM%3D', 1, DATETIME('now'), 1);
