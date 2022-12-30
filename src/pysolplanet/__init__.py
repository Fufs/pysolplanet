import asyncio
from aiohttp import ClientSession, web_exceptions


class Stick:
    def __init__(self, host: str, port: int = 8484) -> None:
        self.host = host
        self.port = port

        self.inverters = []


    async def async_setup(self) -> None:
        if not await self.test_connection():
            raise web_exceptions.HTTPException("Host "+self.host+" is unreachable")
        await self.discover_inverters()


    async def test_connection(self) -> bool:
        return (await self._make_request("getdev.cgi", {"device": "2"}))[0] == 200


    async def discover_inverters(self) -> list:
        self.inverters = []

        resp = await self.get_device_info(device=2)
        for inverter in resp["inv"]:
            self.inverters.append(Inverter(self, inverter["isn"], inverter["add"]))

        return self.inverters


    async def _request(self, script: str, query: dict = {}):
        qs = '&'.join([str(key)+'='+str(query[key]) for key in query])
        url = "http://" + self.host + ":" + str(self.port) + "/" + script + "?" + qs
        async with ClientSession() as session:
            async with session.get(url) as resp:
                return resp.status, await resp.json()



    async def get_wlan_info(self, info = 2):
        return (await self._make_request("wlanget.cgi", {"info": info}))[1]


    async def get_device_info(self, device = 0):
        return (await self._make_request("getdev.cgi", {"device": device}))[1]



class Inverter:
    def __init__(self, stick: Stick, sn: str, addr: int) -> None:
        self.stick = stick
        self.sn = sn
        self.addr = addr


    async def get_solar_data(self):
        return (await self.stick._make_request("getdevdata.cgi", {"device": "2", "sn": self.sn}))[1]

    # TODO: add configuration options