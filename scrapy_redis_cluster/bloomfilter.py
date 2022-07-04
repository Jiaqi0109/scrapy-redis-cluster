# -*- coding: utf-8 -*-
import logging
import math
import mmh3

logger = logging.getLogger(__name__)


class BloomFilter(object):
    SEEDS = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
             107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
             227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347,
             349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
             467, 479, 487, 491, 499, 503, 509, 521, 523, 541]

    logger = logger

    def __init__(self, server, key, capacity=100000000, error_rate=1 / 100000):
        """
        Initialize BloomFilter
        :param server: Redis Server
        :param key: BloomFilter Key prefix
        :param capacity: Number of items in the filter
        :param error_rate: Probability of false positives, fraction between 0 and 1
        """
        self.server = server
        self.key = key

        self.m = math.ceil(capacity * math.log2(math.e) * math.log2(1 / error_rate))
        self.k = math.ceil(math.log1p(2) * self.m / capacity)
        if self.k > 100:
            raise ValueError('K is too big.')
        self.mem = math.ceil(self.m / 8 / 1024 / 1024)  # 需要的内存，MB
        self.blocknum = math.ceil(self.mem / 512)  # 需要多少个512M的内存块,value的第一个字符必须是ascii码，所有最多有256个内存块
        self.seeds = self.SEEDS[0:self.k]
        self.N = 2 ** 31 - 1
        logger.info(f'BloomFilter: [Size] {self.mem}Mb  [Block Number] {self.blocknum}  [K] {self.k}')

    def exists(self, value):
        """
        if value exists
        :param value:
        :return:
        """
        if not value:
            return False
        key = self.key + "_" + str(ord(value[0]) % self.blocknum)
        hashs = self.hash(value)
        exist = True
        for h in hashs:
            exist = exist & self.server.getbit(key, h)
        return exist

    def insert(self, value):
        """
        add value to bloom
        :param value:
        :return:
        """
        key = self.key + "_" + str(ord(value[0]) % self.blocknum)
        hashs = self.hash(value)
        for h in hashs:
            self.server.setbit(key, h, 1)

    def hash(self, value):
        hashs = []
        for seed in self.seeds:
            h = mmh3.hash(value, seed)
            if h >= 0:
                hashs.append(h)
            else:
                hashs.append(self.N - h)
        return hashs
