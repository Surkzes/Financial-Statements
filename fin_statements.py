import pandas as pd
from bs4 import BeautifulSoup
import urllib.request as ur

ticker = 'TSLA'

# Opens a URL for an income statement and saves the lxml data to a variable for processing
income_st_url = 'https://finance.yahoo.com/quote/' + ticker + '/financials?'
webpage = ur.urlopen(income_st_url).read() 
soup_income = BeautifulSoup(webpage,'lxml')

# Finds all the lines with the div class and saves them to a list for further processing
sort_divs= []
for line in soup_income.find_all('div'): 
  sort_divs.append(line.string) 

# Cleans out Empty rows
new_ls = list(filter(None, sort_divs))

# Isolate the data and add extra entries for missing Categories
statement = new_ls[16:]
statement.insert(0,  'Annual')
statement.insert(6,  'Total Revenue')
statement.insert(24, 'Operating Expense')
statement.insert(36, 'Net Non Operating Interest Income Expense')
statement.insert(42, 'Other Income Expense')
statement.insert(60, 'Net Income Common Stockholders')

# Reorganizes the data in 6 columns and import into a pandas df; 
#     create an iterator from the list, move through it in blocks of 6, and zip it back together
df_buffer = list(zip(*[iter(statement)]*6))
income_statement = pd.DataFrame(df_buffer)


# This part works as intended, reindex and transpose the data to flip the rows and columns, then remove some unneccesary data
income_statement.columns = income_statement.iloc[0]
income_statement = income_statement.iloc[1:,]
income_statement = income_statement.T
income_statement = income_statement[income_statement.columns[:-5]]


# This is the attempt to reindex the second time to remove the '0' row, that is NOT working correctly
income_statement.columns = income_statement.iloc[0]
income_statement.drop(income_statement.index[0], inplace=True)
income_statement = income_statement.iloc[0:,]


# Writes table back to HTML file
#with open('temp.html', 'w') as file:
    #file.write(str())
    
print(income_statement)
