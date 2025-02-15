"""
Read the vamb abundance and composition files and 
create a dataframe of the abundance profile
"""

import os
import sys
import pandas as pd
import numpy as np
from .bcolors import bcolors
__author__ = 'Rob Edwards'



def read_abundance(vamb_dir, verbose=False):
    """
    Read the abundance and composition files from vamb and create a dataframe
    """

    if verbose:
        sys.stderr.write(f"{bcolors.GREEN}Reading the abundance and composition files from {vamb_dir}{bcolors.ENDC}\n")

    if not os.path.exists(os.path.join(vamb_dir, 'abundance.npz')):
        sys.stderr.write(f"{bcolors.RED}FATAL: abundance.npz not found in {vamb_dir}{bcolors.ENDC}\n")
        sys.exit(-1)

    if not os.path.exists(os.path.join(vamb_dir, 'composition.npz')):
        sys.stderr.write(f"{bcolors.RED}FATAL: composition.npz not found in {vamb_dir}{bcolors.ENDC}\n")
        sys.exit(-1)


    # Load the npz files
    abundance = np.load(os.path.join(vamb_dir, 'abundance.npz'), allow_pickle=True)
    composition = np.load(os.path.join(vamb_dir, 'composition.npz'), allow_pickle=True)

    # Extract the data
    matrix = abundance['matrix']
    samplenames = abundance['samplenames']
    samplenames = np.array([s.split('/')[-1].replace('.bam', '') for s in samplenames])
    identifiers = composition['identifiers'] 

    # Create the DataFrame
    df = pd.DataFrame(matrix, index=identifiers, columns=samplenames)

    return df


def read_clusters(vamb_dir, verbose=False):
    """
    Read the cluster file and return a dataframe
    """

    if verbose:
        print(f"{bcolors.GREEN}Reading the cluster file from {vamb_dir}{bcolors.ENDC}", file=sys.stderr)

    if not os.path.exists(os.path.join(vamb_dir, 'vae_clusters.tsv')):
        print(f"{bcolors.RED}FATAL: vae_clusters.tsv not found in {vamb_dir}{bcolors.ENDC}", file=sys.stderr)
        sys.exit(-1)

    df = pd.read_csv(os.path.join(vamb_dir, 'vae_clusters.tsv'), sep="\t", header=None, names=['cluster', 'contig'])
    df = df.set_index('contig')

    return df


def read_vamb(vamb_dir, abundance_output=None, verbose=False):
    """
    Read the vamb output and return a dictionary of dataframes
    """

    if verbose:
        print(f"{bcolors.GREEN}Reading the vamb output from {vamb_dir}{bcolors.ENDC}", file=sys.stderr)

    abundance = read_abundance(vamb_dir, verbose)
    clusters = read_clusters(vamb_dir, verbose)
    df = abundance.join(clusters, how='inner')
    if abundance_output:
        if not abundance_output.endswith('.gz'):
            abundance_output += '.gz'
        print(f"{bcolors.PINK}Writing compressed abundance output to {abundance_output}{bcolors.ENDC}", file=sys.stderr)
        df.to_csv(abundance_output, sep="\t", compression='gzip')

    return df




