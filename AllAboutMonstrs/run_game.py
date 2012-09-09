#!/usr/bin/env python
import argparse
import AllAboutMonstrs.__main__
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    add = ap.add_argument
    add("--test-start-state", default=None)
    args = ap.parse_args()
    AllAboutMonstrs.__main__.main(args)
