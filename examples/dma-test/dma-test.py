from core_axi4dmacontroller import CoreAXI4DmaController
from udmabuf import Udmabuf
import numpy as np
import random

if __name__ == '__main__':
    dma_uio_name  = 'dma-controller@60010000'
    udmabuf0_name = 'udmabuf-ddr-c0'
    udmabuf1_name = 'udmabuf-ddr-c1'
    word_type     = np.uint32
    num_words     = 1024
    num_bytes     = num_words*np.dtype(word_type).itemsize
    dma_id        = 0
    
    dma      = CoreAXI4DmaController(dma_uio_name)

    udmabuf0 = Udmabuf(udmabuf0_name)
    udmabuf1 = Udmabuf(udmabuf1_name)

    src_addr = udmabuf0.phys_addr
    dst_addr = udmabuf1.phys_addr

    print("src_addr  = 0x%08X" % src_addr)
    print("dst_addr  = 0x%08X" % dst_addr)
    
    src_buf  = udmabuf0.memmap(word_type, num_words)
    dst_buf  = udmabuf1.memmap(word_type, num_words)

    src_buf[:] = random.randint(1,255)
    dst_buf[:] = 0

    print(f"num_words = {num_words}")
    print(f"src_buf   = {src_buf}")
    print(f"dst_buf   = {dst_buf}")
    # print("intr_status = 0x%08X" % dma.irq_status(0))

    print("dma setup")
    dma.irq_on(dma_id)
    dma.setup(dma_id,1,1,num_bytes,src_addr,dst_addr)

    print("dma start")
    dma.start(dma_id)
    dma_status = dma.wait_irq(timeout=10)
    dma.irq_off(dma_id)

    if dma_status == None:
        print("dma timeout!")
    else:
        print("dma done!")
        print(f"dst_buf   = {dst_buf}")

    print("intr_status = 0x%08X" % dma.irq_status(dma_id))
    print("intr_status clear")
    dma.irq_clear(dma_id)
    print("intr_status = 0x%08X" % dma.irq_status(dma_id))
    
