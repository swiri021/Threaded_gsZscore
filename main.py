import pandas as pd
from cls.thread_zscore import calculator

####Load example
df = pd.read_csv('Input_Example/Example.csv', index_col=0)
df.index = df.index.astype(int).astype(str)

#### Init Class and check input file
zscore_calculator = calculator(df)

#### Input list should be EntrezIDs
result = zscore_calculator.gs_zscore(df, gene_set=['9480', '367', '2137'])