################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../stm32-it-sdk/Src/it_sdk/encrypt/aes128ctr.c \
../stm32-it-sdk/Src/it_sdk/encrypt/speck.c \
../stm32-it-sdk/Src/it_sdk/encrypt/tools.c 

OBJS += \
./stm32-it-sdk/Src/it_sdk/encrypt/aes128ctr.o \
./stm32-it-sdk/Src/it_sdk/encrypt/speck.o \
./stm32-it-sdk/Src/it_sdk/encrypt/tools.o 

C_DEPS += \
./stm32-it-sdk/Src/it_sdk/encrypt/aes128ctr.d \
./stm32-it-sdk/Src/it_sdk/encrypt/speck.d \
./stm32-it-sdk/Src/it_sdk/encrypt/tools.d 


# Each subdirectory must supply rules for building sources it contributes
stm32-it-sdk/Src/it_sdk/encrypt/%.o stm32-it-sdk/Src/it_sdk/encrypt/%.su stm32-it-sdk/Src/it_sdk/encrypt/%.cyclo: ../stm32-it-sdk/Src/it_sdk/encrypt/%.c stm32-it-sdk/Src/it_sdk/encrypt/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DUSE_HAL_DRIVER -DSTM32L072xx -DDEBUG -c -I../Core/Inc -I../Drivers/STM32L0xx_HAL_Driver/Inc -I../Drivers/STM32L0xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../Drivers/CMSIS/Include -I/home/local/Documents/StageIoT/STM/B-L072Z-main/stm32-it-sdk/Inc -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-stm32-2d-it-2d-sdk-2f-Src-2f-it_sdk-2f-encrypt

clean-stm32-2d-it-2d-sdk-2f-Src-2f-it_sdk-2f-encrypt:
	-$(RM) ./stm32-it-sdk/Src/it_sdk/encrypt/aes128ctr.cyclo ./stm32-it-sdk/Src/it_sdk/encrypt/aes128ctr.d ./stm32-it-sdk/Src/it_sdk/encrypt/aes128ctr.o ./stm32-it-sdk/Src/it_sdk/encrypt/aes128ctr.su ./stm32-it-sdk/Src/it_sdk/encrypt/speck.cyclo ./stm32-it-sdk/Src/it_sdk/encrypt/speck.d ./stm32-it-sdk/Src/it_sdk/encrypt/speck.o ./stm32-it-sdk/Src/it_sdk/encrypt/speck.su ./stm32-it-sdk/Src/it_sdk/encrypt/tools.cyclo ./stm32-it-sdk/Src/it_sdk/encrypt/tools.d ./stm32-it-sdk/Src/it_sdk/encrypt/tools.o ./stm32-it-sdk/Src/it_sdk/encrypt/tools.su

.PHONY: clean-stm32-2d-it-2d-sdk-2f-Src-2f-it_sdk-2f-encrypt

