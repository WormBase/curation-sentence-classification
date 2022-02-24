#!/usr/bin/env bash

psql -U ${PSQL_USER} -h ${PSQL_HOST} -d ${PSQL_DATABASE} -c "select exp_pattern from exp_pattern" -t -o extracted_sentences/sentences_exp_pattern.txt
psql -U ${PSQL_USER} -h ${PSQL_HOST} -d ${PSQL_DATABASE} -c "select exp_subcellloc from exp_subcellloc" -t -o extracted_sentences/sentences_exp_subcellloc.txt