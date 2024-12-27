#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-2-Clause
# Copyright (c) 2024 ikwzm

import numpy as np
import mmap
import os
import glob
import re

class Uio:
    """A simple uio class"""

    @staticmethod
    def find_device_file(device_name):
        device_file = None
        r = re.compile("/sys/class/uio/(.*)/name")
        for uio_device_name_file in glob.glob("/sys/class/uio/uio*/name"):
            f = open(uio_device_name_file, "r")
            uio_device_name = f.readline().strip()
            if uio_device_name == device_name:
                m = r.match(uio_device_name_file)
                device_file = m.group(1)
            f.close()
        return device_file
        
    def __init__(self, name):
        self.name        = name
        self.device_name = Uio.find_device_file(self.name)
        self.device_file = os.open('/dev/%s' % self.device_name, os.O_RDWR | os.O_SYNC)
        self.memmap_dict = {}

    def sys_class_file_name(self, name):
        return '/sys/class/uio/%s/%s' % (self.device_name, name)

    def read_class_integer(self, name):
        file_name = self.sys_class_file_name(name)
        with open(file_name, "r") as file:
            value = file.readline().strip()
        if   value.startswith("0x") or value.startswith("0X"):
            return int(value, 16)
        elif value.isdigit():
            return int(value, 10)
        raise ValueError("Invalid value %s in %s " % (value, file_name))
        
    def get_map_addr(self, index=0):
        return self.read_class_integer('maps/map%d/addr'   % index)

    def get_map_size(self, index=0):
        return self.read_class_integer('maps/map%d/size'   % index)

    def get_map_offset(self, index=0):
        return self.read_class_integer('maps/map%d/offset' % index)

    def get_map_info(self, index=0):
        map_addr   = self.get_map_addr(index)
        map_size   = self.get_map_size(index)
        map_offset = self.get_map_offset(index)
        return dict(addr=map_addr, size=map_size, offset=map_offset)
        
    def irq_on(self):
        os.write(self.device_file, bytes([1, 0, 0, 0]))

    def irq_off(self):
        os.write(self.device_file, bytes([0, 0, 0, 0]))
        
    def wait_irq(self):
        os.read(self.device_file, 4)

    def regs(self, index=0, offset=0, length=None):
        if index in self.memmap_dict.keys():
            memmap_info = self.memmap_dict[index]
            memmap      = memmap_info['memmap']
            mmap_offset = memmap_info['offset']
            mmap_size   = memmap_info['size']
            mmap_addr   = memmap_info['addr']
        else:
            page_size   = os.sysconf("SC_PAGE_SIZE")
            map_info    = self.get_map_info(index)
            mmap_addr   = map_info['addr']
            mmap_offset = ((map_info['addr'] + map_info['offset'])        ) % page_size
            mmap_size   = ((map_info['size'] + page_size - 1) // page_size) * page_size
            memmap      = mmap.mmap(self.device_file,
                                    mmap_size,
                                    mmap.MAP_SHARED,
                                    mmap.PROT_READ | mmap.PROT_WRITE,
                                    index*page_size)
            memmap_info = {'memmap': memmap, 'size': mmap_size, 'addr': mmap_addr, 'offset': mmap_offset}
            self.memmap_dict[index] = memmap_info
        regs_offset = mmap_offset + offset
        if   length == None:
            regs_length = mmap_size - regs_offset
        elif regs_offset + length <= mmap_size:
            regs_length = length
        else:
            raise ValueError("region range error")
        return Uio.Regs(memmap, regs_offset, regs_length)

    class Regs:
        
        def __init__(self, memmap, offset, length):
            self.memmap = memmap
            self.offset = offset
            self.length = length
            self.alloc_word_array()
            self.alloc_byte_array()

        def alloc_word_array(self):
            self.word_array  = np.frombuffer(self.memmap, np.uint32, self.length>>2, self.offset)

        def read_word(self, offset):
            return int(self.word_array[offset>>2])

        def write_word(self, offset, data):
            self.word_array[offset>>2] = np.uint32(data)

        def alloc_half_array(self):
            self.half_array  = np.frombuffer(self.memmap, np.uint16, self.length>> 1, self.offset)

        def read_half(self, offset):
            return int(self.half_array[offset>>1])

        def write_half(self, offset, data):
            self.half_array[offset>>1] = np.uint16(data)

        def alloc_byte_array(self):
            self.byte_array  = np.frombuffer(self.memmap, np.uint8 , self.length>>0, self.offset)

        def read_byte(self, offset):
            return int(self.byte_array[offset>>0])

        def write_byte(self, offset, data):
            self.byte_array[offset>>0] = np.uint8(data)

