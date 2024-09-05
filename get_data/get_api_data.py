
import requests
import pandas as pd
import tqdm

fieids_url = {
"artists" : "http://y.saoju.net/yyj/api/artist/",
"produces" : "http://y.saoju.net/yyj/api/produce/",
"musicals":"http://y.saoju.net/yyj/api/musical/",
"musicalproduces":"http://y.saoju.net/yyj/api/musicalproduces/",
"citys" : "http://y.saoju.net/yyj/api/city/",
"theatres":"http://y.saoju.net/yyj/api/theatre/", #这里的theatre要删掉location这个foreign key
"stages":"http://y.saoju.net/yyj/api/stage/",
"shows":"http://y.saoju.net/yyj/api/search_day/?date={}"
# example ：http://y.saoju.net/yyj/api/search_day/?date=2023-07-25

}

def main():
    data_dict = {}
    request_all_data(data_dict)
    data_dict["shows"] = get_shows_by_date_range("2023-01-01", "2024-09-01")
    save_all2csv(data_dict)



def request_all_data(data_dict:dict):
    for key in fieids_url.keys():
        response = requests.get(fieids_url[key])
        if response.status_code == 200:
            print(f"successfully request on {fieids_url[key]}, status code {response.status_code}.")
            data_dict[key] = pd.json_normalize(response.json())
        else:
            print(f"Error occur when requesting {fieids_url[key]}, status code {response.status_code}.")

def get_shows_by_date(date:str):
    url = fieids_url["shows"].format(date)
    response = requests.get(url)
    if response.status_code == 200:
        print(f"successfully request on {url}, status code {response.status_code}.")
        data = pd.json_normalize(response.json())
        if data["show_list"][0]:  # 检查 show_list 是否为空
            shows = pd.json_normalize(data["show_list"][0])
            shows['cast'] = shows['cast'].apply(lambda x: ' '.join([j["artist"] for j in x]))
            shows["date"] = date
            return shows
        else:
            print(f"{date} 没有演出数据。")
            return pd.DataFrame()
    else:
        print(f"Error occur when requesting {url}, status code {response.status_code}.")

def get_shows_by_date_range(start_date:str, end_date:str):
    date_range = pd.date_range(start_date, end_date)
    shows = pd.DataFrame()
    for date in tqdm.tqdm(date_range):
        shows = pd.concat([shows, get_shows_by_date(date.strftime("%Y-%m-%d"))])
    shows['date'] = pd.to_datetime(shows['date'].astype(str) + ' ' + shows['time'])
    shows = shows[["date","city","musical","cast","theatre"]]
    return shows


def save_all2csv(data_dict:dict):
    for key in data_dict.keys():
        data_dict[key].to_csv(f"../original_data/{key}")



if __name__ == "__main__":
    main()
    print("successfully get all data")

