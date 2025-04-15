from src.utils.get_data_util import (
    get_all_locations,
    get_koivukyla,
    get_laajasalo,
    get_vallila,
)

# df = get_laajasalo()
# df = get_vallila()
# df = get_koivukyla()
df = get_laajasalo(get_2024=True)
print(df.head())
