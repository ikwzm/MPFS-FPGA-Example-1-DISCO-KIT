#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-2-Clause
# Copyright (c) 2024 ikwzm

from mmapio import Uio
import time

if __name__ == '__main__':
    core_gpio_uio  = Uio('core-gpio-uio-0')
    core_gpio_regs = core_gpio_uio.regs()
    led_pattern_1  = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02]
    led_pattern_2  = [0x41, 0x22, 0x18, 0x22]

    for i in range(60):
        data = led_pattern_1[i % len(led_pattern_1)]
        core_gpio_regs.write_byte(0xA0, data)
        time.sleep(0.1)
    for i in range(60):
        data = led_pattern_2[i % len(led_pattern_2)]
        core_gpio_regs.write_byte(0xA0, data)
        time.sleep(0.1)
    core_gpio_regs.write_byte(0xA0, 0x7F)
        
