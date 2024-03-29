# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 23:13:11 2024

@author: maria
"""

import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns

class Covid19AnalysisTool:
    def __init__(self, master):
        self.master = master
        self.master.title("COVID-19 Analysis Tool")
        self.create_widgets()

    def create_widgets(self):
        # Create input fields and buttons
        self.label_file = tk.Label(self.master, text="Select dataset file:")
        self.label_file.pack()
        self.button_file = tk.Button(self.master, text="Browse", command=self.open_file)
        self.button_file.pack()

        self.button_clean_dataset = tk.Button(self.master, text="Clean Dataset", command=self.clean_data)
        self.button_clean_dataset.pack()

        self.label_country = tk.Label(self.master, text="Select a country for analysis:")
        self.label_country.pack()
        self.combobox_country = ttk.Combobox(self.master)
        self.combobox_country.pack()

        self.label_second_country = tk.Label(self.master, text="Select second country for analysis:")
        self.label_second_country.pack()
        self.combobox_second_country = ttk.Combobox(self.master)
        self.combobox_second_country.pack()

        self.label_analysis_type = tk.Label(self.master, text="Select analysis type:")
        self.label_analysis_type.pack()
        self.combobox_analysis_type = ttk.Combobox(self.master, values=["Time Series", "Regional and Country-Level", "Pattern Analysis", "Correlation Analysis"])
        self.combobox_analysis_type.pack()

        self.label_graph_type = tk.Label(self.master, text="Select graph type:")
        self.label_graph_type.pack()
        self.combobox_graph_type = ttk.Combobox(self.master, values=["Scatter Plot", "Line Plot", "Bar Chart", "Histogram"])
        self.combobox_graph_type.pack()

        self.label_x_axis = tk.Label(self.master, text="Select X-Axis:")
        self.label_x_axis.pack()
        self.combobox_x_axis = ttk.Combobox(self.master)
        self.combobox_x_axis.pack()

        self.label_y_axis = tk.Label(self.master, text="Select Y-Axis:")
        self.label_y_axis.pack()
        self.combobox_y_axis = ttk.Combobox(self.master)
        self.combobox_y_axis.pack()

        self.button_analyze = tk.Button(self.master, text="Analyze", command=self.analyze)
        self.button_analyze.pack()

        self.button_print_data = tk.Button(self.master, text="Print Data", command=lambda: self.print_data(graph_type=self.combobox_graph_type.get()))
        self.button_print_data.pack()

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, self.master)
        self.canvas.get_tk_widget().pack()

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx;*.xls")])
        if file_path:
            try:
                # Attempt to read CSV file
                self.dataset = pd.read_csv(file_path, parse_dates=['Date'], dayfirst=True)
            except pd.errors.ParserError:
                try:
                    # Attempt to read Excel file
                    self.dataset = pd.read_excel(file_path, parse_dates=['Date'], dayfirst=True)
                except pd.errors.XLRDError:
                    messagebox.showerror("Unsupported Format", "Unsupported file format. Please select a CSV or Excel file.")
                    return

            self.update_comboboxes()

    def update_comboboxes(self):
        self.countries = self.dataset['Country'].unique().tolist()
        self.combobox_country['values'] = self.countries
        self.combobox_second_country['values'] = self.countries

        columns = self.dataset.columns.tolist()
        self.combobox_x_axis['values'] = columns
        self.combobox_y_axis['values'] = columns

    def clean_data(self):
        # Perform basic data cleaning (you can customize this based on your dataset)
        if hasattr(self, 'dataset'):
            self.dataset = self.dataset.dropna()
            messagebox.showinfo("Data Cleaned", "Dataset cleaned successfully!")

    def analyze(self):
        country = self.combobox_country.get()
        second_country = self.combobox_second_country.get()
        analysis_type = self.combobox_analysis_type.get()
        graph_type = self.combobox_graph_type.get()

        if country:
            country_data = self.dataset[self.dataset['Country'] == country]

            if second_country:
                second_country_data = self.dataset[self.dataset['Country'] == second_country]
            else:
                second_country_data = None

            if analysis_type == "Time Series":
                self.time_series_analysis(country_data, second_country_data, graph_type)
            elif analysis_type == "Regional and Country-Level":
                self.regional_country_analysis(country_data, second_country_data, graph_type)
            elif analysis_type == "Pattern Analysis":
                self.pattern_analysis(country_data, second_country_data, graph_type)
            elif analysis_type == "Correlation Analysis":
                self.correlation_analysis(country_data, second_country_data, graph_type)

    def time_series_analysis(self, data, second_data, graph_type):
        # Implement time series analysis logic
        # For example, plotting weekly and monthly trends
        pass

    def regional_country_analysis(self, data, second_data, graph_type):
        # Implement regional and country-level analysis logic
        # For example, comparing statistics across regions or countries
        pass

    def pattern_analysis(self, data, second_data, graph_type):
        # Implement pattern analysis logic
        # For example, detecting patterns or anomalies
        pass

    def correlation_analysis(self, data, second_data, graph_type):
        # Implement correlation analysis logic
        # For example, calculating and displaying the correlation matrix
        if graph_type == "Correlation Matrix":
            correlation_matrix = data.corr()

            plt.figure(figsize=(10, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
            plt.title("Correlation Matrix")
            plt.show()

    def print_data(self, graph_type=None):
        country = self.combobox_country.get()
        second_country = self.combobox_second_country.get()
        x_axis = self.combobox_x_axis.get()
        y_axis = self.combobox_y_axis.get()

        if country and x_axis and y_axis:
            country_data = self.dataset[self.dataset['Country'] == country]

            x_values = country_data[x_axis]
            y_values = country_data[y_axis]

            # Plotting the data on the graph
            self.ax.clear()
            if graph_type == "Scatter Plot":
                self.ax.scatter(x_values, y_values, label=country)
            elif graph_type == "Line Plot":
                self.ax.plot(x_values, y_values, label=country)
            elif graph_type == "Bar Chart":
                self.ax.bar(x_values, y_values, label=country)
            elif graph_type == "Histogram":
                self.ax.hist(x_values, bins=10, alpha=0.5, label=country)

            self.ax.set_xlabel(x_axis)
            self.ax.set_ylabel(y_axis)
            self.ax.set_title(f"{country} - {x_axis} vs {y_axis}")
            self.ax.legend()

            # Redraw the canvas
            self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = Covid19AnalysisTool(root)
    root.mainloop()
