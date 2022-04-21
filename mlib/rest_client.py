class Client:
    def __init__(self, cfg: dict) -> None:
        self._url = cfg.get("url")
        self._headers = {
            "apikey": cfg.get("apikey"),
            "Authorization": f"Bearer {cfg.get('token')}"
        }

    async def api_call(self, path: str, method: str = "GET", **kwargs):
        import aiohttp
        async with aiohttp.ClientSession(headers=self._headers) as _session:
            async with _session.request(method, f"{self._url}/{path}", json=kwargs) as r:
                try:
                    r.raise_for_status()
                    return await r.json()
                except Exception as ex:
                    from .logger import log
                    log.exception(r.content._buffer)
                    return 0
