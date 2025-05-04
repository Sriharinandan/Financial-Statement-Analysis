import pandas as pd

class Basic:
    def __init__(self, df):
        self.df = df
    
    def display_shape(self):
        print("Dataset Shape:", self.df.shape)
    
    def summary_statistics(self):
        print("Summary Statistics:\n", self.df.describe())
    
    def missing_values(self):
        print("Missing Values:\n", self.df.isnull().sum())
    
    def data_types(self):
        print("Data Types:\n", self.df.dtypes)
    
    def main(self):
        print("\n--- Basic Data Analysis ---")
        self.display_shape()
        self.summary_statistics()
        self.missing_values()
        self.data_types() # we are going to use this module to return the basic eda of the  datafile

#Basic eda in this case refers to finding out the shape,summary stats,counting the number of missing values as well as the datatypes of all the columns in the particular dataset.