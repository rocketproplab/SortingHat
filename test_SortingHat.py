import SortingHat as hat
import pandas as pd
import os

hat.sortingHat(True)

cwd = os.getcwd()
fileName = 'assets/sortingList.csv'
filePath = os.path.join(cwd, fileName)

df = pd.read_excel(filePath, header=0)
print(df['Name'])
