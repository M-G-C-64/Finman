# imports
import gspread
import pandas as pd
    
import pandasql as ps
import plotly.express as px
import plotly.io as pio


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

    # bring balance column to 4th index
    balance_df = df.pop("Balance")
    df.insert(1, 'Balance', balance_df)

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
    worksheet.clear()

    # worksheet.update('A9', [[1, 22, 121]])
    # Consider the last element - C2
    # C --> number of columns 
    # 2 --> number of rows
    # C2 -> df[2,3]
    
    re_df = pd.read_csv("input_data.csv", header=None, keep_default_na=False)
    re_df = re_df.astype(str)
    del re_df[re_df.columns[0]]
    # re_df = re_df

    nrows, ncols = re_df.shape
    # print(nrows, ncols)
    # worksheet.update('A2', [re_df.iloc[1].values.tolist()])
    # print([re_df.iloc[2].values.tolist()])
    list_o_list = []
    for i in range(1,nrows):
        # lit = 'A'+str(i)
        # print(lit)
        list_o_list.append(re_df.iloc[i].values.tolist())
        # worksheet.update('A1', [re_df.iloc[i].values.tolist()])
        # print([re_df.iloc[i].values.tolist()])
    # print(chr(65+ncols)+str(69))
    list_o_list.append(re_df.iloc[0].values.tolist())
    worksheet.update('A1:'+chr(65+ncols)+str(nrows), list_o_list[::-1])
    # graphs(re_df)
    

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

# gc = gspread.service_account()
# sh = gc.open("FM_input")


# importt(sh)
# exportt(sh)

def graphs():


    re_df = pd.read_csv("input_data.csv")
    del re_df[re_df.columns[0]]
    re_df['Date'] = pd.to_datetime(re_df['Date'])
    re_df['Date'] = re_df['Date'].dt.date
    print(re_df.head())
    def saveimg(fig, i):
        fig.update_layout(yaxis = dict(showgrid=True, gridwidth=1, gridcolor='gray'), height=400, width=1200)
        pio.write_image(fig, 'static/'+str(i)+'.png')

    

    # q1 = "SELECT Date, sum(Expense) as daily_expense FROM re_df group by Date"
    q2 = "SELECT Location, sum(Expense) as location_expense FROM re_df group by Location"
    q3 = "SELECT Platform, sum(Expense) as platform_expense FROM re_df where Platform NOT IN ('Amazon') group by Platform"
    q4 = "SELECT Item, sum(Expense) as item_Expense FROM re_df where Item NOT IN ('Cheeti Paata', 'PG Rent', 'Realme Narzo 60x', 'PG Advance', 'Salary', 'Borrow', 'PG Advance Refund') group by Item"
    q5 = "SELECT Recursive, sum(Expense) as Recursive_expense FROM re_df group by Recursive"
    q6 = "SELECT Recursive, sum(Expense) as Recursive_expense, sum(Income) as Recursive_income FROM re_df group by Recursive"
    q7 = "SELECT Type, sum(Expense) as type_expense FROM re_df group by Type"
    q8 = "SELECT Item, Monthly_value FROM re_df where Item NOT IN ('Cheeti Paata', 'PG Rent', 'PG Advance', 'Salary', 'Borrow', 'PG Advance Refund') group by Item"
    q9 = "SELECT Recursive, sum(Monthly_value), sum(Income) as Recursive_income FROM re_df group by Recursive"
    q10 = "SELECT Date, min(Balance) as Balance FROM re_df group by Date"

    # fig1 = px.bar(ps.sqldf(q1, locals()), x='Date', y='daily_expense')
    fig2 = px.bar(ps.sqldf(q2, locals()), x='Location', y='location_expense')
    fig4 = px.bar(ps.sqldf(q4, locals()), x='Item', y='item_Expense', color="item_Expense", color_continuous_scale=["cyan", "blue", "violet", "purple"])
    fig3 = px.bar(ps.sqldf(q3, locals()), x='Platform', y='platform_expense', color="Platform")
    fig5 = px.bar(ps.sqldf(q5, locals()), x='Recursive', y='Recursive_expense', color='Recursive')
    fig6 = px.bar(ps.sqldf(q6, locals()), x='Recursive', y=['Recursive_income', 'Recursive_expense'], barmode='group')
    fig8 = px.bar(ps.sqldf(q8, locals()), x='Item', y='Monthly_value', color="Monthly_value", color_continuous_scale=["cyan", "blue", "violet", "purple"])
    fig7 = px.bar(ps.sqldf(q7, locals()), x='Type', y='type_expense', color='Type')
    fig9 = px.bar(ps.sqldf(q9, locals()), x='Recursive', y=[ 'Recursive_income','sum(Monthly_value)'], barmode = 'group')
    fig10 = px.line(ps.sqldf(q10, locals()), x='Date', y='Balance')

    for i in range (1, 11):
        if 'fig'+str(i) in locals():
            exec("saveimg(locals()['fig'+str(i)], i)")
            
    
def custom_graphs(q1, x_axis, y_axis, color=None, barmode=None, color_continuous_scale= None):
    print("inside custom_graphs")
    
    re_df = pd.read_csv("input_data.csv")
    del re_df[re_df.columns[0]]
    re_df['Date'] = pd.to_datetime(re_df['Date'])
    re_df['Date'] = re_df['Date'].dt.date
    print(re_df.head())

    fig = px.bar(ps.sqldf(q1, locals()), x = x_axis, y= y_axis )
    fig.update_layout(yaxis = dict(showgrid=True, gridwidth=1, gridcolor='gray'), height=400, width=1200)
    pio.write_image(fig, 'static/'+'1'+'.png')
