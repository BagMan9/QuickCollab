import string
import ipaddress as ipv
import socket as sock


def get_local_ip() -> ipv.IPv4Address:
    s = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    try:
        s.connect(("1.1.1.1", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ipv.IPv4Address(ip)


def ip_word(local_ip: ipv.IPv4Address):
    value = int(local_ip) & 0xFFFFFF
    base36 = ""
    chars = string.digits + string.ascii_uppercase
    while value:
        value, remainder = divmod(value, 36)
        base36 = chars[remainder] + base36
    base36 = base36.rjust(5, "0")

    return base36


def word_ip(local_ip: ipv.IPv4Address, word: str) -> ipv.IPv4Address | ipv.IPv6Address:
    base = int(local_ip) & 0xFF000000
    remote_addr = base | int(word, 36)

    return ipv.ip_address(remote_addr)


if __name__ == "__main__":
    addr = get_local_ip()
    shortip = ip_word(addr)
    print(shortip)
    print(word_ip(addr, shortip))
