# !/usr/bin/python3
# -*- coding:utf-8 -*-
import proxy_sites


def run():
    proxy_sites.register_all()
    for s in proxy_sites.sites.values():
        for p in s.yield_proxy():
            print(p)


if __name__ == '__main__':
    run()
