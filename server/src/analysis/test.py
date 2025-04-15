from src.utils.get_data_util import (
    get_all_locations,
    get_koivukyla,
    get_laajasalo,
    get_vallila,
)

# df = get_laajasalo()
# print(df.head())

df = get_koivukyla(nightime=True)
print(df.head())

# df = get_koivukyla()
# print(df.head())

# df = get_all_locations()
# print(df.head())
