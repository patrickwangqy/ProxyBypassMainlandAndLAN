#!/usr/bin/python3

import os
import requests


def get_china_ips():
    url = "http://www.ipdeny.com/ipblocks/data/aggregated/cn-aggregated.zone"
    response = requests.get(url)
    return filter(lambda x: len(x) > 0, response.content.decode("UTF-8").split("\n"))


def get_lan_ips():
    return [
        "10.0.0.0/8",
        "127.0.0.0/16",
        "129.254.0.0/16",
        "172.16.0.0/12",
        "192.168.0.0/16"
    ]


def get_mainland_and_lan_ips():
    return [*get_lan_ips(), *get_china_ips()]


def ip_to_num(s):
    return sum([int(n) * (256 ** int(e)) for e, n in enumerate(s.split(".")[::-1])])


def n_to_mask(n):
    return (2**32 - 1) >> (32 - n) << (32 - n)


def to_upper_hex(n):
    return "{:#010X}".format(n).replace("X", "x")


def read_code():
    with open("code.js") as file:
        return file.read()


def main():
    mainland_and_lan_ips = get_mainland_and_lan_ips()
    pairs = [p.split("/") for p in mainland_and_lan_ips]
    data = [(ip_to_num(s), n_to_mask(int(n))) for s, n in pairs]
    data = sorted(data, key=lambda x: x[0])

    out = ",\n".join(["  [{}, {}]".format(to_upper_hex(a), to_upper_hex(b)) for a, b in data])
    out = "var WHITELIST = [\n" + out + "\n];"

    code = read_code()
    pac = code + out
    with open("pac.txt", "w", encoding="UTF-8", newline="\n") as file:
        file.write(pac)


if __name__ == '__main__':
    main()
