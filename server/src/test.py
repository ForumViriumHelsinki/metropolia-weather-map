import asyncio

import matplotlib.pyplot as plt
from utils.filter_tag import filter_location_with_tag, sensors_with_tag
from utils.get_data_util import get_koivukyla, get_makelankatu
from utils.utils import filter_daytime_data


async def test_func():
    # df = await get_makelankatu()
    df = await filter_location_with_tag("Mäkelänkatu", "viheralue")
    return


if __name__ == "__main__":
    asd = asyncio.run(test_func())
    # print(asd)
