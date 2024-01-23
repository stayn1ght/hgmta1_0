# process da_results table

librayr("tidyverse")
getwd()
daResults <- read_csv("da_results.csv", col_names = c(
    "id",
    "da_id",
    "batch",
    "taxa",
    "kingdom",
    "taxon_level",
    "w_statistic",
    "p_value",
    "lfc",
    "assay_type",
    "case_name",
    "control_name",
    "num_case",
    "num_control",
    "taxa_short_name",
    "display"))

daResults %>%
    group_by(case_name, taxa) %>%
    mutate(
        nrproj = n(),
        conflict = ifelse(sum(ifelse(lfc > 0, 1, 0)) > 0 & sum(ifelse(lfc < 0, 1, 0)) > 0, 0, 1)
    ) %>%
    ungroup() %>%
    write.csv("da_results_processed.csv",  row.names = FALSE)
    
