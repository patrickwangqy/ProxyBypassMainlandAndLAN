// Author: iBug

function belongsToSubnet(host, list) {
  var ip = host.split(".");
  ip = 0x1000000 * Number(ip[0]) + 0x10000 * Number(ip[1]) +
    0x100 * Number(ip[2]) + Number(ip[3]);

  if (ip < list[0][0])
    return false;

  // Binary search
  var x = 0, y = list.length, middle;
  while (y - x > 1) {
    middle = Math.floor((x + y) / 2);
    if (list[middle][0] < ip)
      x = middle;
    else
      y = middle;
  }

  // Match
  var masked = ip & list[x][1];
  return (masked ^ list[x][0]) == 0;
}

var proxy = "__PROXY__";
var direct = "DIRECT";

function FindProxyForURL(url, host) {
  var remote = dnsResolve(host);
  if (belongsToSubnet(remote, WHITELIST)) {
      return direct;
  }
  return proxy;
}

// Format: [Hex IP, mask]
// e.g. 1.0.1.0/24 = [0x80008000, 0xFFFFFF00]
// Source: http://www.ipdeny.com/ipblocks/data/aggregated/cn-aggregated.zone

