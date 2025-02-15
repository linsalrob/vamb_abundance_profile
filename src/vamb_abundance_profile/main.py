"""
This is the main script for the project. Take the parameters and run the appropriate functions
"""

import os
import sys
import argparse
from .read_vamb_dir import read_vamb
from .pca import cluster_abundance
from .bcolors import bcolors

__author__ = 'Rob Edwards'





def main():
    """
    Run the main script
    """
    parser = argparse.ArgumentParser(description=' ')
    parser.add_argument('-d', '--vamb', help='vamb directory', required=True)
    parser.add_argument('-c', '--cluster', help='cluster abundance output file', required=True) 
    parser.add_argument('-a', '--abundance', help='all contigs abundance output file (optional)')
    parser.add_argument('-v', '--verbose', help='verbose output', action='store_true')
    args = parser.parse_args()


    if not os.path.exists(args.vamb):
        sys.stderr.write(f"{bcolors.RED}ERROR: {args.vamb} does not exist{bcolors.ENDC}\n")
        sys.exit(-1)

    if args.abundance:
        df = read_vamb(args.vamb, args.abundance, args.verbose)
    else:
        df = read_vamb(args.vamb, None, args.verbose)

    pca_df = cluster_abundance(df)

    if not args.cluster.endswith('.gz'):
        args.cluster += '.gz'

    if args.verbose:
        print(f"{bcolors.GREEN}Writing compressed clusters to {args.cluster}{bcolors.ENDC}")
    
    pca_df.to_csv(args.cluster, compression='gzip', sep='\t')

