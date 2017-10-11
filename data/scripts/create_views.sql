USE `test`;
CREATE 
     OR REPLACE ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `samples_id_vie` AS
    SELECT 
        `samples`.`id` AS `SAMPLE_ID`,
        `lab_sample_loading`.`id` AS `SSR_ID`,
        `lab_sample_loading`.`PRID` AS `PRID`,
        `lab_pipeline_tracking`.`seqRunId` AS `SEQRUN_ID`
    FROM
        ((`lab_pipeline_tracking`
        JOIN `lab_sample_loading` ON ((`lab_sample_loading`.`PRID` = `lab_pipeline_tracking`.`PRID`)))
        JOIN `samples` ON ((`samples`.`vial_barcode` = CONVERT( `lab_sample_loading`.`tubeId` USING UTF8))))
    WHERE
        (`lab_pipeline_tracking`.`seqRunId` = 0);
