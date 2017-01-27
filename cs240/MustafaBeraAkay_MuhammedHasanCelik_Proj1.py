import thinkstats2
import pandas as ps
import thinkplot as tplot
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy import stats
import random


class PARTI:

    def __init__(self):
        self.df = PARTI._read_file()

    def plotHistogram(self):
        self.df.sum(axis=0).plot.bar()
        plt.show()

    def plotCategory(self, category, start_year, end_year):
        hist_years = self._get_hist_by_year(category, start_year, end_year)
        ps.Series(dict(hist_years)).plot.bar()
        plt.show()

    def findOutlier(self, category, start_year, end_year):
        hist_years = self._get_hist_by_year(category, start_year, end_year)
        return (
            min(hist_years, key=lambda x: x[1])[1],
            max(hist_years, key=lambda x: x[1])[1]
        )

    def mean(self, category):
        return sum(self.df[category]) / float(len(self.df[category]))

    def variance(self, category):
        vrn = sum(map(
            lambda x: (self.mean(category) - x)**2, self.df[category]
        )) / float(len(self.df[category]))
        return (vrn, math.sqrt(vrn))

    @staticmethod
    def _read_file():
        '''
            This static function readfiles and selects necessary rows.
            return: pandas dataframe
        '''
        table = list()
        f = open('wine.txt')
        header = f.readline().strip().split('\t')[1:]
        for i in f:
            row = i.strip().split('\t')
            if len(row) > 2:
                table.append(map(int, row[1:]))
            else:
                break
        return ps.DataFrame(table, columns=header)

    def _get_hist_by_year(self, category, start_year, end_year):
        years = {
            (i / 12 + 1980): sum(self.df[category][i:i + 3])
            for i in range(0, len(self.df[category]), 12)
        }.items()
        return filter(lambda x: end_year >= x[0] >= start_year, years)


class PARTII:

    def generate(self):
        pmf = thinkstats2.Pmf(np.random.rand(1000))
        tplot.Pmf(pmf)
        tplot.Cdf(thinkstats2.MakeCdfFromPmf(pmf))
        tplot.Show()

    def PMF(self, list_of_int=range(1, 7)):
        X = [PARTII._choose_until_four(list_of_int) for i in range(10000)]
        tplot.Hist(thinkstats2.Pmf(X))
        tplot.Show()

    def CDF(self, list_of_int=range(1, 7)):
        X = [PARTII._choose_until_four(list_of_int) for i in range(10000)]
        tplot.Cdf(thinkstats2.Cdf(X))
        tplot.Show()

    def findDefective(self):
        books = ps.read_csv('Book2.csv')
        X = [PARTII._book_experiment(books) for i in range(100)]
        pmf = thinkstats2.Pmf(X)
        tplot.Pmf(pmf)
        cdf = thinkstats2.MakeCdfFromPmf(pmf)
        tplot.Cdf(cdf)
        tplot.Show()

        # percentiles and percentile ranks calculaition for all book.
        ranks = map(cdf.PercentileRank, X)
        pers = map(cdf.Percentile, ranks)
        return (ranks, pers)

    @staticmethod
    def _book_experiment(books):
        num_try = 1
        samp = books.sample(3)
        while not all((samp['PART_ID'] > 10) & (samp['PART'] == 'D')):
            num_try += 1
            samp = books.sample(3)
        return num_try

    @staticmethod
    def _choose_until_four(list_of_int):
        num_try = int()
        rand_choose_nums = list()
        while 4 not in rand_choose_nums:
            num_try += 1
            rand_choose_nums.append(random.choice(list_of_int))
        return num_try
