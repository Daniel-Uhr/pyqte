import pandas as pd

class PanelDataChecker:
    """
    PanelDataChecker is used to verify the quality and structure of panel data before estimation.
    
    Attributes:
    -----------
    data : pandas.DataFrame
        The dataset containing the panel data.
    id_column : str
        The name of the column containing the individual IDs.
    time_column : str
        The name of the column containing the time period.
    """

    def __init__(self, data, id_column, time_column):
        self.data = data
        self.id_column = id_column
        self.time_column = time_column

    def check_missing_data(self):
        """
        Check for missing data in the panel dataset.
        
        Returns:
        --------
        missing_data : pandas.DataFrame
            A DataFrame indicating the number of missing values for each column.
        """
        missing_data = self.data.isnull().sum()
        return missing_data

    def check_balanced_panel(self):
        """
        Check if the panel data is balanced.
        
        Returns:
        --------
        is_balanced : bool
            True if the panel is balanced, False otherwise.
        """
        panel_counts = self.data.groupby(self.id_column)[self.time_column].nunique()
        is_balanced = panel_counts.nunique() == 1
        return is_balanced

    def check_duplicate_entries(self):
        """
        Check for duplicate entries in the panel data.
        
        Returns:
        --------
        duplicate_entries : pandas.DataFrame
            A DataFrame containing any duplicate entries found in the dataset.
        """
        duplicates = self.data[self.data.duplicated(subset=[self.id_column, self.time_column], keep=False)]
        return duplicates

    def summary(self):
        """
        Provide a summary of the panel data checks.
        
        Returns:
        --------
        summary_dict : dict
            A dictionary summarizing the checks performed on the panel data.
        """
        summary_dict = {
            "Missing Data": self.check_missing_data(),
            "Balanced Panel": self.check_balanced_panel(),
            "Duplicate Entries": self.check_duplicate_entries()
        }
        return summary_dict

