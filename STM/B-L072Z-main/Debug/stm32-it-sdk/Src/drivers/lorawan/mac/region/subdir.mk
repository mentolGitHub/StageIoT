################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../stm32-it-sdk/Src/drivers/lorawan/mac/region/Region.c \
../stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionAS923.c \
../stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionAU915.c \
../stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionCN470.c \
../stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionCN779.c \
../stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionCommon.c \
../stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionEU433.c \
../stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionEU868.c \
../stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionIN865.c \
../stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionKR920.c \
../stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionRU864.c \
../stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionUS915.c 

OBJS += \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/Region.o \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionAS923.o \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionAU915.o \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionCN470.o \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionCN779.o \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionCommon.o \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionEU433.o \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionEU868.o \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionIN865.o \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionKR920.o \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionRU864.o \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionUS915.o 

C_DEPS += \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/Region.d \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionAS923.d \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionAU915.d \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionCN470.d \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionCN779.d \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionCommon.d \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionEU433.d \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionEU868.d \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionIN865.d \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionKR920.d \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionRU864.d \
./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionUS915.d 


# Each subdirectory must supply rules for building sources it contributes
stm32-it-sdk/Src/drivers/lorawan/mac/region/%.o stm32-it-sdk/Src/drivers/lorawan/mac/region/%.su stm32-it-sdk/Src/drivers/lorawan/mac/region/%.cyclo: ../stm32-it-sdk/Src/drivers/lorawan/mac/region/%.c stm32-it-sdk/Src/drivers/lorawan/mac/region/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DUSE_HAL_DRIVER -DSTM32L072xx -DDEBUG -c -I../Core/Inc -I../Drivers/STM32L0xx_HAL_Driver/Inc -I../Drivers/STM32L0xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../Drivers/CMSIS/Include -I/home/local/Documents/StageIoT/STM/B-L072Z-main/stm32-it-sdk/Inc -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-stm32-2d-it-2d-sdk-2f-Src-2f-drivers-2f-lorawan-2f-mac-2f-region

clean-stm32-2d-it-2d-sdk-2f-Src-2f-drivers-2f-lorawan-2f-mac-2f-region:
	-$(RM) ./stm32-it-sdk/Src/drivers/lorawan/mac/region/Region.cyclo ./stm32-it-sdk/Src/drivers/lorawan/mac/region/Region.d ./stm32-it-sdk/Src/drivers/lorawan/mac/region/Region.o ./stm32-it-sdk/Src/drivers/lorawan/mac/region/Region.su ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionAS923.cyclo ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionAS923.d ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionAS923.o ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionAS923.su ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionAU915.cyclo ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionAU915.d ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionAU915.o ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionAU915.su ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionCN470.cyclo ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionCN470.d ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionCN470.o ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionCN470.su ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionCN779.cyclo ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionCN779.d ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionCN779.o ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionCN779.su ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionCommon.cyclo ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionCommon.d ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionCommon.o ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionCommon.su ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionEU433.cyclo ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionEU433.d ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionEU433.o ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionEU433.su ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionEU868.cyclo ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionEU868.d ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionEU868.o ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionEU868.su ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionIN865.cyclo ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionIN865.d ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionIN865.o ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionIN865.su ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionKR920.cyclo ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionKR920.d ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionKR920.o ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionKR920.su ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionRU864.cyclo ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionRU864.d ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionRU864.o ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionRU864.su ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionUS915.cyclo ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionUS915.d ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionUS915.o ./stm32-it-sdk/Src/drivers/lorawan/mac/region/RegionUS915.su

.PHONY: clean-stm32-2d-it-2d-sdk-2f-Src-2f-drivers-2f-lorawan-2f-mac-2f-region

