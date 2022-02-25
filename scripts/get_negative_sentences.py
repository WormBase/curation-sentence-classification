import argparse
import logging

from wbtools.db.dbmanager import WBDBManager
from wbtools.literature.corpus import CorpusManager

from common import get_negative_paper_ids


def main():
    parser = argparse.ArgumentParser(description="Extract a set of negative sentence for a given datatype")
    parser.add_argument("-N", "--db-name", metavar="db_name", dest="db_name", type=str)
    parser.add_argument("-U", "--db-user", metavar="db_user", dest="db_user", type=str)
    parser.add_argument("-P", "--db-password", metavar="db_password", dest="db_password", type=str, default="")
    parser.add_argument("-H", "--db-host", metavar="db_host", dest="db_host", type=str)
    parser.add_argument("-w", "--http-username", metavar="http_user", dest="http_user", type=str)
    parser.add_argument("-z", "--http-password", metavar="http_password", dest="http_password", type=str)
    parser.add_argument("-y", "--ssh-user", metavar="ssh_user", dest="ssh_user", type=str)
    parser.add_argument("-j", "--ssh-password", metavar="ssh_password", dest="ssh_password", type=str)
    parser.add_argument("-s", "--ssh-host", metavar="ssh_host", dest="ssh_host", type=str)
    parser.add_argument("-k", "--http-host", metavar="http_host", dest="http_host", type=str)
    parser.add_argument("-l", "--log-file", metavar="log_file", dest="log_file", type=str, default=None,
                        help="path to the log file to generate")
    parser.add_argument("-L", "--log-level", dest="log_level", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR',
                                                                        'CRITICAL'], default="INFO",
                        help="set the logging level")
    parser.add_argument("-n", "--num-papers", metavar="num_papers", dest="num_papers", type=int, default=None,
                        help="number of papers to process, from the most recent")
    parser.add_argument("-i", "--paper-ids", metavar="paper_ids", dest="paper_ids", type=str, nargs="+", default=None,
                        help="process the provided list of papers instead of automatically obtaining them")
    args = parser.parse_args()
    logging.basicConfig(filename=args.log_file, level=args.log_level,
                        format='%(asctime)s - %(name)s - %(levelname)s:%(message)s')
    if args.paper_ids:
        papers_to_extract = args.paper_ids
    else:
        logging.info("reading list of validated negative paper ids from curation status form")
        papers_to_extract = get_negative_paper_ids(datatype="otherexpr", user=args.http_user,
                                                   password=args.http_password, host=args.http_host)
    if args.num_papers:
        papers_to_extract = sorted(papers_to_extract, reverse=True)[0:args.num_papers]
    cm = CorpusManager()
    cm.load_from_wb_database(args.db_name, args.db_user, args.db_password, args.db_host, ssh_user=args.ssh_user,
                             ssh_passwd=args.ssh_password, ssh_host=args.ssh_host, paper_ids=papers_to_extract)
    pass


if __name__ == '__main__':
    main()