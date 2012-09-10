#!/usr/bin/env python
import argparse
import AllAboutMonstrs.__main__
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    add = ap.add_argument
    add("--test-start-state", default=None,
        help="Commence a particular mode of operation")
    add("--debug-rectangles", default=False, action="store_true",
        help="Make visible the footprint rectangles")
    args = ap.parse_args()
    AllAboutMonstrs.__main__.main(args)
