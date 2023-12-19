# imports
import gspread
import pandas as pd

def importt(sh):
    """Imports the data from Google Sheet.

    Imports the latest data form the Googlesheet from my account
    Reads it into a csv format and adds 2 columns 'Date' and 'Monthly balance'
    and saves the csv locally.

    Args:
        sh: the "FM_Input" sheet inside my Google sheet using gspread.

    Returns:
        None.
    
    Raises:
        None.
    """

    # C:\Users\ganes\G\projects\Financial_manager\extract_daily.py
    mya = my_account()

    worksheet = sh.get_worksheet(0)

    # get all the records
    list_o_list = worksheet.get_all_records()

    # convert into a data frame
    df = pd.DataFrame(list_o_list)

    # Convert 'Date' column from string to Date
    df['Date'] = pd.to_datetime(df['Date'])

    # Sort rows based on date
    df = df.sort_values(by='Date', ascending=True).reset_index(drop=True)

    # Calculate monthly value
    df['Monthly_value'] = df.apply(lambda row: mya.calc_monthly_value(row['Expense'], row['Life']), axis=1).round(1)

    # Calculate Balance
    df["Balance"] = df.apply(lambda row: mya.balance_cal(row['Expense'], row['Income'], row['Account']), axis=1)

    # Save the file as csv
    df.to_csv("input_data.csv")

def exportt(sh):
    """Exports the locally transformed csv.

    Saves the locally transformed csv into the google sheet 
    by reading the entire csv and converting it into a 2 dimensional list
    and update it using gspread worksheet.update.

    Args:
        sh: The "FM_Input" google sheet using gspread.

    Returns:
        None.

    Raises:
        None.
    """

    worksheet = sh.get_worksheet(1)

    # worksheet.update('A9', [[1, 22, 121]])
    # Consider the last element - C2
    # C --> number of columns 
    # 2 --> number of rows
    # C2 -> df[2,3]
    
    re_df = pd.read_csv("input_data.csv", header=None, keep_default_na=False)
    re_df = re_df.astype(str)
    del re_df[re_df.columns[0]]

    nrows, ncols = re_df.shape
    # print(nrows, ncols)
    # worksheet.update('A2', [re_df.iloc[1].values.tolist()])
    # print([re_df.iloc[2].values.tolist()])
    list_o_list = []
    for i in range(nrows):
        # lit = 'A'+str(i)
        # print(lit)
        list_o_list.append(re_df.iloc[i].values.tolist())
        # worksheet.update('A1', [re_df.iloc[i].values.tolist()])
        # print([re_df.iloc[i].values.tolist()])
    # print(chr(65+ncols)+str(69))
    worksheet.update('A1:'+chr(65+ncols)+str(nrows), list_o_list)
    

class my_account:
    """Functions and Variables required to transform the data."""

    prev_balance = 29655
    """The balance before the first Item in the Sheet."""

    def balance_cal(self, expp, incc, accc):
        """Subtracts Expenses and Adds Income to the previous Balance.

        Args:
            expp: Current Item expense.
            incc: Current Itme income.
            accc: Current account (Bank or Cash).
        Returns:
            Integer value of current balance after caluclating the expense and income.
        """
        if accc == 'SBI Bank':
            self.prev_balance = self.prev_balance - expp + incc
        return self.prev_balance
    
    # Calculating monthly value based on life
    def calc_monthly_value(self, expense, life):
        """Calculates the Items monthly value.

        Args:
            expense: Current Item expense.
            life: Current Item Life time.
        Returns:
            Integer equalling to the monthly value of the item by considering its entire lifetime.
        """

        if life[0] != "0":
            if life[-1] == "d":
                return (30/int(life[:-1]))*expense
            if life[-1] == "M":
                return (1/int(life[:-1]))*expense
            if life[-1] == "Y":
                return ((1/int(life[:-1]))*expense)/12
        return expense

gc = gspread.service_account()
sh = gc.open("FM_input")


importt(sh)
exportt(sh)
