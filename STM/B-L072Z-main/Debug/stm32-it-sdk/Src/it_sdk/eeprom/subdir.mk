################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../stm32-it-sdk/Src/it_sdk/eeprom/eeprom.c \
../stm32-it-sdk/Src/it_sdk/eeprom/sdk_config.c \
../stm32-it-sdk/Src/it_sdk/eeprom/sdk_state.c \
../stm32-it-sdk/Src/it_sdk/eeprom/securestore.c 

OBJS += \
./stm32-it-sdk/Src/it_sdk/eeprom/eeprom.o \
./stm32-it-sdk/Src/it_sdk/eeprom/sdk_config.o \
./stm32-it-sdk/Src/it_sdk/eeprom/sdk_state.o \
./stm32-it-sdk/Src/it_sdk/eeprom/securestore.o 

C_DEPS += \
./stm32-it-sdk/Src/it_sdk/eeprom/eeprom.d \
./stm32-it-sdk/Src/it_sdk/eeprom/sdk_config.d \
./stm32-it-sdk/Src/it_sdk/eeprom/sdk_state.d \
./stm32-it-sdk/Src/it_sdk/eeprom/securestore.d 


# Each subdirectory must supply rules for building sources it contributes
stm32-it-sdk/Src/it_sdk/eeprom/%.o stm32-it-sdk/Src/it_sdk/eeprom/%.su stm32-it-sdk/Src/it_sdk/eeprom/%.cyclo: ../stm32-it-sdk/Src/it_sdk/eeprom/%.c stm32-it-sdk/Src/it_sdk/eeprom/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DUSE_HAL_DRIVER -DSTM32L072xx -DDEBUG -c -I../Core/Inc -I../Drivers/STM32L0xx_HAL_Driver/Inc -I../Drivers/STM32L0xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../Drivers/CMSIS/Include -I/home/local/Documents/StageIoT/STM/B-L072Z-main/stm32-it-sdk/Inc -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-stm32-2d-it-2d-sdk-2f-Src-2f-it_sdk-2f-eeprom

clean-stm32-2d-it-2d-sdk-2f-Src-2f-it_sdk-2f-eeprom:
	-$(RM) ./stm32-it-sdk/Src/it_sdk/eeprom/eeprom.cyclo ./stm32-it-sdk/Src/it_sdk/eeprom/eeprom.d ./stm32-it-sdk/Src/it_sdk/eeprom/eeprom.o ./stm32-it-sdk/Src/it_sdk/eeprom/eeprom.su ./stm32-it-sdk/Src/it_sdk/eeprom/sdk_config.cyclo ./stm32-it-sdk/Src/it_sdk/eeprom/sdk_config.d ./stm32-it-sdk/Src/it_sdk/eeprom/sdk_config.o ./stm32-it-sdk/Src/it_sdk/eeprom/sdk_config.su ./stm32-it-sdk/Src/it_sdk/eeprom/sdk_state.cyclo ./stm32-it-sdk/Src/it_sdk/eeprom/sdk_state.d ./stm32-it-sdk/Src/it_sdk/eeprom/sdk_state.o ./stm32-it-sdk/Src/it_sdk/eeprom/sdk_state.su ./stm32-it-sdk/Src/it_sdk/eeprom/securestore.cyclo ./stm32-it-sdk/Src/it_sdk/eeprom/securestore.d ./stm32-it-sdk/Src/it_sdk/eeprom/securestore.o ./stm32-it-sdk/Src/it_sdk/eeprom/securestore.su

.PHONY: clean-stm32-2d-it-2d-sdk-2f-Src-2f-it_sdk-2f-eeprom

