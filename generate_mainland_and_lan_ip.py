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


def main():
    mainland_and_lan_ips = get_mainland_and_lan_ips()
    with open("china_ips.txt", "w", encoding="UTF-8", newline="\n") as file:
        file.write('\n'.join(mainland_and_lan_ips))


if __name__ == '__main__':
    main()
