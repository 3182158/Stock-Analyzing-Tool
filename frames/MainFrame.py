import requests
import pandas as pd
import tkinter as tk
from tkcalendar import DateEntry
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


class MainFrame:

    options = [
        "Stock",
        "Volume",
        "Open",
        "High",
        "Low",
        "Close"
    ]

    def __init__(self):
        self.graph_frame = None
        self.root = tk.Tk()
        self.root.geometry("800x500")
        self.root.title("Stock Analyzing Tool")

        search_frame = tk.Frame(self.root)
        search_frame.columnconfigure(0)
        search_frame.columnconfigure(1, pad=5)
        search_frame.columnconfigure(2)
        search_frame.columnconfigure(3)

        tk.Label(search_frame, text="Search", font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W, padx=1, pady=2)
        self.stock_name = tk.Entry(search_frame, font=('Arial', 13))
        self.stock_name.insert(0, 'tcs')
        self.stock_name.grid(row=0, column=1, sticky=tk.W, padx=1, pady=2)
        tk.Button(search_frame, text="Search", font=('Arial', 9), command=self.search).grid(row=0, column=2,
                                                                                            sticky=tk.W, pady=2)
        self.clicked = tk.StringVar()
        self.clicked.set("Stock")
        drop = tk.OptionMenu(search_frame, self.clicked, *self.options)
        drop.grid(row=0, column=3, sticky=tk.W, padx=1, pady=2)

        search_dates_frame = tk.Frame(self.root)
        search_dates_frame.columnconfigure(0)
        search_dates_frame.columnconfigure(1, pad=5)
        search_dates_frame.columnconfigure(2)
        search_dates_frame.columnconfigure(3, pad=5)

        tk.Label(search_dates_frame, text="Start Date", font=('Arial', 10)).grid(row=1, column=0, sticky=tk.W, padx=1,
                                                                                 pady=2)
        self.start_date = DateEntry(search_dates_frame, font=('Arial', 13))
        self.start_date.grid(row=1, column=1, sticky=tk.W, padx=1, pady=2)

        tk.Label(search_dates_frame, text="End Date", font=('Arial', 10)).grid(row=1, column=2, sticky=tk.W, padx=1,
                                                                               pady=2)
        self.end_date = DateEntry(search_dates_frame, font=('Arial', 13))
        self.end_date.grid(row=1, column=3, sticky=tk.W, padx=1, pady=2)

        search_frame.pack(fill="x", padx=5, pady=3)
        search_dates_frame.pack(fill="x", padx=5, pady=3)

        self.root.mainloop()

    def search(self):
        if self.stock_name.get() == "":
            tk.messagebox.showinfo(title="Error", message="Stock Name can be null")
        else:
            if self.graph_frame is not None:
                self.graph_frame.destroy()
            response = requests.get(f'http://127.0.0.1:5000/stock?name={self.stock_name.get()}&start={self.start_date.get_date()}&end={self.end_date.get_date()}')
            data = response.json()
            df = pd.DataFrame.from_dict(data, orient='columns')
            self.plot(df)

    def plot(self, stock_prices):
        if stock_prices.empty:
            tk.messagebox.showinfo(title="Error", message="No Data found! Check Stock name & Dates")
        else:
            self.graph_frame = tk.Frame()
            fig = Figure(figsize=(8, 4), dpi=100)
            plot1 = fig.add_subplot()
            plot1.set_xlabel("Dates")
            plot1.set_ylabel("Price")

            if self.clicked.get() == "Stock":
                up = stock_prices[stock_prices.Close >= stock_prices.Open]
                down = stock_prices[stock_prices.Close < stock_prices.Open]
                col1 = 'green'
                col2 = 'red'
                width = .3
                width2 = .03

                # Plotting up prices of the stock
                plot1.bar(up.index, up.Close-up.Open, width, bottom=up.Open, color=col1)
                plot1.bar(up.index, up.High-up.Close, width2, bottom=up.Close, color=col1)
                plot1.bar(up.index, up.Low-up.Open, width2, bottom=up.Open, color=col1)

                # Plotting down prices of the stock
                plot1.bar(down.index, down.Close-down.Open, width, bottom=down.Open, color=col2)
                plot1.bar(down.index, down.High-down.Open, width2, bottom=down.Open, color=col2)
                plot1.bar(down.index, down.Low-down.Close, width2, bottom=down.Close, color=col2)

            else:
                plot1.plot(stock_prices[self.clicked.get()])

            fig.suptitle(self.stock_name.get().upper())

            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

            # creating the Matplotlib toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.graph_frame)
            toolbar.update()

            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

            self.graph_frame.pack(fill=tk.BOTH, expand=1)
