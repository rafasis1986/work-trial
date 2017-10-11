SET SESSION sql_mode='ALLOW_INVALID_DATES';

USE test;

TRUNCATE samples;

LOAD DATA INFILE '/Users/worktrial/git/work-trial/data/initial/samples.csv' 
INTO TABLE samples
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

TRUNCATE Lab_Sample_Loading;

LOAD DATA INFILE '/Users/worktrial/git/work-trial/data/initial/Lab_Sample_Loading.csv' 
INTO TABLE Lab_Sample_Loading
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

TRUNCATE Lab_Pipeline_Tracking;

LOAD DATA INFILE '/Users/worktrial/git/work-trial/data/initial/Lab_Pipeline_Tracking.csv' 
INTO TABLE Lab_Pipeline_Tracking
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

TRUNCATE clinical_result_counts;

LOAD DATA INFILE '/Users/worktrial/git/work-trial/data/initial/clinical_result_counts.csv' 
INTO TABLE clinical_result_counts
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

TRUNCATE results_diversity;

LOAD DATA INFILE '/Users/worktrial/git/work-trial/data/initial/results_diversity.csv' 
INTO TABLE results_diversity
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
