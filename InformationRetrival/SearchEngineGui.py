from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk 
from tkinter import scrolledtext
import pandas as pd;
from pandastable import Table, TableModel
from contextlib import suppress
import warnings
from IndexingComponent import IndexingDetailMethod
warnings.filterwarnings('ignore')



scraped_db = pd.read_csv('database.csv')
def new_gui():
    window = Tk()
    window.configure(bg='#0F1E9D')
    window.title("Coventry University")
    window.geometry('1100x600')
    
    lbl = Label(window, text="Search Engine",bg="#0F1E9D", font=("Arial Bold", 30), padx=5, pady=5)
    lbl.grid(column=1, row=0)
    
    lbl2 = Label(window, text="Enter your search query here ===>", bg="#0F1E9D",font=("Arial", 15), padx=5, pady=5)
    lbl2.grid(column=0, row=1)
   
    query = Entry(window,width=40)
    query.grid(column=1, row=1,  padx=5, pady=5)
    
    results = Canvas(window, height=30, width=250)
    results.grid(column=1, row=2, padx=5, pady=5)
    
    # Entry
    def getInputBoxValue():
        userInput = query.get()
        return userInput

    
    # Button
    def clicked():
        search()
        #pass
        
    def no_result():
        messagebox.showwarning("Warning", "No results found. Please try different search terms")
        
    
    def search():
        xtest = scraped_db.copy()
        q = query.get()
        f = Frame(window)
        df = IndexingDetailMethod(xtest, q)
        print(df)
        if type(df) == str:
            no_result()
        else:
            pt = Table(results)
            try:
                table = pt = Table(results, dataframe=df)
                pt.show()
            except AttributeError:
                pass
            
    def close_window():
        if messagebox.askokcancel("Quit", "Quit Programme?"):
            window.destroy()
        
    
    btn = Button(window, text="Search",bg="#0F1E9D", command=clicked)
    btn.grid(column=2, row=1)
    
    window.protocol("WM_DELETE_WINDOW", close_window)       
    window.mainloop()
new_gui()