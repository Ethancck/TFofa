import argparse
usage = "Fofa [options]"
parser = argparse.ArgumentParser(prog='Fofa', usage=usage)
# report
report = parser.add_argument_group("Report", "Report options")
report.add_argument('--out', dest="report_name", type=str, default="result.csv",
                    help="generate the report name,default(result.csv)")
report.add_argument('--cidr', dest="cidr",action="store_true",
                    help="generate cidr file(default cidr.txt)")
# Requests options
request = parser.add_argument_group("Request", "request options")
request.add_argument("--size", dest="size", type=int, default=10000, help="The Fofa API Requests of sizes(default 100) ")
request.add_argument("--query", dest="query", type=str, help="your query words!")
request.add_argument("--cert", dest="cert", type=str, help="your domains file!(dork:'cert=\"domain\" && type=\"subdomain\" && country=\"CN\"')")
request.add_argument("--status_code", dest="status_code", type=str, default="",help="dork:status_code=""")
args = parser.parse_args()
