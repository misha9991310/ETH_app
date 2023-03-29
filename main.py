import asyncio
import aiohttp

ETHUSDT = 'https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT'



async def get_eth_price(session):
    async with session.get(ETHUSDT) as response:
        if response.status == 200:
            data = await response.json()
            price = float(data['price'])
            return price
        else:
            raise Exception(
                'Не удалось получить цену ETHUSDT от Binance.')


async def main():
    async with aiohttp.ClientSession() as session:
        last_price = await get_eth_price(session)

        while True:
            try:
                eth_price = await get_eth_price(session)
                price_change_percent = (float(last_price) - float(eth_price)) / float(eth_price) * 100
                if abs(price_change_percent) > 1:
                    print(f"За последний час цена изменилась на {price_change_percent:.2f}%")
                    last_price = eth_price
                await asyncio.sleep(3600)
            except Exception as e:
                print(f'Произошла ошибка: {e}')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Выход")




