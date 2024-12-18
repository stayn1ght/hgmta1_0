# process da_results table

library("tidyverse")
getwd()
daResults <- read_csv("02_da_results.csv", 
    skip = 1,
    col_names = c(
    "taxa",
    "da_id",
    "batch",
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
    "display",
    "taxon_id",
    "scientific_name",
    "scientific_short_name"))

daResults %>%
    group_by(case_name, taxa) %>%
    mutate(
        nrproj = n(),
        conflict = ifelse(
            sum(ifelse(lfc > 0, 1, 0)) > 0 & sum(ifelse(lfc < 0, 1, 0)) > 0, 
            0, 1
            )
    ) %>%
    ungroup() %>%
    write.csv("02_da_results_processed.csv",  row.names = FALSE)
  
