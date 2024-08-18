import os
import pandas as pd

def load_lalonde_data(dataset='lalonde_exp'):
    """
    Load the Lalonde dataset.

    Parameters:
    -----------
    dataset : str
        The name of the dataset to load. Options are:
        'lalonde_exp', 'lalonde_exp_panel', 'lalonde_psid', 'lalonde_psid_panel'.

    Returns:
    --------
    pandas.DataFrame
        The requested dataset as a pandas DataFrame.
    """
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    file_path = os.path.join(data_dir, f'{dataset}.csv')
    
    if not os.path.exists(file_path):
        raise ValueError(f"Dataset {dataset} not found.")
    
    return pd.read_csv(file_path)