import requests
import pandas as pd
from datetime import datetime, timedelta

def get_stock_price(stock_no):
    url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stock_no}.tw"
    resp = requests.get(url).json()
    if resp['msgArray']:
        data = resp['msgArray'][0]
        return data['z']  # 收盤價
    else:
        return None

def get_broker_data(stock_no, date):
    url = f"https://www.twse.com.tw/fund/T86?response=json&date={date}&selectType=ALLBUT0999"
    resp = requests.get(url).json()
    if resp['stat'] == "OK":
        df = pd.DataFrame(resp['data'], columns=resp['fields'])
        df_stock = df[df['證券代號'] == stock_no]
        return df_stock
    return None

if __name__ == "__main__":
    stock_no = "2330"
    # today = datetime.today().strftime('%Y%m%d')
    today = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')
    price = get_stock_price(stock_no)
    broker_df = get_broker_data(stock_no, today)

    # 整理並儲存資料
    if price and broker_df is not None:
        broker_df['收盤價'] = price
        broker_df['日期'] = today
        broker_df.to_csv(f"data/{stock_no}_{today}.csv", index=False, encoding='utf-8-sig')
        print("資料取得並儲存完成！")
    else:
        print("今天資料未取得，請確認後再試")
