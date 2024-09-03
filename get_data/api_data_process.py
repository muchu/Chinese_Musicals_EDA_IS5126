import pandas as pd
from INFO import fieids_url,columns_needed

data_dict = {}
for key in fieids_url.keys():
    data_dict[key] = pd.read_csv(f"../original_data/{key}")[columns_needed[key]]
    data_dict[key] = data_dict[key].replace(pd.NA," ")
    if key == "musicalproduces":
        new_order = ['pk','fields.title','fields.musical',  'fields.produce']
        data_dict[key] = data_dict[key][new_order]
    elif key == "theatres":
        new_order = ['pk', 'fields.name', 'fields.city']
        data_dict[key] = data_dict[key][new_order]
    elif key == "stages":
        new_order = ['pk',  'fields.name','fields.theatre', 'fields.seats']
        data_dict[key] = data_dict[key][new_order]
    

    data_dict[key].to_csv(f"../data/{key}")




