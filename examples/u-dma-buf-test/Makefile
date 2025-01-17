
TEST_PROGRAM_LIST := u-dma-buf-test        \
                     u-dma-buf-direct-test \
                     u-dma-buf-ioctl-test  \
                     u-dma-buf-file-test   \
                     $(END_LIST)

DEVICE_LIST       := udmabuf-fabric-low    \
                     udmabuf-fabric-high   \
                     udmabuf-soc-high      \
                     udmabuf-ddr-c0        \
                     udmabuf-ddr-nc0       \
                     udmabuf-ddr-nc-wcb0   \
                     $(END_LIST)

FILE_TEST_LIST    := $(addprefix file-test-,$(DEVICE_LIST))
FILE_TEST_LOG     := u-dma-buf-file-test.log

DTBO_CONFIG       := ../../tools/dtbo-config
DELETE            := -rm
CC                := gcc
CC_OPTIONS        := -g

all: $(TEST_PROGRAM_LIST)

clean:
	$(DELETE) $(TEST_PROGRAM_LIST) $(FILE_TEST_LOG)

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


file_test: $(FILE_TEST_LIST)

define U_DMA_BUF_FILE_TEST
$(2) : u-dma-buf-file-test $(3)
	$(DTBO_CONFIG) -i $(1) --dts $(3)
	echo "## $(2)"                >> $(FILE_TEST_LOG)
	./u-dma-buf-file-test -n $(1) >> $(FILE_TEST_LOG)
	echo ""                       >> $(FILE_TEST_LOG)
	$(DTBO_CONFIG) -r $(1)
endef

$(foreach DEVICE, $(DEVICE_LIST), $(eval $(call U_DMA_BUF_FILE_TEST, $(DEVICE), $(addprefix file-test-,$(DEVICE)), $(addsuffix .dts,$(DEVICE)))))

