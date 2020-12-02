#!/usr/bin/python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import tempfile


class CoronaData:
    """
    Import and initialise corona data.
    """
    def __init__(self, country, data):
        """
        Initialse imported corona data.

        str country: country name
        pandas dataframe data: dataframe with data
        """
        self.country = country
        self.corona_df = data
        self.corona_df['data'] = pd.to_datetime(self.corona_df['data'])
        self.corona_df.sort_values('data', inplace=True)

    @classmethod
    def from_git_italy(cls):
        """
        Import corona data for Italy from github.
        """
        tmp_dir = tempfile.TemporaryDirectory(prefix="ITA_")
        os.chdir(tmp_dir.name)
        os.system('rm -rf ./COVID-19')
        os.system('GIT_SSL_NO_VERIFY=true git clone https://github.com/pcm-dpc/COVID-19.git')
        csv_file = './COVID-19/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv'
        df = pd.read_csv(csv_file)
        return cls('ITA', df)

    @classmethod
    def from_file(cls, country, file_path):
        """
        Import corona data from a csv file.

        str country: country name to be used for labels
        str file_path: path to a csv file with columns named "data" and "totale_casi"
        """
        df = pd.read_csv(file_path)
        return cls(country, df)


class CoronaPlot:

    def __init__(self, corona_data, png_file):
        """
        Initialise variabels.

        CoronaData corona_data: corona data
        str png_file: path to a png file where the plot will be saved
        """
        self.country = corona_data.country
        self.df = corona_data.corona_df
        self.x = self.df['data']
        self.y = self.df['totale_casi']
        self.png_file = png_file

    @staticmethod
    def sigmoid_func(x, a1, b1, c1, a2, b2, c2):
        return a1*(np.exp(-(x-b1)/c1)+1)**(-1.)+a2*(np.exp(-(x-b2)/c2)+1)**(-1.)

    @staticmethod
    def sigmoid_func_inv(y, a, b, c):
        return -c*np.log(a/y-1)+b

    def _sigmoid_fit(self, fitted_days):
        x_delta = pd.to_datetime(self.x.to_numpy()) - self.x[0]
        x_fit = (x_delta.total_seconds())/86400
        param_bounds = ([100000, 1, 1., 100000, 1, 1.], [4000000, 1000, 1000., 4000000, 1000, 1000.])
        try:
            popt, pcov = curve_fit(CoronaPlot.sigmoid_func, x_fit[:fitted_days], self.y[:fitted_days], bounds=param_bounds)
        except Exception as err:
            print(err)
            print("Fit was not successful. Try other paramters.")
            return None, None
        return popt, pcov

    def plot_fit(self, fitted_days=100, ymax=2.5e6):
        """
        Fit the corona data with a double sigmoid function.
        Save and show the result.

        int fitted_days: day until which the data is fitted
        float ymax: upper y (total cases) bound in plot
        """
        popt, _ = self._sigmoid_fit(fitted_days)

        if popt is not None:

            x_func = self.x[0] + pd.to_timedelta(np.linspace(0.,fitted_days,200)*86400, unit='s')
            x_lin = np.linspace(0., fitted_days,200)
            y_fit = CoronaPlot.sigmoid_func(x_lin, *popt)

            fig, ax = plt.subplots()

            ax.plot(self.x, self.y, 'g.', label=self.country, marker='o', fillstyle='none')
            ax.plot(x_func, y_fit, 'r-', label=self.country)

            plt.gcf().autofmt_xdate()
            plt.ylim(0., ymax)
            plt.legend()
            plt.xlabel('date')
            plt.ylabel('total infected')

            plt.savefig(self.png_file)
            plt.show()


def main():
    corona_data = CoronaData.from_git_italy()
    corona_plot = CoronaPlot(corona_data, '/tmp/corona-fit.png')
    corona_plot.plot_fit(fitted_days=300)


if __name__ == "__main__":
    main()
