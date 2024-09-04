################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../stm32-it-sdk/Src/stm32l_sdk/devices.c \
../stm32-it-sdk/Src/stm32l_sdk/gpio_wrapper.c \
../stm32-it-sdk/Src/stm32l_sdk/misc_wrapper.c \
../stm32-it-sdk/Src/stm32l_sdk/uart_wrapper.c 

OBJS += \
./stm32-it-sdk/Src/stm32l_sdk/devices.o \
./stm32-it-sdk/Src/stm32l_sdk/gpio_wrapper.o \
./stm32-it-sdk/Src/stm32l_sdk/misc_wrapper.o \
./stm32-it-sdk/Src/stm32l_sdk/uart_wrapper.o 

C_DEPS += \
./stm32-it-sdk/Src/stm32l_sdk/devices.d \
./stm32-it-sdk/Src/stm32l_sdk/gpio_wrapper.d \
./stm32-it-sdk/Src/stm32l_sdk/misc_wrapper.d \
./stm32-it-sdk/Src/stm32l_sdk/uart_wrapper.d 


# Each subdirectory must supply rules for building sources it contributes
stm32-it-sdk/Src/stm32l_sdk/%.o stm32-it-sdk/Src/stm32l_sdk/%.su stm32-it-sdk/Src/stm32l_sdk/%.cyclo: ../stm32-it-sdk/Src/stm32l_sdk/%.c stm32-it-sdk/Src/stm32l_sdk/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DUSE_HAL_DRIVER -DSTM32L072xx -DDEBUG -c -I../Core/Inc -I../Drivers/STM32L0xx_HAL_Driver/Inc -I../Drivers/STM32L0xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../Drivers/CMSIS/Include -I/home/local/Documents/StageIoT/STM/B-L072Z-main/stm32-it-sdk/Inc -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-stm32-2d-it-2d-sdk-2f-Src-2f-stm32l_sdk

clean-stm32-2d-it-2d-sdk-2f-Src-2f-stm32l_sdk:
	-$(RM) ./stm32-it-sdk/Src/stm32l_sdk/devices.cyclo ./stm32-it-sdk/Src/stm32l_sdk/devices.d ./stm32-it-sdk/Src/stm32l_sdk/devices.o ./stm32-it-sdk/Src/stm32l_sdk/devices.su ./stm32-it-sdk/Src/stm32l_sdk/gpio_wrapper.cyclo ./stm32-it-sdk/Src/stm32l_sdk/gpio_wrapper.d ./stm32-it-sdk/Src/stm32l_sdk/gpio_wrapper.o ./stm32-it-sdk/Src/stm32l_sdk/gpio_wrapper.su ./stm32-it-sdk/Src/stm32l_sdk/misc_wrapper.cyclo ./stm32-it-sdk/Src/stm32l_sdk/misc_wrapper.d ./stm32-it-sdk/Src/stm32l_sdk/misc_wrapper.o ./stm32-it-sdk/Src/stm32l_sdk/misc_wrapper.su ./stm32-it-sdk/Src/stm32l_sdk/uart_wrapper.cyclo ./stm32-it-sdk/Src/stm32l_sdk/uart_wrapper.d ./stm32-it-sdk/Src/stm32l_sdk/uart_wrapper.o ./stm32-it-sdk/Src/stm32l_sdk/uart_wrapper.su

.PHONY: clean-stm32-2d-it-2d-sdk-2f-Src-2f-stm32l_sdk

