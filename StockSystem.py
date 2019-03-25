import tkinter as tk
import random
from tkinter.font import Font
import sys
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import matplotlib.pyplot as plt
root = tk.Tk()
# width x height + x_offset + y_offset:
root.geometry("570x300+30+30")

w = tk.Label(root,text="Welcome to OptionData Web Cleaner System!")
w1 = tk.Label(root, text="what we can do is giving you a convenient platform \n to select your interested stocks!")
w2 = tk.Label(root, text="we can help you download and clean option data! ")
w3 = tk.Label(root,text="We have 25,000 companies for you to pick, what's more")
w4 = tk.Label(root,text=" we can help you separate it into European option data & nonEuropean option data\n")
w5 = tk.Label(root,text="\n please choose which selection you want:")
w.pack()
w1.pack()
w2.pack()
w3.pack()
w4.pack()
w5.pack()

def slefselect():
    window = tk.Tk()
    t1 = tk.Text(window)
    t1.pack()

    class PrintToT1(object):
        def write(self, s):
            t1.insert(tk.END, s)

    sys.stdout = PrintToT1()
    print('Hello, world!')
    print("Isn't this fun!")

# random selection function
def randomselect():
    window = tk.Toplevel(root)


companycodecollect = list()
def company_codecollect(company_code):
    companycodecollect.append(company_code)
    print(companycodecollect)
#clean data function:

def Cleandata(df):
    #based on company code to select from datacollection.csv
    df = pd.read_csv('cleanData.csv', index_col=0)
    names = df['Code'].unique().tolist()
    data_stock = df.loc[df['Code'] == 'PIH']
    df1 = data_stock.set_index('Date')
    df2 = df1.drop(['Code', 'Volume'], axis=1)
    df2 = df2.astype(float, errors='ignore')
    df3 = df1['Volume']
    df4 = df3.astype(float, errors='ignore')
    fig, axes = plt.subplots(nrows=2)
    df.plot(ax=axes[0])
    axes[0].legend(loc='upper right')
    df.plot(ax=axes[1])
    plt.legend(loc=1)
    plt.show()

def data_summary(syml):
    data_stock = df.loc[df['Code'] == syml]
    df1 = data_stock.set_index('Date')
    df2 = df1.astype(float, errors='ignore')
    datasummary = df2.describe(percentiles=[])
    print('Mean: ', df1.mean().values)
    print(datasummary)
    # return data_summary
    # vis_stock('PIH')
data_summary('PIH')

import pandas as pd
dataframe = pd.read_csv("merge.csv")

def implied_vol(dataframe_clean):
    pass

def clean(dataframe):
    dataframe = dataframe.rename(columns = {'7':'Code'})
    # drop duplicates
    dataframe_dupl = dataframe.drop_duplicates()
    # clean NAN
    dataframe_clean = dataframe_dupl.dropna()
    # clean outliers
    dataframe_iv = implied_vol(dataframe_clean)
    df = dataframe_iv[dataframe_iv["implied vol"]>= 2]
    return dataframe_clean

df = clean(dataframe)
df.to_csv('cleanData.csv')

# web reader function:
def webreader(compancodecollect):
    s_date = '7/1/2015'
    e_date = '7/31/2015'
    # citi = web.DataReader('CIT', data_source='yahoo', start=s_date, end=e_date)
    # df=pd.read_csv('NBOption.csv')
    window=tk.Tk()
    window.geometry("570x500+30+30")
    t1=tk.Text(window)

    t2label = tk.Label(window, text ="Advanced Selection \n you can select company based on indusrty type:")
    cleanbutton = tk.Button(window,text ="Clean & Visualization", command=lambda : Cleandata(df), width=300)
    t2label.pack()
    t1.pack()
    cleanbutton.pack()
    class PrintToT1(object):
        def write(self, s):
            t1.insert(tk.END, s)

    sys.stdout = PrintToT1()
    print('There is the stock information of company you selected:')
    for i in range(len(compancodecollect)):
        df = web.DataReader(str(compancodecollect[i]), data_source='yahoo', start=s_date, end=e_date)
        print(df)


def advancedselect():
    window = tk.Tk()
    window.title("Advanced Selection")
    window.geometry("570x500+30+30")

    tk.Label(window, text="Advanced Selection \n you can select company based on indusrty type:").grid(row=0, sticky=tk.W)
    tk.Label(window, text="\n IT industry:").grid(row=2, sticky=tk.W)

    tk.Checkbutton(window, text='Google Company',command=lambda :company_codecollect('PIH')).grid(row=(3), sticky=tk.W)
    tk.Checkbutton(window, text='Facebook Company',command=lambda :company_codecollect('FB')).grid(row=(4), sticky=tk.W)
    tk.Checkbutton(window, text='Micosoft Company',command=lambda :company_codecollect('MSFT')).grid(row=(5), sticky=tk.W)
    tk.Checkbutton(window, text='Apple Company',command=lambda :company_codecollect('APPL')).grid(row=(6), sticky=tk.W)

    tk.Label(window, text="Bank industry:").grid(row=2, sticky=tk.E)
    tk.Checkbutton(window, text='citiy bank',command=lambda :company_codecollect('CIT')).grid(row=(3),sticky=tk.E)
    tk.Checkbutton(window, text='Chase bank',command=lambda :company_codecollect('GOOG')).grid(row=(4),sticky=tk.E)
    tk.Checkbutton(window, text='BOA',command=lambda :company_codecollect('GOOG')).grid(row=(5),sticky=tk.E)
    tk.Checkbutton(window, text='jjj',command=lambda :company_codecollect('GOOG')).grid(row=(6),sticky=tk.E)


    tk.Button(window, text="submit", command=lambda :webreader(companycodecollect)).grid(row=9,pady=4)

    tk.mainloop()

button1 = tk.Button(root,text='Self Select',command=slefselect)
button1.place(x=125, y=180 + 1 * 30, width=320, height=25)

button2 = tk.Button(root,text='Randomly Select 2000 tickers', command=randomselect)
button2.place(x=125, y=180 + 2 * 30, width=320, height=25)

button3 = tk.Button(root,text='Advanced Select',command=advancedselect)
button3.place(x=125, y=180 + 3 * 30, width=320, height=25)

root.mainloop()