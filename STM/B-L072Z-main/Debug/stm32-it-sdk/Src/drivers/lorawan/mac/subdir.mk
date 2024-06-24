################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMac.c \
../stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacAdr.c \
../stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacClassB.c \
../stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacCommands.c \
../stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacConfirmQueue.c \
../stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacCrypto.c \
../stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacFCntHandler.c \
../stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacParser.c \
../stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacSerializer.c 

OBJS += \
./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMac.o \
./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacAdr.o \
./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacClassB.o \
./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacCommands.o \
./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacConfirmQueue.o \
./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacCrypto.o \
./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacFCntHandler.o \
./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacParser.o \
./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacSerializer.o 

C_DEPS += \
./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMac.d \
./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacAdr.d \
./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacClassB.d \
./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacCommands.d \
./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacConfirmQueue.d \
./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacCrypto.d \
./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacFCntHandler.d \
./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacParser.d \
./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacSerializer.d 


# Each subdirectory must supply rules for building sources it contributes
stm32-it-sdk/Src/drivers/lorawan/mac/%.o stm32-it-sdk/Src/drivers/lorawan/mac/%.su stm32-it-sdk/Src/drivers/lorawan/mac/%.cyclo: ../stm32-it-sdk/Src/drivers/lorawan/mac/%.c stm32-it-sdk/Src/drivers/lorawan/mac/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DUSE_HAL_DRIVER -DSTM32L072xx -DDEBUG -c -I../Core/Inc -I../Drivers/STM32L0xx_HAL_Driver/Inc -I../Drivers/STM32L0xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../Drivers/CMSIS/Include -I/home/local/Documents/StageIoT/STM/itsdk-example-murata-lora/stm32-it-sdk/Inc -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-stm32-2d-it-2d-sdk-2f-Src-2f-drivers-2f-lorawan-2f-mac

clean-stm32-2d-it-2d-sdk-2f-Src-2f-drivers-2f-lorawan-2f-mac:
	-$(RM) ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMac.cyclo ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMac.d ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMac.o ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMac.su ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacAdr.cyclo ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacAdr.d ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacAdr.o ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacAdr.su ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacClassB.cyclo ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacClassB.d ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacClassB.o ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacClassB.su ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacCommands.cyclo ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacCommands.d ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacCommands.o ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacCommands.su ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacConfirmQueue.cyclo ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacConfirmQueue.d ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacConfirmQueue.o ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacConfirmQueue.su ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacCrypto.cyclo ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacCrypto.d ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacCrypto.o ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacCrypto.su ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacFCntHandler.cyclo ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacFCntHandler.d ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacFCntHandler.o ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacFCntHandler.su ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacParser.cyclo ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacParser.d ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacParser.o ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacParser.su ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacSerializer.cyclo ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacSerializer.d ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacSerializer.o ./stm32-it-sdk/Src/drivers/lorawan/mac/LoRaMacSerializer.su

.PHONY: clean-stm32-2d-it-2d-sdk-2f-Src-2f-drivers-2f-lorawan-2f-mac

