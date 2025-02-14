#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-2-Clause
# Copyright (c) 2024 ikwzm

from mmapio import Uio

class CoreAXI4DmaController:

    VERSION_REG_OFFSET         = 0x0000
    START_OPERATION_REG_OFFSET = 0x0004

    class Intr:
        REG_OFFSET          = 0x0010
        REG_BYTES           = 0x10
        STAT_REG_OFFSET     = 0x00
        MASK_REG_OFFSET     = 0x04
        CLEAR_REG_OFFSET    = 0x08
        EXT_ADDR_REG_OFFSET = 0x0C
        
        def __init__(self, id, regs):
            self.id     = id
            self.regs   = regs
            self.offset = self.REG_OFFSET + id * self.REG_BYTES

        def set_mask(self, mask):
            self.regs.write_word(self.offset + self.MASK_REG_OFFSET, mask)

        def get_mask(self):
            return self.regs.read_word(self.offset + self.MASK_REG_OFFSET)

        def get_status(self):
            return self.regs.read_word(self.offset + self.STAT_REG_OFFSET)

        def clear_status(self,mask=0x0F):
            self.regs.write_word(self.offset + self.STAT_REG_OFFSET, mask)

    class Desc:
        REG_OFFSET = 0x0060
        REG_BYTES  = 0x20

        class ConfigReg:
            REG_OFFSET            = 0x00
            REG_BYTES             = 0x04
            SRC_OP_SHIFT          = 0
            SRC_OP_MASK           = 0x00000003
            DST_OP_SHIFT          = 2
            DST_OP_MASK           = 0x0000000C
            CHAIN_SHIFT           = 10
            CHAIN_MASK            = 0x00000040
            EXT_DESC_SHIFT        = 11
            EXT_DESC_MASK         = 0x00000080
            INTR_ON_SHIFT         = 12
            INTR_ON_MASK          = 0x00001000
            SRC_VALID_SHIFT       = 13
            SRC_VALID_MASK        = 0x00002000
            DST_READY_SHIFT       = 14
            DST_READY_MASK        = 0x00004000
            DESC_VALID_SHIFT      = 15
            DESC_VALID_MASK       = 0x00008000
            def __init__(self, regs, offset):
                self.regs   = regs
                self.offset = offset + self.REG_OFFSET

            def get(self):
                return self.regs.read_word(self.offset)
                
            def set_op(self, src_op, dst_op, chain=0):
                config_src_op = (src_op << self.SRC_OP_SHIFT) & self.SRC_OP_MASK
                config_dst_op = (dst_op << self.DST_OP_SHIFT) & self.DST_OP_MASK
                config_chain  = (chain  << self.CHAIN_SHIFT ) & self.CHAIN_MASK
                config_word   = config_src_op | config_dst_op | config_chain
                self.regs.write_word(self.offset, config_word)
            
            def set_valid(self, desc_valid=1, src_valid=1, dst_ready=1,intr_on=1):
                config_old        = self.regs.read_word(self.offset)
                config_src_valid  = (src_valid  << self.SRC_VALID_SHIFT ) & self.SRC_VALID_MASK
                config_dst_ready  = (dst_ready  << self.DST_READY_SHIFT ) & self.DST_READY_MASK
                config_desc_valid = (desc_valid << self.DESC_VALID_SHIFT) & self.DESC_VALID_MASK
                config_intr_on    = (intr_on    << self.INTR_ON_SHIFT   ) & self.INTR_ON_MASK
                config_word       = config_old | config_src_valid | config_dst_ready | config_desc_valid | config_intr_on
                self.regs.write_word(self.offset, config_word)
            
        class ByteCountReg:
            REG_OFFSET = 0x04
            REG_BYTES  = 0x04
            def __init__(self, regs, offset):
                self.regs   = regs
                self.offset = offset + self.REG_OFFSET
            def set(self, byte_count):
                self.regs.write_word(self.offset, byte_count)
            def get(self):
                return self.regs.read_word(self.offset)

        class SrcAddrReg:
            REG_OFFSET = 0x08
            REG_BYTES  = 0x04
            def __init__(self, regs, offset):
                self.regs   = regs
                self.offset = offset + self.REG_OFFSET
            def set(self, src_addr):
                self.regs.write_word(self.offset, src_addr)
            def get(self):
                return self.regs.read_word(self.offset)
            
        class DstAddrReg:
            REG_OFFSET = 0x0C
            REG_BYTES  = 0x04
            def __init__(self, regs, offset):
                self.regs   = regs
                self.offset = offset + self.REG_OFFSET
            def set(self, dst_addr):
                self.regs.write_word(self.offset, dst_addr)
            def get(self):
                return self.regs.read_word(self.offset)
            
        class NextDescAddrReg:
            REG_OFFSET = 0x10
            REG_BYTES  = 0x04
            def __init__(self, regs, offset):
                self.regs   = regs
                self.offset = offset + self.REG_OFFSET
            def set(self, next_desc_addr):
                self.regs.write_word(self.offset, next_desc_addr)
            def get(self):
                return self.regs.read_word(self.offset)
            
        def __init__(self, id, regs):
            self.id     = id
            desc_offset = self.REG_OFFSET + id * self.REG_BYTES
            self.config_reg         = self.ConfigReg(      regs, desc_offset)
            self.byte_count_reg     = self.ByteCountReg(   regs, desc_offset)
            self.src_addr_reg       = self.SrcAddrReg(     regs, desc_offset)
            self.dst_addr_reg       = self.DstAddrReg(     regs, desc_offset)
            self.next_desc_addr_reg = self.NextDescAddrReg(regs, desc_offset)

        def setup(self, src_op, dst_op, byte_count, src_addr, dst_addr, intr_on=1):
            self.config_reg.set_op(src_op, dst_op)
            self.byte_count_reg.set(byte_count)
            self.src_addr_reg.set(src_addr)
            self.dst_addr_reg.set(dst_addr)
            self.config_reg.set_valid(desc_valid=1,src_valid=1,dst_ready=1,intr_on=intr_on)
    
    def __init__(self, uio_name, id_max=4):
        self.uio  = Uio(uio_name)
        self.regs = self.uio.regs()
        self.intr_regs = [self.Intr(i, self.regs) for i in range(id_max)]
        self.desc_regs = [self.Desc(i, self.regs) for i in range(id_max)]

    def setup(self, id, src_op, dst_op, byte_count, src_addr, dst_addr, intr_on=0):
        desc_reg = self.desc_regs[id]
        desc_reg.setup(src_op, dst_op, byte_count, src_addr, dst_addr, intr_on)

    def irq_on(self, id=0, mask=0x0F):
        intr_regs = self.intr_regs[id]
        intr_regs.set_mask(mask)
    
    def irq_off(self, id=0):
        intr_regs = self.intr_regs[id]
        intr_regs.set_mask(0)

    def irq_clear(self, id=0, mask=0x0F):
        intr_regs = self.intr_regs[id]
        return intr_regs.clear_status(mask)

    def irq_status(self, id=0):
        intr_regs = self.intr_regs[id]
        return intr_regs.get_status()

    def wait_irq(self, timeout=None):
        return self.uio.wait_irq(timeout)

    def start(self, id=0):
        regs_offset = self.START_OPERATION_REG_OFFSET
        regs_word   = 1 << id
        self.regs.write_word(regs_offset, regs_word)
