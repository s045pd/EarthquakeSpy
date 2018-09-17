import asks
import trio
import time
import json
import moment

asks.init('trio')

datas = None
with open("./earthquakes1970-2014.csv", "r") as target:
        datas = [item.split(",") for item in target.readlines()]
        print(",".join(datas[0]))
        print(",".join(datas[1]))


async def save(datas, limit):
    url = "http://127.0.0.1:8000/api/datas/"
    async with limit:
        await asks.post(url,data=datas)

async def main():
    limit = trio.CapacityLimiter(4)
    async with trio.open_nursery() as nursery:
        for item in datas[1:]:
            itemdatas = {key: item[index]
                        for index, key in enumerate(["Time",  "Latitede", "Longitude", "Deep", "Level"])}
            itemdatas['Time'] = moment.date(itemdatas['Time']).format("YYYY-MM-DDThh:mm:ss")
            itemdatas['Deep'] = int(float(itemdatas['Deep']))
            itemdatas['Address'] = ['-']
            nursery.start_soon(save,  itemdatas, limit)


if __name__ == '__main__':
    print("start")
    trio.run(main)
    print("end")




