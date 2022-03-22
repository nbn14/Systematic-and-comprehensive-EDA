import pandas as pd
from pandas.api.types import is_numeric_dtype,is_string_dtype


def identify_cat_con(df,threshold=0.05):
    """
    Heuritic identification of continuous and categorical data
    Parameters:
    -----------
    df: pd.DataFrame
    threshold: float, [0,1], default=0.05
        Ratio of unique values vs total number of values
    
    Returns:
    --------
    con_data: list of column names of continuous variables
    cat_data: list of column names of categorical variables
    """
    cat_data = []
    con_data =[]
    for col in df.columns:
        colcount = df[col].nunique()/df[col].count()
        if colcount<=threshold:
            cat_data.append(col)
        else:
            con_data.append(col)

    return con_data,cat_data

    

def is_numeric(array):
    """Return False if any value in the array or list is not numeric
    Note boolean values are taken as numeric"""
    for i in array:
        try:
            float(i)
        except ValueError:
            return False
        else:
            return True

def dtype_standardise(df):
    """
    Parameters:
    -----------
    df: pd.DataFrame
    Returns:
    --------
    df: casted dataframe
        Boolean columns are preserved as this is implicitly numeric
    """
    for col in df.columns:
            if is_numeric(df[col])==False:
                df[col].astype(object)
    return df  

def check_repeated(df,sel_col,id):
    """
    Checking for # of unique combinations of a selection of attributes.
    Different IDs sometimes do not guarantee uniqueness  
    
    Parameters:
    -----------
    df: pd.DataFrame
    sel_col: list of column names 
        Selection of columns where number of unique combinations is investigated
    id: Name of column with unique id
    Returns:
    --------
    dup_instances: int
        Number of instances with more than 1 appearance in the datasetbased on sel_col
    tot_instances: int
        # of instances in the population duplicated

    """
    df0 = df.groupby(by=sel_col).agg({id:"count"}).reset_index()

    dup_instances = (df0[id]>1).sum()
    tot_instances = df0[df0[id]>1][id].sum()

    return dup_instances,tot_instances

