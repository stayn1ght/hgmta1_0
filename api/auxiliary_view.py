from django.db import connection

from api import models
from api.many_views.base import execute_page_sql, dict_fetchall
from django.db.models import Q


def execute_sql(cursor, sql, many=False, lst=None):
    if lst is None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, lst)
    raw_data = cursor.fetchone()
    if many:
        if raw_data is not None:
            return dict([(desc[0], int(raw_data[i])) for i, desc in enumerate(cursor.description)])
        else:
            return None
    else:
        if raw_data is not None:
            return int(raw_data[0])
        else:
            return None


def get_stats():
    sql = """
            select
                count(DISTINCT project_id) as total_projects,
                count(DISTINCT CASE WHEN has_it_been_collected = 'Y' THEN project_id END) as project_count_with_valid_phenotype_data,
                count(DISTINCT CASE WHEN has_it_been_collected = 'N' THEN project_id END) as project_count_with_invalid_phenotype_data,
                sum(CASE WHEN has_it_been_collected = 'N' THEN Number_of_runs END) 
            as run_count_without_valid_phenotype_data,
                sum(CASE WHEN has_it_been_collected = 'N' THEN Number_of_samples 
            END) as sample_count_without_valid_phenotype_data
            from
                projects
            where
                project_id != ''"""
    sql_all_runs_count = """select 
                                count(distinct (run_id)) all_runs_count
                            from 
                                sample_to_run_info 
                            where 
                                project_id != '';"""
    sql_sample_count = """
                        select 
                            count(DISTINCT CASE WHEN t2.QCStatus = 1 THEN project_id END ) as loaded_projects_count,
                            count(DISTINCT CASE WHEN t2.QCStatus = 1 THEN run_id END ) as loaded_runs_count,
                            count(distinct(project_id)) as processed_project_count,
                            count( distinct(run_id) ) as processed_runs_count,
                            count( DISTINCT CASE WHEN t2.QCStatus = 0 THEN project_id END ) as failed_project_count, 
                            count( DISTINCT CASE WHEN t2.QCStatus = 0 THEN run_id END ) as failed_runs_count
                        from 
                            sample_to_run_info  as t1, 
                            samples_loaded as t2 
                        where 
                            t1.run_id = t2.accession_id;"""
    sql_pheonotype_count = """
            select 
                count(*) as pheonotype_count
            from
                stats_by_phenotype
            where 
                disease != '' and disease != 'NA';"""
    sql_species_genus_count = """
                            select 
                                count( DISTINCT CASE WHEN taxon_rank_level = 'species' THEN ncbi_taxon_id END ) as all_species_count,
                                count( DISTINCT CASE WHEN taxon_rank_level = 'genus' THEN ncbi_taxon_id END ) as all_genus_count
                            from 
                                species_abundance_summary 
                            where 
                                disease != '';"""
    stats = {}
    with connection.cursor() as cursor:
        stats.update(execute_sql(cursor, sql, many=True))
        stats['all_runs_count'] = execute_sql(cursor, sql_all_runs_count)
        stats.update(execute_sql(cursor, sql_sample_count, many=True))
        stats['pheonotype_count'] = execute_sql(cursor, sql_pheonotype_count)
        stats.update(execute_sql(cursor, sql_species_genus_count, many=True))
        return stats


def get_stats_markers():
    sql = """
            select 
                count( DISTINCT CASE WHEN  taxon_rank_level = 'species' THEN ncbi_taxon_id END)  as marker_species_count,
                count( DISTINCT CASE WHEN  taxon_rank_level = 'genus' THEN ncbi_taxon_id END)  as marker_genus_count,
                count( DISTINCT ncbi_taxon_id, taxon_rank_level) as marker_taxa_count,
                count( DISTINCT ncbi_taxon_id, taxon_rank_level) as retrieved_species_count,
                count( DISTINCT project_id ) as projects,
                count( DISTINCT phenotype1, phenotype2) as phenotype_pairs
            from curated_lefse_analysis_results;"""
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return dict_fetchall(cursor)[0]


def get_stats_projects():
    sql = """
            select
                count( distinct( project_id ) ) as projects_cnt,
                count( distinct( phenotype ) ) as phenotypes_cnt,
                count( * ) as samples_cnt
            from
                curated_lefse_analysis_group_to_samples;
            """
    with connection.cursor() as cursor:
        return execute_sql(cursor, sql, many=True)


def get_top10diseases():
    sql = """
            select 
                disease, failed_runs, 
                valid_runs as loaded_runs, 
                all_samples as nr_total_samples,
                term
            FROM stats_by_phenotype
            /*前10逆序排序*/
            ORDER BY all_samples DESC
            LIMIT 10"""
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return dict_fetchall(cursor)


def get_disease2term():
    obj = models.StatsByPhenotype.objects.filter(~Q(disease='')).values('disease', 'term')
    disease2term = {}
    if len(obj) > 0:
        for item in obj:
            disease2term[item['disease']] = item['term']
        return disease2term
    else:
        return None


def get_all_phenotype_comparisons_data():
    sql = """
            select
                tnew1.*, t2.term as phenotype1_term, t3.term as phenotype2_term
            from
                ( 
                select
                        phenotype1, phenotype2, count(distinct(project_id)) as projects, 
                        count(distinct(ncbi_taxon_id)) as markers
                from curated_lefse_analysis_results
                group by phenotype1, phenotype2) as tnew1,
                mesh_data as t2,
                mesh_data as t3
            where
                t2.uid = tnew1.phenotype1 and
                t3.uid = tnew1.phenotype2;"""
    with connection.cursor() as cursor:
        data = execute_page_sql(cursor, sql)
        return data


def get_all_phenotype_comparisons_stats():
    sql = """
            SELECT 
                COUNT(DISTINCT project_id) AS projects,
                COUNT(DISTINCT ncbi_taxon_id) AS markers,
                COUNT(DISTINCT phenotype1, phenotype2) AS phenotype_combinations
            FROM curated_lefse_analysis_results"""
    with connection.cursor() as cursor:
        stats = execute_sql(cursor, sql, many=True)
        return stats

