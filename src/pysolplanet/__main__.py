import asyncio
import __init__


stick = __init__.Stick(input("IP: "))

async def main():
    await stick.async_setup()
    print("Stick details")
    print(await stick.get_device_info(device = 0))
    print()
    print("Stick WLAN details")
    print(await stick.get_wlan_info(info = 2))
    print()
    print("Inverters:")
    print(await stick.get_device_info(device = 2))
    print()
    await print_all_solar_data()

async def print_all_solar_data():
    print("Solar data")
    for inverter in stick.inverters:
        print("Inverter @ "+str(inverter.addr)+" ("+inverter.sn+"): "+ str(await inverter.get_solar_data()))

asyncio.run(main())



