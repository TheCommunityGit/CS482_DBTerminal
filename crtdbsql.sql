
CREATE TABLE Video (
VideoCode int,
videoLength int,
primary key(VideoCode)
);

CREATE TABLE Model (
ModelNo char(10),
width numeric (6,2),
height numeric (6,2),
weight numeric (6,2),
depth numeric (6,2),
screenSize numeric (6,2),
primary key (modelNo)
);

CREATE TABLE Site (
siteCode int,
type varchar(16),
address varchar(100),
phone varchar(16),
primary key (siteCode),
CHECK (type IN ('bar', 'restaurant'))
);

CREATE TABLE DigitalDisplay (
serialNo char(10),
schedulerSystem char(10),
modelNo char(10),
primary key (SerialNo),
foreign key (modelNo) references Model(modelNo) on delete cascade on update cascade,
CHECK (schedulerSystem IN ('Random', 'Smart','Virtue'))
);

CREATE TABLE Client (
clientId int,
name varchar (40),
phone varchar (16),
address varchar (100),
primary key (clientId)
);

CREATE TABLE TechnicalSupport (
empId int,
name varchar (40),
gender char (1),
primary key (empId)
);

CREATE TABLE Administrator (
empId int,
name varchar (40),
gender char (1),
primary key(empId)
);

CREATE TABLE Salesman (
empId int,
name varchar (40),
gender char (1),
primary key(empId)
);

CREATE TABLE AirtimePackage (
packageId int,
class varchar (16),
startDate date,
lastDate date,
frequency int,
videoCode int,
primary key(packageId),
CHECK (class IN ('economy', 'whole day','golden hours'))
);

CREATE TABLE AdmWorkHours (
empId int,
day date,
hours numeric (4,2),
primary key(empId, day),
foreign key (empId) references Administrator(empId) on delete cascade on update cascade
);

CREATE TABLE Broadcasts (
videoCode int,
siteCode int,
primary key (videoCode,siteCode),
foreign key (videoCode) references Video(videoCode)on delete cascade
on update cascade,
foreign key (siteCode) references Site(siteCode)on delete cascade
on update cascade
);

CREATE TABLE Administers (
empId int,
siteCode int,
foreign key(empId) references Administrator(empId) on delete cascade
on update cascade,
foreign key(siteCode) references Site(siteCode) on delete cascade
on update cascade,
primary key (empId, siteCode)
);

CREATE TABLE Specializes (
empId int,
modelNo char(10),
primary key (empId,modelNo),
foreign key (empId) references TechnicalSupport(empId) on delete cascade
on update cascade,
foreign key (modelNo) references Model(modelNo) on delete cascade
on update cascade
);

CREATE TABLE Purchases (
clientId int,
empId int,
packageId int,
commissionRate numeric (4,2),
primary key(clientId,empId, packageId),
Foreign key (clientId) references Client (clientId)on delete cascade
on update cascade,
Foreign key (empId) references Salesman (empId)on delete cascade
on update cascade,
Foreign key (packageId) references AirtimePackage (packageId)on delete cascade
on update cascade
);

CREATE TABLE Locates (
serialNo char (10),
siteCode int,
primary key (serialNo, siteCode),
Foreign key (serialNo) references DigitalDisplay (serialNo)on delete cascade
on update cascade,
Foreign key (siteCode) references Site (siteCode)on delete cascade
on update cascade
);
