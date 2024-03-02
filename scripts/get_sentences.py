import argparse
import logging
import os

import numpy as np
from wbtools.lib.nlp.common import PaperSections
from wbtools.literature.corpus import CorpusManager
from nltk import sent_tokenize

from common import get_papers_from_cs_form


def main():
    parser = argparse.ArgumentParser(description="Extract a set of negative sentence for a given datatype")
    parser.add_argument("-N", "--db-name", metavar="db_name", dest="db_name", type=str)
    parser.add_argument("-U", "--db-user", metavar="db_user", dest="db_user", type=str)
    parser.add_argument("-P", "--db-password", metavar="db_password", dest="db_password", type=str, default="")
    parser.add_argument("-H", "--db-host", metavar="db_host", dest="db_host", type=str)
    parser.add_argument("-w", "--http-username", metavar="http_user", dest="http_user", type=str)
    parser.add_argument("-z", "--http-password", metavar="http_password", dest="http_password", type=str)
    parser.add_argument("-k", "--http-host", metavar="http_host", dest="http_host", type=str)
    parser.add_argument("-l", "--log-file", metavar="log_file", dest="log_file", type=str, default=None,
                        help="path to the log file to generate")
    parser.add_argument("-L", "--log-level", dest="log_level", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR',
                                                                        'CRITICAL'], default="INFO",
                        help="set the logging level")
    parser.add_argument("-n", "--num-papers", metavar="num_papers", dest="num_papers", type=int, default=None,
                        help="number of papers to process, from the most recent")
    parser.add_argument("-i", "--paper-ids", metavar="paper_ids", dest="paper_ids", type=str, nargs="+", default=None,
                        help="process the provided list of papers instead of automatically obtaining them. Accepted "
                             "values are list of string IDs or file path where to read them")
    parser.add_argument("-m" "--method", metavar="method", dest="method", type=str, default="allval%20neg",
                        help="curation status form method")
    parser.add_argument("-o" "--output-file", metavar="out_file", dest="out_file", type=str,
                        help="file where to write sentences")
    parser.add_argument("-d" "--datatype", metavar="datatype", dest="datatype", type=str, default="otherexpr",
                        help="cs datatype")
    args = parser.parse_args()
    logging.basicConfig(filename=args.log_file, level=args.log_level,
                        format='%(asctime)s - %(name)s - %(levelname)s:%(message)s')
    if args.paper_ids:
        if os.path.exists(args.paper_ids[0]):
            papers_to_extract = ["000" + line.strip() for line in open(args.paper_ids[0])]
        else:
            papers_to_extract = args.paper_ids
    else:
        logging.info("reading list of paper ids from curation status form")
        papers_to_extract = get_papers_from_cs_form(datatype=args.datatype, user=args.http_user,
                                                    password=args.http_password, host=args.http_host,
                                                    method=args.method)
    if args.num_papers:
        papers_to_extract = sorted(papers_to_extract, reverse=True)[0:args.num_papers]
    cm = CorpusManager()
    cm.load_from_wb_database(args.db_name, args.db_user, args.db_password, args.db_host, paper_ids=papers_to_extract,
                             exclude_temp_pdf=True, exclude_no_main_text=True, main_file_only=True)

    with open(args.out_file, 'w') as out_file:
        for paper in cm.get_all_papers():
            pap_sentences = paper.get_text_docs(include_supplemental=False, split_sentences=True,
                                                return_concatenated=False)
            for sentence in pap_sentences:
                if len(sentence) > 10 and len(sentence.split(" ")) > 2:
                    out_file.write(paper.paper_id + "\t" + sentence+ "\n")


if __name__ == '__main__':
    main()
