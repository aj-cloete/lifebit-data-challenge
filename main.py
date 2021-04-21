import datasets
import utils
import pandas as pd

if __name__ == "__main__":
    data = utils.get_data()
    
    for table, df in data.items():
        print(f"Table name: {table}")
        print("Table columns:", '\n\t'.join(df.columns), sep="\n")
        print(f"Table size: rows={df.shape[0]}, columns={df.shape[1]}")
        print("\n"*2)
    
    