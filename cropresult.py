#!/usr/bin/env python3

import argparse
import json
import sys


def parse_args():
    ap = argparse.ArgumentParser(description="Crop too long tests out of results.json")
    ap.add_argument('-s', '--size', default=2000000,
                    help='Max size for out/err/dmesg')
    ap.add_argument('-i', '--inline', action='store_true',
                    help='Process results.json inline, termination can corrupt file')
    ap.add_argument('-f', '--filename', default='results.json', help="results.json")
    return ap.parse_args()


def main():
    with open(args.filename, "r") as fp:
        j = json.load(fp)
    for t in list(j["tests"].keys()):
        size = len(j["tests"][t]["dmesg"])
        if size > args.size:
            print("Removing", size, t, file=sys.stderr)
            del(j["tests"][t])
    if not args.inline:
        print(j)
    else:
        with open(args.filename, "w") as fp:
            json.dump(j, fp)
    return 0


if __name__ == '__main__':
    args = parse_args()
    print(args)
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr)
        exit(128+15)
