import requests
import pandas as pd
import os
import time

with open("stock_list.txt", "r", encoding="utf-8") as f:
    stock_list = [line.strip() for line in f if line.strip()]


def pyramid(sid):
    res = requests.get(
        "http://norway.twsthr.info/StockHolders.aspx?stock=" + sid + "&fbclid=IwAR0Hq4oVDTnoj8d-jFlomkoLIPiGFM6HiioDDaWeb-KREDwhmXZiuRCtMdk")

    dfs = pd.read_html(res.text)

    if ((dfs[1] == '查詢無此證券代號資料, 請重新查詢!').sum().sum() > 0):
        return None

    col_names = ['資料日期', '集保總張數', '總股東人數', '平均張數/人', '>400張大股東持有張數',
                 '>400張大股東持有百分比', '>400張大股東人數', '400~600張人數', '600~800張人數',
                 '800~1000張人數', '>1000張人數', '>1000張大股東持有百分比', '收盤價']

    df = dfs[9]
    data = {}

    for c in col_names:
        col_id = df[df == c].dropna(how='all', axis=0).dropna(how='all', axis=1).columns[0]
        series = df[col_id]
        row_id = series[series == c].index.values[0]
        data[c] = series[row_id:]

    df = pd.DataFrame(data).iloc[1:].dropna(how='all', axis=0)
    df['Time'] = pd.to_datetime(df['資料日期'])
    df = df.drop('資料日期', axis=1)
    df['stock_id'] = sid
    dflist = df.columns.to_list()
    NewCol = dflist[-2:] + dflist[:-2]
    Retrundf = df[NewCol]

    return Retrundf[:-1]


output_dir = 'data'
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, 'companybigpeople.csv')

if os.path.exists(output_file):
    existing_df = pd.read_csv(output_file, encoding='utf-8-sig', parse_dates=['Time'])
else:
    existing_df = pd.DataFrame()

final_df = pd.DataFrame()

for target_stock in stock_list:
    print(f"Processing stock: {target_stock}")
    mydf = pyramid(str(target_stock))

    if mydf is not None:
        if not existing_df.empty:
            merged_df = pd.merge(mydf, existing_df, on=['Time', 'stock_id'], how='left', indicator=True)
            mydf = merged_df[merged_df['_merge'] == 'left_only'].drop('_merge', axis=1)

        if not mydf.empty:
            final_df = pd.concat([final_df, mydf], ignore_index=True)
            print(f"Success fetching new data for stock: {target_stock}")
        else:
            print(f"No new data for stock: {target_stock}")
    else:
        print(f"Failed fetching data for stock: {target_stock}")

    time.sleep(5)  # 避免短時間大量存取造成問題

if not final_df.empty:
    updated_df = pd.concat([existing_df, final_df], ignore_index=True)
    updated_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Data successfully updated and saved to {output_file}")
else:
    print("No new data to update.")
