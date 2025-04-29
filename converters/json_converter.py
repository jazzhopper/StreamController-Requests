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
            j = {k.replace(' ', '_'): v for k, v in j.items()}
            log.debug("conv_json: {0} \n conv keys: {1}",j,provider.keys )
        except json.decoder.JSONDecodeError as e:
            raise RequestDecodeError(e) from e
        result = JsonConverter.get_value(j, provider.keys)
        log.debug("conv result: {0}",result)
        return result

    @staticmethod
    def get_value(j: dict | None, keys: str):
        if j:
            log.debug("conv get_value: {0} \ keys: {1}",j, keys )
            for key in keys.split('.'):
                log.debug("conv get_value: {0} \ key: {1}",j, key )
                j = j.get(key)
                if not j:
                    return None
        return j
