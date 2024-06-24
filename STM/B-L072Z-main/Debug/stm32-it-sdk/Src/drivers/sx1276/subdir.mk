################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../stm32-it-sdk/Src/drivers/sx1276/murata_cmwx1zzabz.c \
../stm32-it-sdk/Src/drivers/sx1276/sigfox_credentials.c \
../stm32-it-sdk/Src/drivers/sx1276/sigfox_lib_api.c \
../stm32-it-sdk/Src/drivers/sx1276/sigfox_lowlevel.c \
../stm32-it-sdk/Src/drivers/sx1276/sigfox_sx1276.c \
../stm32-it-sdk/Src/drivers/sx1276/sx1276.c 

OBJS += \
./stm32-it-sdk/Src/drivers/sx1276/murata_cmwx1zzabz.o \
./stm32-it-sdk/Src/drivers/sx1276/sigfox_credentials.o \
./stm32-it-sdk/Src/drivers/sx1276/sigfox_lib_api.o \
./stm32-it-sdk/Src/drivers/sx1276/sigfox_lowlevel.o \
./stm32-it-sdk/Src/drivers/sx1276/sigfox_sx1276.o \
./stm32-it-sdk/Src/drivers/sx1276/sx1276.o 

C_DEPS += \
./stm32-it-sdk/Src/drivers/sx1276/murata_cmwx1zzabz.d \
./stm32-it-sdk/Src/drivers/sx1276/sigfox_credentials.d \
./stm32-it-sdk/Src/drivers/sx1276/sigfox_lib_api.d \
./stm32-it-sdk/Src/drivers/sx1276/sigfox_lowlevel.d \
./stm32-it-sdk/Src/drivers/sx1276/sigfox_sx1276.d \
./stm32-it-sdk/Src/drivers/sx1276/sx1276.d 


# Each subdirectory must supply rules for building sources it contributes
stm32-it-sdk/Src/drivers/sx1276/%.o stm32-it-sdk/Src/drivers/sx1276/%.su stm32-it-sdk/Src/drivers/sx1276/%.cyclo: ../stm32-it-sdk/Src/drivers/sx1276/%.c stm32-it-sdk/Src/drivers/sx1276/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DUSE_HAL_DRIVER -DSTM32L072xx -DDEBUG -c -I../Core/Inc -I../Drivers/STM32L0xx_HAL_Driver/Inc -I../Drivers/STM32L0xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../Drivers/CMSIS/Include -I/home/local/Documents/StageIoT/STM/itsdk-example-murata-lora/stm32-it-sdk/Inc -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-stm32-2d-it-2d-sdk-2f-Src-2f-drivers-2f-sx1276

clean-stm32-2d-it-2d-sdk-2f-Src-2f-drivers-2f-sx1276:
	-$(RM) ./stm32-it-sdk/Src/drivers/sx1276/murata_cmwx1zzabz.cyclo ./stm32-it-sdk/Src/drivers/sx1276/murata_cmwx1zzabz.d ./stm32-it-sdk/Src/drivers/sx1276/murata_cmwx1zzabz.o ./stm32-it-sdk/Src/drivers/sx1276/murata_cmwx1zzabz.su ./stm32-it-sdk/Src/drivers/sx1276/sigfox_credentials.cyclo ./stm32-it-sdk/Src/drivers/sx1276/sigfox_credentials.d ./stm32-it-sdk/Src/drivers/sx1276/sigfox_credentials.o ./stm32-it-sdk/Src/drivers/sx1276/sigfox_credentials.su ./stm32-it-sdk/Src/drivers/sx1276/sigfox_lib_api.cyclo ./stm32-it-sdk/Src/drivers/sx1276/sigfox_lib_api.d ./stm32-it-sdk/Src/drivers/sx1276/sigfox_lib_api.o ./stm32-it-sdk/Src/drivers/sx1276/sigfox_lib_api.su ./stm32-it-sdk/Src/drivers/sx1276/sigfox_lowlevel.cyclo ./stm32-it-sdk/Src/drivers/sx1276/sigfox_lowlevel.d ./stm32-it-sdk/Src/drivers/sx1276/sigfox_lowlevel.o ./stm32-it-sdk/Src/drivers/sx1276/sigfox_lowlevel.su ./stm32-it-sdk/Src/drivers/sx1276/sigfox_sx1276.cyclo ./stm32-it-sdk/Src/drivers/sx1276/sigfox_sx1276.d ./stm32-it-sdk/Src/drivers/sx1276/sigfox_sx1276.o ./stm32-it-sdk/Src/drivers/sx1276/sigfox_sx1276.su ./stm32-it-sdk/Src/drivers/sx1276/sx1276.cyclo ./stm32-it-sdk/Src/drivers/sx1276/sx1276.d ./stm32-it-sdk/Src/drivers/sx1276/sx1276.o ./stm32-it-sdk/Src/drivers/sx1276/sx1276.su

.PHONY: clean-stm32-2d-it-2d-sdk-2f-Src-2f-drivers-2f-sx1276

