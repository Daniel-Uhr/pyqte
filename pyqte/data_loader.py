import pandas as pd

def load_lalonde_data():
    """
    Load the Lalonde dataset from the local CSV files.
    
    Returns:
    --------
    dict of pandas.DataFrame:
        A dictionary containing the Lalonde datasets.
        Keys are 'exp', 'exp_panel', 'psid', and 'psid_panel'.
    """
    exp = pd.read_csv('data/lalonde.exp.csv')
    exp_panel = pd.read_csv('data/lalonde.exp.panel.csv')
    psid = pd.read_csv('data/lalonde.psid.csv')
    psid_panel = pd.read_csv('data/lalonde.psid.panel.csv')
    
    return {
        'exp': exp,
        'exp_panel': exp_panel,
        'psid': psid,
        'psid_panel': psid_panel
    }

def load_custom_data(file_path, sep=','):
    """
    Load a custom dataset from a specified file path.
    
    Parameters:
    -----------
    file_path : str
        The path to the data file.
    sep : str, optional (default=',')
        The delimiter to use.
    
    Returns:
    --------
    pandas.DataFrame
        The loaded dataset as a DataFrame.
    """
    return pd.read_csv(file_path, sep=sep)

def split_data_by_treatment(data, treatment_column):
    """
    Split a DataFrame into treated and control groups based on a treatment column.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        The dataset to split.
    treatment_column : str
        The name of the column that indicates treatment status.
    
    Returns:
    --------
    treated : pandas.DataFrame
        The subset of data where the treatment column equals 1.
    control : pandas.DataFrame
        The subset of data where the treatment column equals 0.
    """
    treated = data[data[treatment_column] == 1]
    control = data[data[treatment_column] == 0]
    
    return treated, control

def prepare_panel_data(data, id_column, time_column):
    """
    Prepare panel data for analysis by setting the index to a multi-index of ID and time.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        The panel dataset.
    id_column : str
        The column name representing individual IDs.
    time_column : str
        The column name representing time points.
    
    Returns:
    --------
    pandas.DataFrame
        The DataFrame with a multi-index set on ID and time.
    """
    return data.set_index([id_column, time_column])

def get_summary_statistics(data):
    """
    Calculate summary statistics for a dataset.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        The dataset to summarize.
    
    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing summary statistics (mean, std, min, max).
    """
    return data.describe()

