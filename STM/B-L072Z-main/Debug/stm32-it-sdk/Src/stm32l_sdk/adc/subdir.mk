################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../stm32-it-sdk/Src/stm32l_sdk/adc/adc.c 

OBJS += \
./stm32-it-sdk/Src/stm32l_sdk/adc/adc.o 

C_DEPS += \
./stm32-it-sdk/Src/stm32l_sdk/adc/adc.d 


# Each subdirectory must supply rules for building sources it contributes
stm32-it-sdk/Src/stm32l_sdk/adc/%.o stm32-it-sdk/Src/stm32l_sdk/adc/%.su stm32-it-sdk/Src/stm32l_sdk/adc/%.cyclo: ../stm32-it-sdk/Src/stm32l_sdk/adc/%.c stm32-it-sdk/Src/stm32l_sdk/adc/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DUSE_HAL_DRIVER -DSTM32L072xx -DDEBUG -c -I../Core/Inc -I../Drivers/STM32L0xx_HAL_Driver/Inc -I../Drivers/STM32L0xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../Drivers/CMSIS/Include -I/home/local/Documents/StageIoT/STM/B-L072Z-main/stm32-it-sdk/Inc -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-stm32-2d-it-2d-sdk-2f-Src-2f-stm32l_sdk-2f-adc

clean-stm32-2d-it-2d-sdk-2f-Src-2f-stm32l_sdk-2f-adc:
	-$(RM) ./stm32-it-sdk/Src/stm32l_sdk/adc/adc.cyclo ./stm32-it-sdk/Src/stm32l_sdk/adc/adc.d ./stm32-it-sdk/Src/stm32l_sdk/adc/adc.o ./stm32-it-sdk/Src/stm32l_sdk/adc/adc.su

.PHONY: clean-stm32-2d-it-2d-sdk-2f-Src-2f-stm32l_sdk-2f-adc

