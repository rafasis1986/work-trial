CREATE DATABASE IF NOT EXISTS test;

USE test;

DROP TABLE IF EXISTS `samples`;
DROP TABLE IF EXISTS `Lab_Sample_Loading`;
DROP TABLE IF EXISTS `Lab_Pipeline_Tracking`;
DROP TABLE IF EXISTS `clinical_result_counts`;
DROP TABLE IF EXISTS `results_diversity`;

CREATE   TABLE   `samples`   (
    `id`   bigint(20)   NOT   NULL   AUTO_INCREMENT,                                         
    `vial_barcode`   varchar(32)   DEFAULT   NULL,     `kit_barcode`   varchar(32)   DEFAULT   NULL,
    `study_id`   int(11)   DEFAULT   NULL,
    `user`   bigint(20)   DEFAULT   NULL,
    `experiment`   bigint(20)   DEFAULT   NULL,
    `assigned_kit`   timestamp   NULL   DEFAULT   NULL,
    `kit`   bigint(20)   DEFAULT   NULL,
    `assigned_vial`   timestamp   NULL   DEFAULT   NULL,
    `created`   timestamp   NULL   DEFAULT   CURRENT_TIMESTAMP,
    `processed`   timestamp   NULL   DEFAULT   NULL,
    `samplingTime`   timestamp   NULL   DEFAULT   NULL,
    `samplingTimeText`   varchar(255)   DEFAULT   NULL,
    `received`   timestamp   NULL   DEFAULT   NULL,
    `analyzed`   timestamp   NULL   DEFAULT   NULL,
    `query_exclude`   int(11)   NOT   NULL   DEFAULT   '0',
    `collected`   timestamp   NULL   DEFAULT   NULL,
    `sequencing_revision`   bigint(20)   DEFAULT   NULL,
    `discount_code`   varchar(255)   DEFAULT   NULL,
    `order_email`   varchar(255)   DEFAULT   NULL,
    `order_date`   timestamp   NULL   DEFAULT   NULL,
    `human_barcode1`   varchar(32)   DEFAULT   NULL,
    `human_barcode2`   varchar(32)   DEFAULT   NULL,
    PRIMARY   KEY   (`id`),
    UNIQUE   KEY   `human_barcode1`   (`human_barcode1`),
    KEY   `experiment`   (`experiment`),
      KEY   `assigned_kit`   (`assigned_kit`),
      KEY   `kit`   (`kit`),
      KEY   `query_exclude`   (`query_exclude`),
      KEY   `kit_barcode`   (`kit_barcode`),
      KEY   `sequencing_revision`   (`sequencing_revision`), 
      KEY   `vial_barcode`   (`vial_barcode`)
)   ENGINE=InnoDB   DEFAULT   CHARSET=utf8;

CREATE   TABLE   `Lab_Sample_Loading`   (
    `id`   int(10)   NOT   NULL   AUTO_INCREMENT,                           
    `tubeId`   varchar(255)   DEFAULT   '',
    `PRID`   varchar(255)   NOT   NULL,
    `Extraction_Rack_Number`   varchar(255)   NOT   NULL,
    `Extraction_Rack_Loaction`   varchar(255)   NOT   NULL,
    `Extraction_Rack_Scan_Time`   varchar(255)   DEFAULT   '',
    `pipeline_tracking_record`   bigint(20)   DEFAULT   NULL,
    `originFileName`   varchar(128)   DEFAULT   '',
    `sample`   bigint(20)   DEFAULT   NULL,
    `taxondata_loaded`   timestamp   NULL   DEFAULT   NULL,
    `created`   timestamp   NULL   DEFAULT   CURRENT_TIMESTAMP,
    `pipeline_rev`   int(11)   NOT   NULL   DEFAULT   '1',
    `latestRev2`   int(11)   NOT   NULL   DEFAULT   '0',
    `report_status`   varchar(60)   DEFAULT   NULL,
    `clinical`   tinyint(1)   DEFAULT   NULL,
    `report_comments`   varchar(255)   DEFAULT   NULL,
    PRIMARY   KEY   (`id`),
    KEY   `tubeId`   (`tubeId`),
    KEY   `latestRev2`   (`latestRev2`),
    KEY   `pipeline_rev`   (`pipeline_rev`),
    KEY   `PRID`   (`PRID`)
)   ENGINE=InnoDB   DEFAULT   CHARSET=latin1;


