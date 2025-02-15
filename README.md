# VAMB abundance profile

This is a small package to create an abundance profile from a VAMB output. 

We assume that you have already run VAMB and have the output files, and we read
the abundance.npz file and composition.npz files to create a table with the 
abundance of each contig in each sample.

We append the cluster information from `vae_clusters.tsv` to the table.

Next, we use the first dimnension of a PCA to reduce the dimensionality of the
data so that we end up with a single abundance profile for each cluster.

You can write the final abundance profile to a file using the _required_ `--cluster` option, and
you can also write the intermediate table to a file using the _optional_ `--abundance` option.

## Installation

You can install the package using pip:

```bash
pip install vamb-abundance-profile
```

## Usage

Note that by default the `vamb` directory is in the output directory you specified when running VAMB. 
That directory should contain the `abundance.npz`, `composition.npz`, and `vae_clusters.tsv` files.


```bash
vamb_abundance_profile --vamb vamb/vamb/ --cluster vamb/clusters.tsv.gz -v
```

## Output

The output is a tab-separated file with the abundance profile of each cluster in each sample.

Note that by default we use `gzip` compression. If your file names do not end `.gz`, we add that for you!
If you don't want compression, then uncompress the file after running the script.


