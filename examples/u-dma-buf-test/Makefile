
TEST_PROGRAM_LIST = u-dma-buf-test        \
                    u-dma-buf-direct-test \
                    u-dma-buf-ioctl-test  \
                    u-dma-buf-file-test   \
                    $(END_LIST)

TEST_DEVICE_LIST  = udmabuf-fabric-low    \
                    udmabuf-fabric-high   \
                    udmabuf-soc-high      \
                    udmabuf-ddr-c0        \
                    udmabuf-ddr-nc0       \
                    udmabuf-ddr-nc-wcb0   \
                    $(END_LIST)

U_DMA_BUF_FILE_TEST_LOG= u-dma-buf-file-test.log

DELETE     := -rm
CC         := gcc
CC_OPTIONS := -g

all: $(TEST_PROGRAM_LIST)

test: $(TEST_DEVICE_LIST)

clean:
	$(DELETE) $(TEST_PROGRAM_LIST) $(U_DMA_BUF_FILE_TEST_LOG)

u-dma-buf-test: u-dma-buf-test.c
	$(CC) $(CC_OPTIONS) -o $@ $<

u-dma-buf-direct-test: u-dma-buf-direct-test.c
	$(CC) $(CC_OPTIONS) -o $@ $<

u-dma-buf-ioctl-test: u-dma-buf-ioctl-test.c
	$(CC) $(CC_OPTIONS) -o $@ $<

u-dma-buf-file-test: u-dma-buf-file-test.c
	$(CC) $(CC_OPTIONS) -o $@ $<

u-dma-buf-uring-test: u-dma-buf-uring-test.c
	$(CC) $(CC_OPTIONS) -luring -o $@ $<


define U_DMA_BUF_FILE_TEST
$(1) : u-dma-buf-file-test $(2)
	dtbo-config -i $(1) --dts $(2)
	echo "# u-dma-buf-file-test -n $(1)" >> $(U_DMA_BUF_FILE_TEST_LOG)
	      ./u-dma-buf-file-test -n $(1)  >> $(U_DMA_BUF_FILE_TEST_LOG)
	echo ""                              >> $(U_DMA_BUF_FILE_TEST_LOG)
	dtbo-config -r $(1)
endef

$(foreach DEVICE, $(TEST_DEVICE_LIST), $(eval $(call U_DMA_BUF_FILE_TEST, $(DEVICE), $(addsuffix .dts,$(DEVICE)))))


