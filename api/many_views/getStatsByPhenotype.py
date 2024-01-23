from api.many_views.base import *


def get_general_marker_stats(mesh_id1, mesh_id2):
    sql = """
        select
        	tnew1.*,
        	t2.term as phenotype1_term, t3.term as phenotype2_term,
            %s as mesh_id1,
            %s as mesh_id2
        from
        	(select
        		count( distinct( project_id ) ) as projects,
                count( distinct( ncbi_taxon_id) ) as markers,
                COALESCE( count(distinct( if( taxon_rank_level = 'species' , ncbi_taxon_id, NULL) ) ), 0) as marker_species,
                COALESCE( count(distinct( if( taxon_rank_level = 'genus' , ncbi_taxon_id, NULL) ) ), 0) as marker_genus
        	from curated_lefse_analysis_results
        	where phenotype1 = %s and phenotype2 = %s ) as tnew1,
            mesh_data as t2,
            mesh_data as t3
        where
        	t2.uid = %s and
            t3.uid = %s; 
            """
    with connection.cursor() as cursor:
        cursor.execute(sql, [mesh_id1, mesh_id2, mesh_id1, mesh_id2, mesh_id1, mesh_id2])
        return dict_fetchall(cursor)

def get_marker_counts_by_project(mesh_id):
    sql = """
        select
          da_id, count(*) as markers
        from da_results
        LEFT JOIN disease_info on disease_info.phenotype_name = da_results.case_name
        where mesh_id = %s group by da_id;
        """
    with connection.cursor() as cursor:
        cursor.execute(sql, [mesh_id])
        return dict_fetchall(cursor)


def get_run_summary_by_phenotype(mesh_id):
    sql = """
    SELECT 
        case_name, da_id, da_results.batch, assay_type, project_id,
        COUNT(CASE WHEN kingdom = 'bacteria' AND taxon_level = 'genus' THEN 1 END) AS bac_genus,
        COUNT(CASE WHEN kingdom = 'bacteria' AND taxon_level = 'species' THEN 1 END) AS bac_species,
        COUNT(CASE WHEN kingdom = 'fungi' AND taxon_level = 'genus' THEN 1 END) AS fungi_genus,
        COUNT(CASE WHEN kingdom = 'fungi' AND taxon_level = 'species' THEN 1 END) AS fungi_species
    FROM da_results
    LEFT JOIN disease_info on disease_info.phenotype_name = da_results.case_name
    LEFT JOIN (
        SELECT distinct project_id, batch, batch2
        FROM sample_meta_curated
    ) as t1 on t1.batch2 = da_results.batch
    where mesh_id = %s
    GROUP BY case_name, da_id, da_results.batch, assay_type, project_id;
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, [mesh_id])
        return dict_fetchall(cursor)
    

def get_all_data_of_phenotype_comparison(mesh_id):
    sql = """
        SELECT 
            batch as project_id,
            taxon_level as taxon_rank_level,
            lfc as LDA,
            assay_type as experiment_type,
            display,
            taxa_short_name as scientific_name,
            nrproj,
            conflict,
            case
                when taxa like 'k__Bacteria%%' then 'bacteria' 
                when taxa like 'k__Fungi%%' then 'fungi' 
                else 'other' 
            end as kingdom
        FROM da_results
        LEFT JOIN disease_info on disease_info.phenotype_name = da_results.case_name
        where mesh_id = %s;
        """
    with connection.cursor() as cursor:
        cursor.execute(sql, [mesh_id])
        return dict_fetchall(cursor)
    