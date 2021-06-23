import pandas as pd

def save_to_csv(data,name):
    pd.DataFrame(data).to_csv(name)