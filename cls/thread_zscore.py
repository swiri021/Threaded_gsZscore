import pandas as pd
import numpy as np
import threading
import functools

class funcThread(object):
    def __init__(self):
        print "Loaded Threads"

    def __call__(self, func):
        @functools.wraps(func)
        def run(*args, **kwargs):
            print "Number of Threads : %d"%(kwargs['nthread'])

            threads = [None]*kwargs['nthread']
            container = [None]*kwargs['nthread']

            ####Divide Samples
            i_col = len(args[1].columns.tolist())
            contents_numb = i_col/kwargs['nthread']
            split_columns = [args[1].columns.tolist()[i:i+contents_numb] for i in range(0, len(args[1].columns.tolist()), contents_numb)]

            if len(split_columns)>kwargs['nthread']:
                split_columns[len(split_columns)-2] = split_columns[len(split_columns)-2]+split_columns[len(split_columns)-1]
                split_columns = split_columns[:len(split_columns)-1]

            for i, item in enumerate(split_columns):
                threads[i] = threading.Thread(target = func, args=(args[0], args[1].ix[:,item], container, i), kwargs=kwargs)
                threads[i].start()
            for i in range(len(threads)):
                threads[i].join()

            return pd.concat(container, axis=0)

        return run


class calculator(object):

    def __init__(self, df):
        if df.empty:
            raise ValueError("Input Dataframe is empty, please try with different one.")

    # Wrapper for controlling Threads
    def gs_zscore(self, arr1, nthread=5, gene_set=[]):
        return self._calculating(arr1, None, None, nthread=nthread, gene_set=gene_set)

    # function structure
    # args(input, container, thread_index , **kwargs)
    @funcThread()
    def _calculating(self, arr1, container, i, nthread=5, gene_set=[]):
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
