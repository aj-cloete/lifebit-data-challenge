import pandas as pd
from collections import defaultdict

def fix_dates(df, date_column=[]):
    """
    Extract the date part and the time part from the date_column.
    Args:
        df: the dataframe which should be transformed
        date_column: (string or list of strings) the date column(s) 
            which should be transformed
    Return:
        The same dataframe with provided date_column populated with a 
        DD-MM-YYYY date format and [date_column]_time populated with the time
    """
    if not isinstance(date_column, str):
        for d in date_column:
            df = fix_dates(df, d)
        return df
    if f"{date_column}_time" in df.columns:
        return df
    df = df.copy()
    if date_column not in df.columns:
        return df
    date_col = pd.to_datetime(df[date_column])
    dates = date_col.dt.strftime("%d-%m-%Y")
    times = date_col.dt.time
    df[date_column] = dates
    df[f"{date_column}_time"] = times
    return df

def get_date_columns():
    """
    Consult the data dictionary to find all date columns
    
    Return:
        A dict with table name as key and a list of date columns as value
    """
    from datasets import data_dictionary as dd
    date_rows = dd["Enumerations/Date Type"].str.lower().str.contains('date')
    return dd[date_rows][["Table", "Field"]].groupby("Table")\
        .apply(lambda x: list(x.Field)).to_dict()
    
def recursive_default_dictionary():
    """
    Return:
        A recursive default dictionary - useful data structure 
            to construct and store nested lookup data
    """
    return defaultdict(recursive_default_dictionary)

def get_dicts():
    """
    Extract the contents of the data dictionary and store it an a structured 
    nested dictionary
    Return:
        A nested dictionary with:
            first keys representing the table, 
            second keys representing fields of the table
            third keys representing the codes present in the field
            fourth keys representing the categories/levels of the field
    """
    from datasets import data_dictionary as dd
    dicts = recursive_default_dictionary()
    for table in dd.Table.unique():
        for field in dd[dd.Table==table].Field.unique():
            dd_filtered = dd[(dd.Table==table)&(dd.Field==field)]
            for item in dd_filtered["Enumerations/Date Type"]:
                if " = " not in item:
                    continue
                try:
                    k, v = item.split(" = ")
                    if not (k and v):
                        continue
                    dicts[table][field][k] = v
                except Exception:
                    for comb in item.split(", "):
                        if not (k and v):
                            continue
                        dicts[table][field][k] = v
            if not len(dicts[table][field]):
                del dicts[table][field]
        if not len(dicts[table]):
            del dicts[table]
    return dicts


def get_data():
    """
    Get the datasets into memory and perform pre-processing
    Returns:
        A dict with table name as key and the cleaned dataset as value
    """
    import datasets, utils
    data = {table: getattr(datasets, table) for table in datasets.names}
    date_columns = get_date_columns()
    for table, col in date_columns.items():
        data[table] = utils.fix_dates(getattr(datasets, table), col)
    
    dicts = utils.get_dicts()
    # TODO: use dicts to transform the data from categories to codes.
    
    return data


# TODO: write encoder for phenotypes which will generate codes and provide a 
#     dictionary that can be used to map the data
