"""
Reduce the dimensionality of a dataset using PCA
"""

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

def get_pca_first_component(group, numeric_cols):
    """
    Function to apply PCA only when there are two or more samples in the group
    """

    if len(group) == 1:
        return group[numeric_cols].values.flatten()  # Return raw values
    else:
        pca = PCA(n_components=1)
        transformed = pca.fit_transform(group[numeric_cols].T)  # Apply PCA
        return transformed[:, 0]  # Return first principal component

def cluster_abundance(df):
    """
    Apply PCA to each cluster and return the first principal component
    """

    # Assume df has 127 numerical columns + 'cluster' as the last column
    numeric_cols = df.columns[:-1]  # All columns except 'cluster'

    # Apply function and handle variable-length outputs
    pca_results = df.groupby('cluster').apply(get_pca_first_component, numeric_cols)

    pca_matrix = np.vstack(pca_results.values)  # Stack arrays
    pca_df = pd.DataFrame(pca_matrix, index=pca_results.index, columns=numeric_cols)

    return pca_df


