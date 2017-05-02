import pandas as pd
import matplotlib.pyplot as plt
import os

cwd = os.getcwd()
fileName = 'assets/points.xlsx'
filePath = os.path.join(cwd, fileName)
pd.read_excel(filePath)

df = pd.read_excel(filePath, header=0)
ax = df.plot.bar(color=['r','c','b','g'])
ax.set_ylabel('Points')
plt.savefig('assets/pointTally.jpg')
