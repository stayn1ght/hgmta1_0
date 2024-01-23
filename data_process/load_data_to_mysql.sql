LOAD DATA INFILE 'D:/07-data/HGMTA/01_disease_info.csv'
INTO TABLE disease_info
COLUMNS TERMINATED BY ','
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(short_name, phenotype_name, mesh_id);

LOAD DATA INFILE 'D:/07-data/HGMTA/01_project.csv'
INTO TABLE project
COLUMNS TERMINATED BY ','
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(short_name, amplicon_16s, amplicon_ITS, WGS);

LOAD DATA INFILE 'D:/07-data/HGMTA/01_run.csv'
INTO TABLE run
COLUMNS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(short_name,amplicon_16s,amplicon_ITS,WGS, Total);

LOAD DATA INFILE 'D:/07-data/HGMTA/02_DA_results.csv'
INTO TABLE da_results
COLUMNS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(da_id,batch,taxa,kingdom,taxon_level,w_statistic,p_value,lfc,assay_type,case_name,control_name,num_case,num_control,taxa_short_name,
@var1)
SET display = (@var1 = 'TRUE');

LOAD DATA INFILE 'F:/07-data/da_results_processed.csv'
INTO TABLE da_results
COLUMNS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id,da_id,batch,taxa,kingdom,taxon_level,w_statistic,p_value,lfc,assay_type,case_name,control_name,num_case,num_control,taxa_short_name,
display,nrproj,conflict);

LOAD DATA INFILE 'D:/07-data/HGMTA/03_feat_table_demo.csv'
INTO TABLE feature_table
COLUMNS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(taxa,run_id,abundance);

LOAD DATA INFILE 'D:/07-data/HGMTA/project_all.csv'
INTO TABLE project_all
COLUMNS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(project_id,assay_type,project_title,project_description,public_accession,journal,handler);

LOAD DATA INFILE 'D:/07-data/HGMTA/project_summary.csv'
INTO TABLE project_summary
COLUMNS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(project_id,batch,summary,associated_project);

LOAD DATA INFILE 'D:/07-data/HGMTA/sample_meta_all_QC.csv'
INTO TABLE sample_meta_curated
COLUMNS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(project_id,run_id ,sample_name,assay_type ,sequencing_method ,phenotype_name ,
sample_description ,phenotype_id ,country ,geographic_location , longitude ,lattitude ,
age ,sex ,bmi ,antibiotic_use ,antibiotic_name ,bodysite ,batch ,batch2,QC_state,QC_Bacteria,QC_Bacteria_gg,QC_Fungi
);

LOAD DATA INFILE 'F:/07-data/08_search_bar.csv'
INTO TABLE searchable
COLUMNS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(type, keywords, accession);

LOAD DATA INFILE 'F:/07-data/06_taxa_6748_final.csv'
INTO TABLE taxa2ncbi
COLUMNS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(hgmt_micro_id, level, taxa, short_name, taxid, scientific_name);

LOAD DATA INFILE 'F:/07-data/03_feat_table_B.csv'
INTO TABLE feature_table_bac
COLUMNS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(taxa, run_id, abundance);

LOAD DATA INFILE 'F:/07-data/03_feat_table_F.csv'
INTO TABLE feature_table_fungi
COLUMNS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(taxa, run_id, abundance);