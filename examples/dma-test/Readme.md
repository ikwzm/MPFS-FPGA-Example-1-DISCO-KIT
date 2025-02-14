dma-test
------------------------------------------------------------------------------------

### Instal Device Tree

```dts:dma-test.dts
/dts-v1/; /plugin/;

/ {
	fragment@0 {
		target-path = "/fabric-bus@40000000";
		#address-cells = <2>;
		#size-cells = <2>;

		__overlay__ {
			#address-cells = <2>;
			#size-cells = <2>;
			fpgadma: dma-controller@60010000 {
				compatible = "microchip,mpfs-fpga-dma";
				reg = <0x0 0x60010000 0x0 0x1000>;
				interrupt-parent = <&plic>;
				interrupts = <120>;
				#dma-cells = <1>;
			};
			udmabuf-ddr-c0 {
				compatible = "ikwzm,u-dma-buf";
				device-name = "udmabuf-ddr-c0";
				memory-region = <&fabricbuf0ddrc>;
				size = <0x1000000>;
			};
			udmabuf-ddr-c1 {
				compatible = "ikwzm,u-dma-buf";
				device-name = "udmabuf-ddr-c1";
				memory-region = <&fabricbuf0ddrc>;
				size = <0x1000000>;
			};
		};
	};
};
```

```console
shell$ sudo ../../tools/dtbo-config --install --dts dma-test.dts
```

or

```console
shell$ cd examples/dma-test/
shell$ dtc -I dts -O dtb -o dma-test.dtb dma-test.dts
shell$ sudo mkdir /config/device-tree/overlays/dma-test
shell$ sudo cp dma-test.dtb /config/device-tree/overlays/dma-test/dtbo
```

### Run

```console
shell$ cd examples/dma-test/
shell$ sudo PYTHONPATH=../../python python3 dma-test.py
src_addr  = 0x88000000
dst_addr  = 0x89000000
num_words = 1024
src_buf   = [128 128 128 ... 128 128 128]
dst_buf   = [0 0 0 ... 0 0 0]
dma setup
dma start
dma done!
dst_buf   = [128 128 128 ... 128 128 128]
intr_status = 0x00000000
intr_status clear
intr_status = 0x00000000
```

### Uninstal Device Tree 

```console
shell$ cd examples/dma-test/
shell$ sudo ../../tools/dtbo-config --remove dma-test
```

or

```console
shell$ sudo rmdir /config/device-tree/overlays/dma-test
```


