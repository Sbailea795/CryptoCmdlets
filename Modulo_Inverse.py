#!/usr/bin/env python

import argparse
import sys
import typing

from numpy import number

def main(argv):
    parser = argparse.ArgumentParser(description='Finds the multiplicitive inverse given a modulo')
    parser.add_argument('number', type=int,
                        help='number', metavar='Number')
    parser.add_argument('modulo', type=int,
                        help='modulo', metavar='Modulo')
    #Error try-catch
    try:               
        args = parser.parse_args()
    except:
        sys.exit('Error: ArgumentParser failed to parse the arguments')
    print(modinv(args.number, args.modulo))

def modinv(number, modulo):
    try:
        return(pow(number, -1, modulo))
    except:
        sys.exit( "Error: Inverse of {:d} not available with the given modulo {:d}".format(number, modulo) )
    
 
if __name__ == "__main__":
   main(sys.argv[1:])