CREATE   TABLE   `Lab_Pipeline_Tracking`   (
    `PRID`   varchar(255)   NOT   NULL,                
    `StartTime`   varchar(255)   NOT   NULL,
    `primerPlateId`   varchar(255)   NOT   NULL,
    `PCRSetupStartTime`   varchar(255)   NOT   NULL,
    `PCRPlateBarcode`   varchar(255)   NOT   NULL,
    `ExtractStorageTime`   varchar(255)   NOT   NULL,
    `ThermocycleStartTime`   varchar(255)   NOT   NULL,
    `PCRProductTubeId`   varchar(255)   NOT   NULL,
    `PCRProductScanTime`   varchar(255)   NOT   NULL,
    `qBitData`   longtext   NOT   NULL,
    `DCCPlateStorageTime`   varchar(255)   NOT   NULL,
    `labChippedTubeId`   varchar(255)   NOT   NULL,
    `labChippedProductScanTime`   varchar(255)   NOT   NULL,
    `PCRProductTubeStorageTime`   varchar(255)   NOT   NULL,     
    `FinalLibraryAliquatTime`   varchar(255)   NOT   NULL,
    `labChippedTubeStorageTime`   varchar(255)   NOT   NULL,
    `id`   bigint(20)   NOT   NULL   AUTO_INCREMENT,
    `seqRunName`   varchar(255)   NOT   NULL,
    `seqRunId`   bigint(20)   NOT   NULL,
    `active_at_robot`   int(11)   DEFAULT   NULL,
    PRIMARY   KEY   (`id`),
      KEY   `PRID`   (`PRID`)
)   ENGINE=InnoDB   DEFAULT   CHARSET=latin1;

CREATE   TABLE   `clinical_result_counts`   (
    `id`   int(11)   NOT   NULL   AUTO_INCREMENT, 
    `taxon`   int(11)   NOT   NULL,
    `count`   double   NOT   NULL,
    `percent_count`   float   NOT   NULL,
    `ssr`   int(11)   NOT   NULL,
    `uploadTime`   timestamp   NULL   DEFAULT   CURRENT_TIMESTAMP,
    `soft_version`   varchar(255)   DEFAULT   '0.0.1',
    `total_reads`   int(11)   DEFAULT   NULL,
    PRIMARY   KEY   (`id`),
    KEY   `function`   (`taxon`),
    KEY   `ssr`   (`ssr`),
    KEY   `percent_count`   (`percent_count`)
)   ENGINE=InnoDB   DEFAULT   CHARSET=latin1;

CREATE   TABLE   `results_diversity`   (
    `id`   bigint(20)   NOT   NULL   AUTO_INCREMENT,            
    `ssr`   bigint(20)   DEFAULT   NULL,
    `type`   varchar(255)   DEFAULT   NULL,
    `value`   float   DEFAULT   NULL,
    `created`   timestamp   NOT   NULL   DEFAULT   CURRENT_TIMESTAMP,
    PRIMARY   KEY   (`id`),
    KEY   `ssr`   (`ssr`),
    KEY   `type`   (`type`),
    KEY   `value`   (`value`),
    KEY   `created`   (`created`)
)   ENGINE=InnoDB   DEFAULT   CHARSET=latin1;

CREATE TABLE `pending_ssr` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sample` bigint(20) NOT NULL,
  `tubeid` varchar(32) NOT NULL,
  `prid` varchar(255) NOT NULL,
  `days_elapsed` varchar(45) DEFAULT NULL,
  `created_ts` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `ssr` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create index pending_prid_index on pending_ssr(prid) using HASH;
create index pending_ssr_index on pending_ssr(ssr) using HASH;

CREATE TABLE `aborted_ssr` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sample` bigint(20) NOT NULL,
  `tubeid` varchar(32) NOT NULL,
  `prid` varchar(255) NOT NULL,
  `days_elapsed` varchar(45) DEFAULT NULL,
  `created_ts` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `ssr` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create index aborted_prid_index on aborted_ssr(prid) using HASH;
create index aborted_ssr_index on aborted_ssr(ssr) using HASH;

CREATE TABLE `exclude_samples` (
  `id` bigint(20) NOT NULL,
  `created_ts` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE VIEW samples_view AS
    SELECT 
        s.id AS sample,
        lsl.id AS ssr,
        lsl.PRID AS prid,
        lpt.seqRunId AS seqrun
    FROM
        lab_pipeline_tracking as lpt
        INNER JOIN lab_sample_loading as lsl ON lsl.PRID = lpt.PRID
        INNER JOIN samples as s ON s.vial_barcode = lsl.tubeId
    WHERE
        lpt.seqRunId = 0
    ORDER BY 
        sample,
        prid DESC;

SET SESSION sql_mode='ALLOW_INVALID_DATES';

USE test;

TRUNCATE samples;

LOAD DATA INFILE '/data/samples.csv' 
INTO TABLE samples
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

TRUNCATE Lab_Sample_Loading;

LOAD DATA INFILE '/data/Lab_Sample_Loading.csv' 
INTO TABLE Lab_Sample_Loading
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

TRUNCATE Lab_Pipeline_Tracking;

LOAD DATA INFILE '/data/Lab_Pipeline_Tracking.csv' 
INTO TABLE Lab_Pipeline_Tracking
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

TRUNCATE clinical_result_counts;

LOAD DATA INFILE '/data/clinical_result_counts.csv' 
INTO TABLE clinical_result_counts
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

TRUNCATE results_diversity;

LOAD DATA INFILE '/data/results_diversity.csv' 
INTO TABLE results_diversity
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
