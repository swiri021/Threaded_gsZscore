# Threaded_gsZscore
Threaded Gene-set Zscore(Or Pathway Score) by using decorator.
# Reference
[Pathway and gene-set activation measurement from mRNA expression data: the tissue distribution of human pathways](https://genomebiology.biomedcentral.com/articles/10.1186/gb-2006-7-10-r93)

# Example :
```Python
import pandas as pd
from cls.thread_zscore import calculator

####Load example
df = pd.read_csv('Input_Example/Example.csv', index_col=0)
df.index = df.index.astype(int).astype(str)


#### Init Class and check input file
zscore_calculator = calculator(df)

#### Input list should be EntrezIDs(Pathways)
result = zscore_calculator.gs_zscore(nthread=4, gene_set=['9480', '367', '2137'])
print result
```
