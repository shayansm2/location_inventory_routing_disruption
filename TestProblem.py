#%%
from tkinter import Tk
from tkinter import filedialog
import os
import numpy as np
import pandas as pd
#%%
class TestProblem(object):

    def __init__(self):

        self.select_file()

        df_facilities = pd.read_excel(self.file_directory, sheet_name = "facilities")

        self.dim_facilities = len(df_facilities)        
        self.disruption_probability  = np.array(df_facilities["q"])
        self.capacities = np.array(df_facilities["cap"])
        self.demand_threshold = np.array(df_facilities["s"])
        self.opening_cost = np.array(df_facilities["f"])
        self.ordering_cost = np.array(df_facilities["b"])
        self.inventory_cost = np.array(df_facilities["h"])
        self.purchase_cost = np.array(df_facilities["v"])

        df_customers = pd.read_excel(self.file_directory, sheet_name = "customers")
        self.dim_customers = len(df_customers)

        def fuzzy_number_generator(a,b,c):
            return (a,b,c)
        
        def expected_value_generator(a,b,c):
            return (a+b+c) / 3
        
        df_customers["demand"] = df_customers.apply(lambda x:  
                                                    fuzzy_number_generator(
                                                        x["d1"],
                                                        x["d2"],
                                                        x["d3"]), axis = 1)
        
        df_customers["expected_value_demand"] = df_customers.apply(lambda x:  
                                                    expected_value_generator(
                                                        x["d1"],
                                                        x["d2"],
                                                        x["d3"]), axis = 1)

        self.demand = np.array(df_customers["demand"])
        self.expected_value_demand = np.array(df_customers["expected_value_demand"])

        df_transport_cstmr_fclty = pd.read_excel(self.file_directory, sheet_name = "transport_cstmr_fclty")
        df_transport_cstmr_fclty.drop(columns = ["i/j"], inplace = True)
        self.transportation_customer2facility = np.array(df_transport_cstmr_fclty)

        df_transport_fclty_fclty = pd.read_excel(self.file_directory, sheet_name = "transport_fclty_fclty")
        df_transport_fclty_fclty.drop(columns = ["j/j"], inplace = True)
        self.transportation_facility2facility = np.array(df_transport_fclty_fclty)

        df_scalars = pd.read_excel(self.file_directory, sheet_name = "scalars",header=None ) 
        df_scalars.set_index(0, inplace = True)
        self.penalty_cost = df_scalars.loc["pi"].values[0]
        self.service_level = df_scalars.loc["T"].values[0]

    def select_file(self):
        
        try:
            root = Tk()
            root.withdraw()
            filename = filedialog.askopenfilename(parent=root)
        except IOError as e:
            print(e)
        self.file_directory = filename


# %%
