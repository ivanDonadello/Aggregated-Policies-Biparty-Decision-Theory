import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#import scipy.stats as stats
import numpy as np

pd.set_option('display.max_columns', None)  # use only to console print pandas DF
#pd.set_option('display.max_rows', None)
pd.set_option("display.precision", 3)

# AD_df = pd.read_csv('csv_policy_experiments_normal_minByPop_final.csv')
# selected_df = AD_df[['AD (bimax)','AD (-1)']][AD_df.tree_height == 4]
# print(selected_df.describe())

AD_df = pd.read_csv('../data/datasets/tree_1_population_1.csv')
#selected_df = AD_df[['AD (bimax)','AD (-1)']][AD_df.tree_height == 4]
print(AD_df.describe())

# Read CSV file into a pandas DataFrame
df = AD_df
df = df.drop('id', axis=1)
print(df.describe())

# calculate the mean, median, mode, range, variance, and standard deviation for the numerical columns
mean = df.mean()
median = df.median()
mode = df.mode()
range = df.max() - df.min()
variance = df.var()
std_dev = df.std()

# print the calculated statistics
print('Mean:\n', mean.to_frame().T)
print('\n')
print('Median:\n', median.to_frame().T)
print('\n')
print('Mode:\n', mode)
print('\n')
print('Range:\n', range.to_frame().T)
print('\n')
print('Variance:\n', variance.to_frame().T)
print('\n')
print('Standard Deviation:\n', std_dev.to_frame().T)
print('\n')


# calculate correlation coefficients between each pair of columns
corr_matrix = df.corr()

# print the correlation matrix
print('correlation: ', corr_matrix)

# create a heatmap of the correlation matrix
sns.heatmap(corr_matrix, vmin=corr_matrix.values.min(), vmax=1, square=True, cmap="coolwarm", linewidths=0.1, annot=True, annot_kws={"fontsize":8} ) #cmap='coolwarm', annot=True)

plt.title('Correlation Matrix')
plt.show()

column = '6'

sns.histplot(df[column], kde=True)

plt.title('Histogram of Column Name with Kernel Density Estimate')
plt.xlabel('Column Name')
plt.ylabel('Frequency')
plt.show()



