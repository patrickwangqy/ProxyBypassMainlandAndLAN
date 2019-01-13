#!/usr/bin/python3

import requests
from IPy import IP


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


def to_proxifier_config(name, ip_list):
    config_content = (f'    <Rule enabled="true">\n'
                      f'      <Name>{name}</Name>\n'
                      f'      <Targets>{"; ".join(ip_list)}</Targets>\n'
                      f'      <Action type="Direct" />\n'
                      f'    </Rule>')
    return config_content


def chunks(l, n):
    s = len(l) // n
    for i in range(0, len(l), s):
        yield l[i:i+s]


def main():
    mainland_and_lan_ips = get_mainland_and_lan_ips()
    ip_list = list(map(lambda x: IP(x).strNormal(3), mainland_and_lan_ips))
    config_content_list = []
    for index, sub_ip_list in enumerate(chunks(ip_list, 8)):
        config_content_list.append(to_proxifier_config(f'CHINA-IP-{index+1}', sub_ip_list))
    with open('proxifier_head.ppx', encoding='UTF-8') as file:
        head = file.read()
    with open('proxifier_foot.ppx', encoding='UTF-8') as file:
        foot = file.read()
    with open('bypass_mainland_and_lan_ip.ppx', 'w', newline='\n') as f:
        f.write(head)
        f.write('\n')
        f.write('\n'.join(config_content_list))
        f.write('\n')
        f.write(foot)


if __name__ == '__main__':
    main()
