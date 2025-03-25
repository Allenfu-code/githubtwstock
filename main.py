import requests
import pandas as pd
import os
from datetime import datetime
import time

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
    today = datetime.today().strftime('%Y%m%d')

    with open("stock_list.txt", "r", encoding='utf-8') as f:
        stock_list = [line.strip() for line in f if line.strip()]

    for stock_no in stock_list:
        price = get_stock_price(stock_no)
        broker_df = get_broker_data(stock_no, today)

        if price and broker_df is not None:
            broker_df['收盤價'] = price
            broker_df['日期'] = today

            output_file = f"data/{stock_no}.csv"

            if os.path.exists(output_file):
                existing_df = pd.read_csv(output_file)
                existing_dates = set(existing_df['日期'].astype(str).values)
                if today in existing_dates:
                    print(f"股票 {stock_no} 日期 {today} 已存在資料中，不進行新增。")
                else:
                    updated_df = pd.concat([existing_df, broker_df], ignore_index=True)
                    updated_df.to_csv(output_file, index=False, encoding='utf-8-sig')
                    print(f"股票 {stock_no} 資料儲存成功：{output_file}")
            else:
                broker_df.to_csv(output_file, index=False, encoding='utf-8-sig')
                print(f"股票 {stock_no} 資料儲存成功：{output_file}")
        else:
            print(f"股票 {stock_no} 今天資料未取得，請確認後再試")
        time.sleep(5)
        
