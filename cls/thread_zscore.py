import pandas as pd
import numpy as np
import threading
import functools

class funcThread(object):
    def __init__(self,  n=5):
        self.n = n

    def __call__(self, func):
        @functools.wraps(func)
        def run(*args, **kwargs):

            threads = [None]*self.n
            container = [None]*self.n

            ####Divide Samples
            i_col = len(args[1].columns.tolist())
            contents_numb = i_col/self.n
            data_range = range(0, i_col, contents_numb)

            for i, item in enumerate(data_range):
                threads[i] = threading.Thread(target = func, args=(args[0], args[1].ix[:,item:item+contents_numb], container, i), kwargs=kwargs)
                threads[i].start()
            for i in range(len(threads)):
                threads[i].join()

            return pd.concat(container, axis=0)

        return run


class calculator(object):

    def __init__(self, df):
        if df.empty:
            raise ValueError("Input Dataframe is empty, please try with different one.")

    @funcThread(n=5)
    # function structure
    # args(input, container, thread_number , **kwargs)
    def gs_zscore(self, arr1, container, i, gene_set=[] ,form='pandas'):
        zscore=[]
        arr1_index = arr1.index.tolist()
        inter = list(set(arr1_index).intersection(gene_set))

        diff_mean = arr1.loc[inter].mean(axis=0).subtract(arr1.mean(axis=0))
        len_norm = arr1.std(ddof=1, axis=0).apply(lambda x: np.sqrt(len(inter))/x)
        zscore = diff_mean*len_norm
        zscore = zscore.to_frame()
        zscore.columns = ['Zscore']
        container[i] = zscore
        ##No Return

