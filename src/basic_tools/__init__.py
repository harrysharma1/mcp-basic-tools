import base64
import codecs
from datetime import datetime
import hashlib
import html
import json
import random
import uuid
from zoneinfo import ZoneInfo
from urllib.parse import quote, unquote 

from fastmcp import FastMCP
mcp = FastMCP("Basic Tools")


@mcp.tool
def get_current_time (format: str, tz: str = "Europe/London"):
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
            return quote(text)
        case "url_decode":
            return unquote(text)
        case "html_encode":
            return html.escape(text)
        case "html_decode":
            return html.unescape(text)
        case _:
            return text

@mcp.tool
def generate_random_numbers(
        min_val: float = 0, 
        max_val: float = 100,
        count: int = 1,
        precision: int = 2,
        unique: bool = False, 
        distribution: str = "uniform"):
    res = []
    gen_set = set()

    if min_val > max_val:
        raise ValueError("min cannot be greater than max")
    if not (1 <= count <= 100):
        raise ValueError("count must be between 1 and 100")
    if not (0 <= precision <= 10):
        raise ValueError("precision must be between 0 and 10")

    max_attempts = count * 1000
    attempts = 0

    while len(res) < count and attempts < max_attempts:
        attempts += 1
        val = None

        match distribution:
            case "uniform":
                val = random.uniform(min_val, max_val)
            case "gaussian":
                mean = (min_val + max_val) / 2
                std_dev = (max_val - min_val) / 4 if max_val != min_val else 1.0

                candidate = random.gauss(mean, std_dev)
                if min_val <= candidate <= max_val:
                    val = candidate
            case "exponential":
                r_width = max_val - min_val
                lamd = 1.0 / (r_width / 2) if r_width > 0 else 1.0

                candidate = min_val + random.expovariate(lamd)
                if candidate <= max_val:
                    val = candidate
            case "triangular":
                val = random.triangular(min_val, max_val, (min_val + max_val)/ 2)
            case _:
                raise ValueError(f"Unsupported distribution: {distribution}")
        if val is not None:
            val = round(val, precision)
            if precision == 0:
                val = int(val)

            if unique:
                if val not in gen_set:
                    gen_set.add(val)
                    res.append(val)
            else:
                res.append(val)
        if unique and len(res) < count:
            raise RuntimeError("Could not generate enough unique numbers within range")

        return res

@mcp.tool
def generate_uuid(
        count: int = 1,
        uppercase: bool = False,
        include_braces: bool = False,
        strip_hyphens: bool = False
        ):
    if not (1 <= count <= 100):
        raise ValueError("count must be between 1 and 100")
    if strip_hyphens and include_braces:
        raise ValueError("cannot stip hyphens and include braces at the same time")

    res = []
    for _ in range(count):
        u = str(uuid.uuid4())
        if uppercase:
            u = u.upper()
        if include_braces:
            u = "{" + u + "}"
        if strip_hyphens:
            u = u.replace("-", "")
        res.append(u)
    return res

@mcp.tool
def generate_hash(
    text: str,
    algorithm: str = "sha256",
    uppercase: bool = False
    ):
    ret_hash = None
    match algorithm:
        case "md5":
            ret_hash = hashlib.md5(text.encode("utf-8")).hexdigest()
        case "sha1":
            ret_hash = hashlib.sha1(text.encode("utf-8")).hexdigest()
        case "sha256":
            ret_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        case "sha512":
            ret_hash = hashlib.sha512(text.encode("utf-8")).hexdigest()
        case _:
            raise ValueError("algorithm is empty or invalide")

    if uppercase:
        return ret_hash.capitalize()

    return ret_hash

@mcp.tool
def format_json(
        json_string: str,
        indent: int = 2,
        sort_keys: bool = False,
        compact: bool = False,
        escape_unicode: bool = False
        ):
    try:
        parsed = json.loads(json_string)
    except json.JSONDecodeError as err:
        return f"invalid json: {err}"

    if compact or indent == 0:
        return json.dumps(parsed, separators=(",", ":"), ensure_ascii=escape_unicode, sort_keys=sort_keys)

    effective_indent = indent if indent in (2,4) else 2
    return json.dumps(parsed, indent=effective_indent, ensure_ascii=escape_unicode, sort_keys=sort_keys)


def main() -> None:
    mcp.run()
