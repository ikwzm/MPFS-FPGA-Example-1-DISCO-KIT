#!/usr/bin/env ruby
# SPDX-License-Identifier: BSD-2-Clause
# Copyright (c) 2025 ikwzm

$LOAD_PATH.unshift(File.join("..", "..", "ruby", "mmapio-0.1.0", "lib"))
require 'mmapio'

if __FILE__ == $0
  core_gpio_uio  = MMapIO::Uio.new('core-gpio-uio-0')
  core_gpio_regs = core_gpio_uio.regs()
  led_pattern_1  = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02]
  led_pattern_2  = [0x41, 0x22, 0x18, 0x22]

  for i in 0..59 do
    data = led_pattern_1[i % led_pattern_1.length]
    core_gpio_regs.write_byte(0xA0, data)
    sleep(0.1)
  end
  
  for i in 0..59 do
    data = led_pattern_2[i % led_pattern_2.length]
    core_gpio_regs.write_byte(0xA0, data)
    sleep(0.1)
  end
  
  core_gpio_regs.write_byte(0xA0, 0x7F)
  
end
