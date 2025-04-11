import asyncio

from utils.filter_tag import filter_location_with_tag, sensors_with_tag
from utils.get_data_util import get_koivukyla


async def test_func():
    # df = await get_koivukyla()
    tag_ids = await sensors_with_tag("viheralue")
    print(tag_ids)
    # asd = await filter_location_with_tag("Koivukylä", "viheralue")
    # print(filtered_df["dev-id"].unique)


if __name__ == "__main__":
    asd = asyncio.run(test_func())
    # print(asd)
