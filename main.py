import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def main():
    # Копируем в массив все акции из файла
    tickers_list = []
    with open('companies.txt') as f:    
        for line in f:
            tickers_list.extend(line.split())

    # Инициализация DataFrame'ов для формирования таблиц с данными
    closes_data = pd.DataFrame(columns=tickers_list)
    dividends_data = pd.DataFrame(columns=tickers_list)
    opens_data = pd.DataFrame(columns=tickers_list)
    
    # Вычисляем диапазон дат "от" и "до"
    now = datetime.now()
    seven_years_in_days = 7 * 365
    date_from = (now - timedelta(days=seven_years_in_days)).strftime("%Y-%m-%d")
    date_to = now.strftime("%Y-%m-%d")

    # Скачиваем информацию по каждой акции и сохраняем информацию в соответствующие таблицы
    for ticker in tickers_list:
        ticker_data = yf.download(ticker, date_from, date_to, actions=True)
        
        if 'Dividends' in ticker_data:
            dividends_data[ticker] = ticker_data['Dividends'].iloc[::-1]
        if 'Close' in ticker_data:
            closes_data[ticker] = ticker_data['Close'].iloc[::-1]
        if 'Open' in ticker_data:
            opens_data[ticker] = ticker_data['Open'].iloc[::-1]


    # Сохраняем файлы
    closes_data.head()
    closes_data.to_excel("closes.xlsx")
    dividends_data.head()
    dividends_data.to_excel("dividends.xlsx")
    opens_data.head()
    opens_data.to_excel("opens.xlsx")

if __name__ == "__main__":
    main()
