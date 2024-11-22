from numbers_parser import Document
import pandas as pd

def transform():

    doc = Document("average_spending_2022_2024.numbers")
    sheets = doc.sheets
    tables = sheets[0].tables
    data = tables[0].rows(values_only=True)

    df = pd.DataFrame(data[1:], columns=data[0])

    # Lets first convert the date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Now lets extract the month and year for filtering purposes

    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year

    # lets also have the month name

    df['Month Name'] = df['Date'].dt.strftime('%B')

    df['Start of Month'] = df['Date'].apply(lambda x: x.strftime('%Y-%m-01'))

    return df
