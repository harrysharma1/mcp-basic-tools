import base64
import binascii
from codecs import decode
import codecs
from datetime import datetime
from zoneinfo import ZoneInfo

from fastmcp import FastMCP
mcp = FastMCP("Basic Tools")


@mcp.tool
def get_current_time (tz: str, format: str):
    current_time = datetime.now(ZoneInfo(tz))
    return current_time.strftime(format)

@mcp.tool
def convert_encoding(text: str, operation: str):
    match operation:
        case "text_to_binary":
            return "".join(format(ord(char), '08b') for char in text)
        case "binary_to_text":
            decimal_value= int(text, 2)
            num_bytes  = (decimal_value.bit_length() + 7) // 8
            return decimal_value.to_bytes(num_bytes, "big").decode("utf-8")
        case "text_to_hex":
            return text.encode().hex()
        case "hex_to_text":
            return codecs.decode(text, 'hex').decode('utf-8')
        case "text_to_base64":
            return base64.b64encode(text.encode()).decode()
        case "base64_to_text":
            return base64.b64decode(text).decode()
        case "url_encode":
            pass
        case "url_decode":
            pass
        case "html_encode":
            pass
        case "html_decode":
            pass
        case _:
            return text
def main() -> None:
    print("Hello from basic-tools!")
