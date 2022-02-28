#!/usr/bin/env bash

# possibly exclude paper ids for large scale experiments? 00006525 00031006

psql -U ${PSQL_USER} -h ${PSQL_HOST} -d ${PSQL_DATABASE} -c "select exp_pattern from exp_pattern join exp_paper on exp_pattern.joinkey = exp_paper.joinkey where exp_paper.exp_paper NOT LIKE '%WBPaper00006525%' and exp_paper.exp_paper NOT LIKE '%WBPaper00031006%'" -t -o extracted_sentences/sentences_exp_pattern.txt
psql -U ${PSQL_USER} -h ${PSQL_HOST} -d ${PSQL_DATABASE} -c "select exp_subcellloc from exp_subcellloc join exp_paper on exp_subcellloc.joinkey = exp_paper.joinkey where exp_paper.exp_paper NOT LIKE '%WBPaper00006525%' and exp_paper.exp_paper NOT LIKE '%WBPaper00031006%'" -t -o extracted_sentences/sentences_exp_subcellloc.txt