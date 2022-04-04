#!/usr/bin/env python

import argparse
import sys
import typing

def main(argv):
    parser = argparse.ArgumentParser(description='Tests for a greatest common factor; returns 1 if co-prime')
    parser.add_argument('numbers', nargs='+', default=[11, 26], type=int,
                        help='numbers to test for gcd', metavar='Numbers')
    #Error try-catch

    try:               
        args = parser.parse_args()
    except:
        sys.exit('Error: ArgumentParser failed to parse the arguments')
    try:
        number = getattr(args, "numbers")
    except:
        sys.exit('Error Parsing Args')
    if len(args.numbers) == 1:
        print(args.numbers[0])
        return args.numbers[0]

    result = args.numbers[0]
    for arg in args.numbers:
        result = gcd(result, arg)
    print(result)

def gcd(x, y):
    while(y):
        x, y = y, x % y
    return x

if __name__ == "__main__":
    main(sys.argv)