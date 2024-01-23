from django.db import models

# Create your models here.

class DiseaseInfo(models.Model):
    short_name = models.CharField(max_length=100, null=False)
    phenotype_name = models.CharField(max_length=100, null=False)
    mesh_id = models.CharField(max_length=100, primary_key=True)

    class Meta:
        db_table = "disease_info"

class Project(models.Model):
    short_name = models.CharField(max_length=100, null=False)
    amplicon_16s = models.IntegerField(null=False)
    amplicon_ITS = models.IntegerField(null=False)
    WGS = models.IntegerField(null=False)
        
    class Meta:
        db_table = "project"

class Run(models.Model):
    short_name = models.CharField(max_length=100, null=False)
    amplicon_16s = models.IntegerField(null=False)
    amplicon_ITS = models.IntegerField(null=False)
    WGS = models.IntegerField(null=False)
    Total = models.IntegerField(null=False)

    class Meta:
        db_table = "run"

class DAResults(models.Model):
    da_id = models.CharField(max_length=100, null=False)
    batch = models.CharField(max_length=100, null=False)
    taxa = models.CharField(max_length=500, null=False)
    kingdom = models.CharField(max_length=100, null=False)
    taxon_level = models.CharField(max_length=100, null=False)
    w_statistic = models.FloatField(null=False)
    p_value = models.FloatField(null=False)
    lfc = models.FloatField(null=False)
    assay_type = models.CharField(max_length=100, null=False)
    case_name = models.CharField(max_length=100, null=False)
    control_name = models.CharField(max_length=100, null=False)
    num_case = models.IntegerField(null=False)
    num_control = models.IntegerField(null=False)
    taxa_short_name = models.CharField(max_length=100, null=False)
    display = models.BooleanField(null=False)
    nrproj = models.IntegerField(null=False)
    conflict = models.IntegerField(null=False)

    class Meta:
        db_table = "da_results"

class ProjectAll(models.Model):
    project_id = models.CharField(max_length=100, null=False)
    assay_type = models.CharField(max_length=100, null=False)
    project_title = models.CharField(max_length=200, null=False)
    project_description = models.CharField(max_length=3000, null=False)
    public_accession = models.CharField(max_length=100, null=True)
    journal = models.CharField(max_length=100, null=True)
    handler = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "project_all"

class ProjectSummary(models.Model):
    project_id = models.CharField(max_length=100, null=False)
    batch = models.CharField(max_length=100, null=False)
    summary = models.CharField(max_length=500, null=False)
    associated_project = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "project_summary"

class SampleMetaCurated(models.Model):
    #Project_ID","Run_ID","Sample_name","Assay_type","Sequencing_method","Phenotype_name","Sample_description","Phenotype_ID","Country","Geographic_location","longitude","lattitude","Age","Sex","BMI","Antibiotic_use","Antibiotic_name","Bodysite","batch","batch2
    project_id = models.CharField(max_length=100, null=False)
    run_id = models.CharField(max_length=100, null=False)
    sample_name = models.CharField(max_length=100, null=False)
    assay_type = models.CharField(max_length=100, null=False)
    sequencing_method = models.CharField(max_length=100, null=False)
    phenotype_name = models.CharField(max_length=100, null=False)
    sample_description = models.CharField(max_length=100, null=False)
    phenotype_id = models.CharField(max_length=100, null=False)
    country = models.CharField(max_length=100, null=False)
    geographic_location = models.CharField(max_length=100, null=False)
    longitude = models.CharField(max_length=100, null=False)
    lattitude = models.CharField(max_length=100, null=False)
    age = models.CharField(max_length=100, null=False)
    sex = models.CharField(max_length=100, null=False)
    bmi = models.CharField(max_length=100, null=False)
    antibiotic_use = models.CharField(max_length=100, null=False)
    antibiotic_name = models.CharField(max_length=100, null=False)
    bodysite = models.CharField(max_length=100, null=False)
    batch = models.CharField(max_length=100, null=False)
    batch2 = models.CharField(max_length=100, null=False)
    QC_state = models.CharField(max_length=100, null=False)
    QC_Bacteria = models.CharField(max_length=100, null=False)
    QC_Bacteria_gg = models.CharField(max_length=100, null=False)
    QC_Fungi = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = "sample_meta_curated"

class Searchable(models.Model):
    type = models.CharField(max_length=100, null=False)
    keywords = models.CharField(max_length=100, null=False)
    accession = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = "searchable"

class taxa2ncbi(models.Model):
    hgmt_micro_id = models.CharField(max_length=100, null=False)
    level = models.CharField(max_length=100, null=False)
    taxa = models.CharField(max_length=300, null=False)
    short_name = models.CharField(max_length=100, null=False)
    taxid = models.CharField(max_length=100, null=False)
    scientific_name = models.CharField(max_length=300, null=False)

    class Meta:
        db_table = "taxa2ncbi"

class FeatureTableFungi(models.Model):
    taxa = models.CharField(max_length=500, null=False)
    run_id = models.CharField(max_length=100, null=False)
    abundance = models.FloatField(null=False)
    # abundance 以 100 为基准

    class Meta:
        db_table = "feature_table_fungi"

class FeatureTableBac(models.Model):
    taxa = models.CharField(max_length=500, null=False)
    run_id = models.CharField(max_length=100, null=False)
    abundance = models.FloatField(null=False)
    # abundance 以 100 为基准

    class Meta:
        db_table = "feature_table_bac"