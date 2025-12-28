import pandas as pd

data = {
    'city': ['Bangalore', 'Mumbai', 'Delhi'],
    'store_id': ['10677', '10151', ''],
    'pincode': ['560102', '400063', '110048']
}
df = pd.DataFrame(data)
print(df)