core-gpio-uio
------------------------------------------------------------------------------------

### Instal Device Tree

```dts:core-gpio-uio-0.dts
/dts-v1/; /plugin/;

/ {
	fragment@0 {
		target-path = "/fabric-bus@40000000";
		#address-cells = <2>;
		#size-cells = <2>;

		__overlay__ {
			#address-cells = <2>;
			#size-cells = <2>;
			core-gpio-uio-0 {
				compatible = "generic-uio";
				reg = <0x0 0x40000100 0x0 0x0100>;
			};
		};
	};
};
```

```console
shell$ sudo ../../tools/dtbo-config --install --dts core-gpio-uio-0.dts
```

or

```console
shell$ cd examples/core-gpio-uio/
shell$ dtc -I dts -O dtb -o core-gpio-uio-0.dtb core-gpio-uio-0.dts
shell$ sudo mkdir /config/device-tree/overlays/core-gpio-uio-0
shell$ sudo cp core-gpio-uio-0.dtb /config/device-tree/overlays/core-gpio-uio-0/dtbo
```

### Run

```python:sample.py
#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-2-Clause
# Copyright (c) 2024 ikwzm

from uio import Uio
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
```

```console
shell$ cd examples/core-gpio-uio/
shell$ sudo PYTHONPATH=../../python python3 sample.py 
```

### Uninstal Device Tree 

```console
shell$ cd examples/core-gpio-uio/
shell$ sudo ../../tools/dtbo-config --remove core-gpio-uio-0
```

or

```console
shell$ sudo rmdir /config/device-tree/overlays/core-gpio-uio-0
```
