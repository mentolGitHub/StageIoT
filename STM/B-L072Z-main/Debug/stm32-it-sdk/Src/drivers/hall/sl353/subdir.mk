################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../stm32-it-sdk/Src/drivers/hall/sl353/sl353.c 

OBJS += \
./stm32-it-sdk/Src/drivers/hall/sl353/sl353.o 

C_DEPS += \
./stm32-it-sdk/Src/drivers/hall/sl353/sl353.d 


# Each subdirectory must supply rules for building sources it contributes
stm32-it-sdk/Src/drivers/hall/sl353/%.o stm32-it-sdk/Src/drivers/hall/sl353/%.su stm32-it-sdk/Src/drivers/hall/sl353/%.cyclo: ../stm32-it-sdk/Src/drivers/hall/sl353/%.c stm32-it-sdk/Src/drivers/hall/sl353/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DUSE_HAL_DRIVER -DSTM32L072xx -DDEBUG -c -I../Core/Inc -I../Drivers/STM32L0xx_HAL_Driver/Inc -I../Drivers/STM32L0xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../Drivers/CMSIS/Include -I/home/local/Documents/StageIoT/STM/B-L072Z-main/stm32-it-sdk/Inc -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-stm32-2d-it-2d-sdk-2f-Src-2f-drivers-2f-hall-2f-sl353

clean-stm32-2d-it-2d-sdk-2f-Src-2f-drivers-2f-hall-2f-sl353:
	-$(RM) ./stm32-it-sdk/Src/drivers/hall/sl353/sl353.cyclo ./stm32-it-sdk/Src/drivers/hall/sl353/sl353.d ./stm32-it-sdk/Src/drivers/hall/sl353/sl353.o ./stm32-it-sdk/Src/drivers/hall/sl353/sl353.su

.PHONY: clean-stm32-2d-it-2d-sdk-2f-Src-2f-drivers-2f-hall-2f-sl353
