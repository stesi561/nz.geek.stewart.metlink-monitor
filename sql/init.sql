CREATE TABLE IF NOT EXISTS service (
       id VARCHAR(10),
       name VARCHAR(255),
       PRIMARY KEY (id)
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS stops (
       sms VARCHAR (5),
       name VARCHAR (255),       
       lat DECIMAL(12,7),
       lng DECIMAL(12,7),
       farzone VARCHAR(2),   
       PRIMARY KEY (sms)
) ENGINE=INNODB;
 
CREATE TABLE IF NOT EXISTS servicelocations (
       id SERIAL PRIMARY KEY,
       RecordedAtTime DATETIME,
       VehicleRef INTEGER,
       ServiceID INTEGER,
       HasStarted BOOLEAN,
       DepartureTime DATETIME,
       OriginStopID INTEGER,
       DestinationStopID INTEGER,
       Direction TINYINT,
       Bearing SMALLINT,
       BehindSchedule BOOLEAN,
       VehicleFeature VARCHAR(255),
       DelaySeconds INTEGER,
       lat DECIMAL(12,7),
       lng DECIMAL(12,7)
) ENGINE=INNODB;
