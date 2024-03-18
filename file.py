import argparse, requests, datetime
from helpers.splashscreen import splashscreen

# Take in CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', help="Discord CDN File URL", required=True)
args = parser.parse_args()

file = args.file

print()
splashscreen()

# Get file url
response = requests.get(file)
if response.status_code == 200:
    # If request succeeded
    print("\n\x1b[1m\x1b[4mFile\x1b[0m")
    print(f"\x1b[1mURL                   \x1b[0m{file}")
    print(f"\x1b[1mTYPE                  \x1b[0m{response.headers["Content-Type"]}")
    print(f"\x1b[1mUPLOAD TIME           \x1b[0m{datetime.datetime.strptime(response.headers["Last-Modified"], "%a, %d %b %Y %H:%M:%S %Z").isoformat()}")
else:
    # If request failed present an error message
    print("\nUnknown file")

print()