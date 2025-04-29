import json
import mimetypes
import requests
from .base import ContentConverterBase, KeyProvider, RequestDecodeError
from loguru import logger as log

class JsonConverter(ContentConverterBase):
    supports_keys = True
    mime_type = mimetypes.types_map[".json"]

    def get_button_text(self, provider: KeyProvider, response: requests.Response):
        j = None
        try:
            j = json.loads(response.text)
            log.debug("conv json: {0} \n conv keys: {1}",j,provider.keys )
        except json.decoder.JSONDecodeError as e:
            raise RequestDecodeError(e) from e
        return JsonConverter.get_value(j, provider.keys)

    @staticmethod
    def get_value(j: dict | None, keys: str):
        if j:
            for key in keys.split('.'):
                j = j.get(key)
                if not j:
                    return None
        return j
