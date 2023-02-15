#!/usr/bin/env python3
#
# splitresult.py
#
# Split tests from results.json to N files
#
# When importing the files separately, psycog2 doesn't cough up to OOM
#

import argparse
import copy
import json
from math import ceil
import sys


def parse_args():
    ap = argparse.ArgumentParser(description="Split results.json to N pieces")
    ap.add_argument('-n', type=int, default=5,
                    help='Number of new jsons')
    ap.add_argument('-f', '--filename', default='results.json', help="results.json")
    return ap.parse_args()


def main():
    with open(args.filename, "r") as fp:
        j = json.load(fp)
    testnames = list(j["tests"].keys())
    testsperfile = ceil(len(testnames)/args.n)
    print(f"Tests {len(testnames)} per-file {testsperfile}")
    if testsperfile < 1: return -1
    outj = None
    outf = 1
    for t in testnames:
        # start new json by copying everything and removing non-relevant parts
        if not outj:
            outj = copy.deepcopy(j)
            # clear statistics
            outj["tests"] = {}
            outj["totals"] = {}
            outj["runtimes"] = {}
            outn = 0
        # copy test per test
        outj["tests"][t] = j["tests"][t]
        outn += 1
        # filled one json or got to the last test
        if outn >= testsperfile or t == testnames[-1]:
            print(f"Writing results{outf}.json with {outn} tests")
            with open(f"results{outf}.json", "w") as fp:
                json.dump(outj, fp)
            outj = None
            outf += 1

    return 0


if __name__ == '__main__':
    args = parse_args()
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr)
        sys.exit(128+15)
