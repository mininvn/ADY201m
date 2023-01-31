import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("dulieuxettuyendaihoc.csv", header = 0, delimiter = ",", encoding = 'unicode_escape')

a = df

df.head(10)

df.tail(10)

df.columns

# datatypes
df.dtypes

# data size
df.shape

# RangeIndex(start=0, stop=100, step=1)
df.index

# includes RangeIndex, dtype and non-null count of columns, memory usage
# df.info()

# remove null data
df.dropna(how = 'all')

# remove duplicated rows
df.drop_duplicates()

# fill null cell with value
df.fillna('Unknown')

# create new col
df['TBDH'] = (df['DH1'] + df['DH2'] + df['DH3'])/3

# headmap to visualize data
plt.figure(figsize=(10, 6))
sns.heatmap(df.isna().transpose(), cmap = "YlGnBu", cbar_kws = {'label': 'missing data'})
plt.savefig('./generated/missingdata.png', dpi = 100)

# get specified cols, return a data frame
df_dh = df[['DH1', 'DH2', 'DH3', 'TBDH', 'KV', 'KT']]

# get specified rows by range, return a data frame, excluded
df[2:5]

# get specified row by name
df.loc[2]

# get specified rows by range, return a data frame, included
df.loc[2:4]

# get specified rows and columns, return a data frame
df.loc[2:4, ['DH1', 'DH2', 'DH3', 'KT']]

# get specified row by index
df.iloc[2]

# get specified rows by range, return a data frame, excluded
df.iloc[2:4]
df.iloc[:5]
df.iloc[95:]

# get specified rows and columns by range, return a dataframe, excluded
df.iloc[2:5,1:5]

# sort data
df.sort_values(by = ['DH1', 'DH2'], ascending = [True, False])

# get data by conditions
df[df['KT'] == 'C']
df[(df['DH1'] > 5) & (df['DH2'] > 5)]

# modify data by conditions
df.loc[df['TBDH'] < 5, 'KETQUA'] = 'FAIL'
df.loc[df['TBDH'] >= 5, 'KETQUA'] = 'PASS'

# aggregate
df_dh.aggregate({'DH1': ['sum', 'mean'], 'DH2': ['min', 'max'], 'DH3': ['mean', 'max']})

# group by
df_dh.groupby('KV')['KV'].agg(['count'])
df_dh.groupby('KV')['DH1'].agg(['min', 'mean', 'std', 'max'])

a = pd.pivot_table(df, values = ['DH1', 'DH2', 'DH3'], columns = 'KETQUA', aggfunc = ['min', 'mean', 'max'])

print(a)