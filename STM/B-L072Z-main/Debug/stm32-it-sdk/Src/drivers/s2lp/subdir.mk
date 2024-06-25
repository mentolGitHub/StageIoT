################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../stm32-it-sdk/Src/drivers/s2lp/s2lp.c \
../stm32-it-sdk/Src/drivers/s2lp/s2lp_idRetriever.c \
../stm32-it-sdk/Src/drivers/s2lp/s2lp_spi.c \
../stm32-it-sdk/Src/drivers/s2lp/sigfox_helper.c \
../stm32-it-sdk/Src/drivers/s2lp/st_lib_api.c 

OBJS += \
./stm32-it-sdk/Src/drivers/s2lp/s2lp.o \
./stm32-it-sdk/Src/drivers/s2lp/s2lp_idRetriever.o \
./stm32-it-sdk/Src/drivers/s2lp/s2lp_spi.o \
./stm32-it-sdk/Src/drivers/s2lp/sigfox_helper.o \
./stm32-it-sdk/Src/drivers/s2lp/st_lib_api.o 

C_DEPS += \
./stm32-it-sdk/Src/drivers/s2lp/s2lp.d \
./stm32-it-sdk/Src/drivers/s2lp/s2lp_idRetriever.d \
./stm32-it-sdk/Src/drivers/s2lp/s2lp_spi.d \
./stm32-it-sdk/Src/drivers/s2lp/sigfox_helper.d \
./stm32-it-sdk/Src/drivers/s2lp/st_lib_api.d 


# Each subdirectory must supply rules for building sources it contributes
stm32-it-sdk/Src/drivers/s2lp/%.o stm32-it-sdk/Src/drivers/s2lp/%.su stm32-it-sdk/Src/drivers/s2lp/%.cyclo: ../stm32-it-sdk/Src/drivers/s2lp/%.c stm32-it-sdk/Src/drivers/s2lp/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DUSE_HAL_DRIVER -DSTM32L072xx -DDEBUG -c -I../Core/Inc -I../Drivers/STM32L0xx_HAL_Driver/Inc -I../Drivers/STM32L0xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../Drivers/CMSIS/Include -I/home/local/Documents/StageIoT/STM/B-L072Z-main/stm32-it-sdk/Inc -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-stm32-2d-it-2d-sdk-2f-Src-2f-drivers-2f-s2lp

clean-stm32-2d-it-2d-sdk-2f-Src-2f-drivers-2f-s2lp:
	-$(RM) ./stm32-it-sdk/Src/drivers/s2lp/s2lp.cyclo ./stm32-it-sdk/Src/drivers/s2lp/s2lp.d ./stm32-it-sdk/Src/drivers/s2lp/s2lp.o ./stm32-it-sdk/Src/drivers/s2lp/s2lp.su ./stm32-it-sdk/Src/drivers/s2lp/s2lp_idRetriever.cyclo ./stm32-it-sdk/Src/drivers/s2lp/s2lp_idRetriever.d ./stm32-it-sdk/Src/drivers/s2lp/s2lp_idRetriever.o ./stm32-it-sdk/Src/drivers/s2lp/s2lp_idRetriever.su ./stm32-it-sdk/Src/drivers/s2lp/s2lp_spi.cyclo ./stm32-it-sdk/Src/drivers/s2lp/s2lp_spi.d ./stm32-it-sdk/Src/drivers/s2lp/s2lp_spi.o ./stm32-it-sdk/Src/drivers/s2lp/s2lp_spi.su ./stm32-it-sdk/Src/drivers/s2lp/sigfox_helper.cyclo ./stm32-it-sdk/Src/drivers/s2lp/sigfox_helper.d ./stm32-it-sdk/Src/drivers/s2lp/sigfox_helper.o ./stm32-it-sdk/Src/drivers/s2lp/sigfox_helper.su ./stm32-it-sdk/Src/drivers/s2lp/st_lib_api.cyclo ./stm32-it-sdk/Src/drivers/s2lp/st_lib_api.d ./stm32-it-sdk/Src/drivers/s2lp/st_lib_api.o ./stm32-it-sdk/Src/drivers/s2lp/st_lib_api.su

.PHONY: clean-stm32-2d-it-2d-sdk-2f-Src-2f-drivers-2f-s2lp

