import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
# %matplotlib inline
from matplotlib import cm
import seaborn as sns 
import warnings
warnings.filterwarnings("ignore")


class Visualization:
    def __init__(self,data_frame = None, location_name_list=None):
        self.data_frame = data_frame 
        self.location_name_list = location_name_list
        self.colors = ['b','r','g','p']
        self.distmapping = { 'W': 'Weekly', 'M': 'Monthly','Y':'Yearly'}
        self.cols_to_keep = [x for x in self.data_frame.columns if x not in ['InCount'+y for y in location_name_list]] 
        self.cols_to_keep = [ x for x in self.cols_to_keep if 'Weekday_' not in x and 'Month_' not in x ]
       
    def plot_graphs(self, plot_type = 'boxplot', col_name = 'InCount', nplotrows=4,nplotcols=2):
        
        location_area_index = 0
        for i in range(nplotrows):# 4 rows of plots 
            fig = plt.figure(figsize=(16,8)) 
            for j in range(nplotcols):# 2 colums of sub plots
              ax1 = fig.add_subplot(1, 2, j+1)
              if(col_name == 'InCount'):
                target_variable = col_name +self.location_name_list[location_area_index]
              else:
                target_variable = col_name                
            
              if(plot_type == 'boxplot'): 
                ax1.boxplot(self.data_frame[target_variable])
              elif(plot_type == 'histogram'):
                n, bins, patches = ax1.hist(self.data_frame[target_variable], bins=200, color=self.colors[j])
              elif(plot_type == 'heatmap'):
                cols = self.cols_to_keep.copy()
                cols.append(target_variable)
                sns.heatmap(self.data_frame[cols].corr(), annot=True, linewidths=.20)
                                        
              ax1.set_xlabel('Mall foot fall for ' + self.location_name_list[location_area_index] )
              ax1.set_ylabel('Frequency')
              ax1.set_title('Mall foot fall '+ plot_type +' for ' + self.location_name_list[location_area_index])
              location_area_index +=1
            
    def show_timedistribution(self, distribution_type='W', col_name='InCount'):
      for i in range(len(self.location_name_list)):
        if(col_name == 'InCount'):
          target_variable = col_name +self.location_name_list[i]
        else:
          target_variable = col_name
        self.data_frame[target_variable].resample(distribution_type).mean().plot(figsize = (20,8))
        
        xlabel = self.distmapping[distribution_type]
        plt.xlabel(xlabel)
        plt.ylabel('Mall Foot fall')
        plt.legend(self.location_name_list)
        plt.title("Mall Foot fall for different locations - " + xlabel)
        
    def show_pairplot(self,one_location_only = True):
      sns.set_style('whitegrid')
      cols = self.cols_to_keep
      cols.append('InCount'+self.location_name_list[0])
      sns.pairplot(self.data_frame[cols])