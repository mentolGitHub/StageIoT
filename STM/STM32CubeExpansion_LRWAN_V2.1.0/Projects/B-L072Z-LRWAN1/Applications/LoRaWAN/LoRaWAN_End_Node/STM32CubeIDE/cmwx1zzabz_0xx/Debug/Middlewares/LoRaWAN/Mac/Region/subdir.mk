################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/Region.c \
/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionAS923.c \
/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionAU915.c \
/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionBaseUS.c \
/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionCN470.c \
/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionCN779.c \
/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionCommon.c \
/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionEU433.c \
/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionEU868.c \
/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionIN865.c \
/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionKR920.c \
/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionRU864.c \
/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionUS915.c 

OBJS += \
./Middlewares/LoRaWAN/Mac/Region/Region.o \
./Middlewares/LoRaWAN/Mac/Region/RegionAS923.o \
./Middlewares/LoRaWAN/Mac/Region/RegionAU915.o \
./Middlewares/LoRaWAN/Mac/Region/RegionBaseUS.o \
./Middlewares/LoRaWAN/Mac/Region/RegionCN470.o \
./Middlewares/LoRaWAN/Mac/Region/RegionCN779.o \
./Middlewares/LoRaWAN/Mac/Region/RegionCommon.o \
./Middlewares/LoRaWAN/Mac/Region/RegionEU433.o \
./Middlewares/LoRaWAN/Mac/Region/RegionEU868.o \
./Middlewares/LoRaWAN/Mac/Region/RegionIN865.o \
./Middlewares/LoRaWAN/Mac/Region/RegionKR920.o \
./Middlewares/LoRaWAN/Mac/Region/RegionRU864.o \
./Middlewares/LoRaWAN/Mac/Region/RegionUS915.o 

C_DEPS += \
./Middlewares/LoRaWAN/Mac/Region/Region.d \
./Middlewares/LoRaWAN/Mac/Region/RegionAS923.d \
./Middlewares/LoRaWAN/Mac/Region/RegionAU915.d \
./Middlewares/LoRaWAN/Mac/Region/RegionBaseUS.d \
./Middlewares/LoRaWAN/Mac/Region/RegionCN470.d \
./Middlewares/LoRaWAN/Mac/Region/RegionCN779.d \
./Middlewares/LoRaWAN/Mac/Region/RegionCommon.d \
./Middlewares/LoRaWAN/Mac/Region/RegionEU433.d \
./Middlewares/LoRaWAN/Mac/Region/RegionEU868.d \
./Middlewares/LoRaWAN/Mac/Region/RegionIN865.d \
./Middlewares/LoRaWAN/Mac/Region/RegionKR920.d \
./Middlewares/LoRaWAN/Mac/Region/RegionRU864.d \
./Middlewares/LoRaWAN/Mac/Region/RegionUS915.d 


# Each subdirectory must supply rules for building sources it contributes
Middlewares/LoRaWAN/Mac/Region/Region.o: /home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/Region.c Middlewares/LoRaWAN/Mac/Region/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DSTM32L072xx -DUSE_B_L072Z_LRWAN1 -DCMWX1ZZABZ0XX -c -I../../../LoRaWAN/App -I../../../LoRaWAN/Target -I../../../Core/Inc -I../../../../../../../../Utilities/misc -I../../../../../../../../Utilities/timer -I../../../../../../../../Utilities/trace/adv_trace -I../../../../../../../../Utilities/lpm/tiny_lpm -I../../../../../../../../Utilities/sequencer -I../../../../../../../../Drivers/BSP/B-L072Z-LRWAN1 -I../../../../../../../../Drivers/BSP/CMWX1ZZABZ_0xx -I../../../../../../../../Drivers/STM32L0xx_HAL_Driver/Inc -I../../../../../../../../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../../../../../../../../Drivers/CMSIS/Include -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy/sx1276 -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Crypto -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac/Region -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Utilities -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler/packages -I../../../../../../../../Drivers/BSP/IKS01A2 -I../../../../../../../../Drivers/BSP/Components/Common -I../../../../../../../../Drivers/BSP/Components/hts221 -I../../../../../../../../Drivers/BSP/Components/lps22hb -I../../../../../../../../Drivers/BSP/Components/lsm6dsl -I../../../../../../../../Drivers/BSP/Components/lsm303agr -I/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/LmHandler/Packages -Os -ffunction-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"
Middlewares/LoRaWAN/Mac/Region/RegionAS923.o: /home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionAS923.c Middlewares/LoRaWAN/Mac/Region/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DSTM32L072xx -DUSE_B_L072Z_LRWAN1 -DCMWX1ZZABZ0XX -c -I../../../LoRaWAN/App -I../../../LoRaWAN/Target -I../../../Core/Inc -I../../../../../../../../Utilities/misc -I../../../../../../../../Utilities/timer -I../../../../../../../../Utilities/trace/adv_trace -I../../../../../../../../Utilities/lpm/tiny_lpm -I../../../../../../../../Utilities/sequencer -I../../../../../../../../Drivers/BSP/B-L072Z-LRWAN1 -I../../../../../../../../Drivers/BSP/CMWX1ZZABZ_0xx -I../../../../../../../../Drivers/STM32L0xx_HAL_Driver/Inc -I../../../../../../../../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../../../../../../../../Drivers/CMSIS/Include -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy/sx1276 -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Crypto -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac/Region -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Utilities -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler/packages -I../../../../../../../../Drivers/BSP/IKS01A2 -I../../../../../../../../Drivers/BSP/Components/Common -I../../../../../../../../Drivers/BSP/Components/hts221 -I../../../../../../../../Drivers/BSP/Components/lps22hb -I../../../../../../../../Drivers/BSP/Components/lsm6dsl -I../../../../../../../../Drivers/BSP/Components/lsm303agr -I/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/LmHandler/Packages -Os -ffunction-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"
Middlewares/LoRaWAN/Mac/Region/RegionAU915.o: /home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionAU915.c Middlewares/LoRaWAN/Mac/Region/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DSTM32L072xx -DUSE_B_L072Z_LRWAN1 -DCMWX1ZZABZ0XX -c -I../../../LoRaWAN/App -I../../../LoRaWAN/Target -I../../../Core/Inc -I../../../../../../../../Utilities/misc -I../../../../../../../../Utilities/timer -I../../../../../../../../Utilities/trace/adv_trace -I../../../../../../../../Utilities/lpm/tiny_lpm -I../../../../../../../../Utilities/sequencer -I../../../../../../../../Drivers/BSP/B-L072Z-LRWAN1 -I../../../../../../../../Drivers/BSP/CMWX1ZZABZ_0xx -I../../../../../../../../Drivers/STM32L0xx_HAL_Driver/Inc -I../../../../../../../../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../../../../../../../../Drivers/CMSIS/Include -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy/sx1276 -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Crypto -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac/Region -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Utilities -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler/packages -I../../../../../../../../Drivers/BSP/IKS01A2 -I../../../../../../../../Drivers/BSP/Components/Common -I../../../../../../../../Drivers/BSP/Components/hts221 -I../../../../../../../../Drivers/BSP/Components/lps22hb -I../../../../../../../../Drivers/BSP/Components/lsm6dsl -I../../../../../../../../Drivers/BSP/Components/lsm303agr -I/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/LmHandler/Packages -Os -ffunction-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"
Middlewares/LoRaWAN/Mac/Region/RegionBaseUS.o: /home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionBaseUS.c Middlewares/LoRaWAN/Mac/Region/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DSTM32L072xx -DUSE_B_L072Z_LRWAN1 -DCMWX1ZZABZ0XX -c -I../../../LoRaWAN/App -I../../../LoRaWAN/Target -I../../../Core/Inc -I../../../../../../../../Utilities/misc -I../../../../../../../../Utilities/timer -I../../../../../../../../Utilities/trace/adv_trace -I../../../../../../../../Utilities/lpm/tiny_lpm -I../../../../../../../../Utilities/sequencer -I../../../../../../../../Drivers/BSP/B-L072Z-LRWAN1 -I../../../../../../../../Drivers/BSP/CMWX1ZZABZ_0xx -I../../../../../../../../Drivers/STM32L0xx_HAL_Driver/Inc -I../../../../../../../../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../../../../../../../../Drivers/CMSIS/Include -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy/sx1276 -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Crypto -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac/Region -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Utilities -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler/packages -I../../../../../../../../Drivers/BSP/IKS01A2 -I../../../../../../../../Drivers/BSP/Components/Common -I../../../../../../../../Drivers/BSP/Components/hts221 -I../../../../../../../../Drivers/BSP/Components/lps22hb -I../../../../../../../../Drivers/BSP/Components/lsm6dsl -I../../../../../../../../Drivers/BSP/Components/lsm303agr -I/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/LmHandler/Packages -Os -ffunction-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"
Middlewares/LoRaWAN/Mac/Region/RegionCN470.o: /home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionCN470.c Middlewares/LoRaWAN/Mac/Region/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DSTM32L072xx -DUSE_B_L072Z_LRWAN1 -DCMWX1ZZABZ0XX -c -I../../../LoRaWAN/App -I../../../LoRaWAN/Target -I../../../Core/Inc -I../../../../../../../../Utilities/misc -I../../../../../../../../Utilities/timer -I../../../../../../../../Utilities/trace/adv_trace -I../../../../../../../../Utilities/lpm/tiny_lpm -I../../../../../../../../Utilities/sequencer -I../../../../../../../../Drivers/BSP/B-L072Z-LRWAN1 -I../../../../../../../../Drivers/BSP/CMWX1ZZABZ_0xx -I../../../../../../../../Drivers/STM32L0xx_HAL_Driver/Inc -I../../../../../../../../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../../../../../../../../Drivers/CMSIS/Include -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy/sx1276 -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Crypto -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac/Region -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Utilities -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler/packages -I../../../../../../../../Drivers/BSP/IKS01A2 -I../../../../../../../../Drivers/BSP/Components/Common -I../../../../../../../../Drivers/BSP/Components/hts221 -I../../../../../../../../Drivers/BSP/Components/lps22hb -I../../../../../../../../Drivers/BSP/Components/lsm6dsl -I../../../../../../../../Drivers/BSP/Components/lsm303agr -I/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/LmHandler/Packages -Os -ffunction-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"
Middlewares/LoRaWAN/Mac/Region/RegionCN779.o: /home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionCN779.c Middlewares/LoRaWAN/Mac/Region/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DSTM32L072xx -DUSE_B_L072Z_LRWAN1 -DCMWX1ZZABZ0XX -c -I../../../LoRaWAN/App -I../../../LoRaWAN/Target -I../../../Core/Inc -I../../../../../../../../Utilities/misc -I../../../../../../../../Utilities/timer -I../../../../../../../../Utilities/trace/adv_trace -I../../../../../../../../Utilities/lpm/tiny_lpm -I../../../../../../../../Utilities/sequencer -I../../../../../../../../Drivers/BSP/B-L072Z-LRWAN1 -I../../../../../../../../Drivers/BSP/CMWX1ZZABZ_0xx -I../../../../../../../../Drivers/STM32L0xx_HAL_Driver/Inc -I../../../../../../../../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../../../../../../../../Drivers/CMSIS/Include -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy/sx1276 -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Crypto -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac/Region -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Utilities -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler/packages -I../../../../../../../../Drivers/BSP/IKS01A2 -I../../../../../../../../Drivers/BSP/Components/Common -I../../../../../../../../Drivers/BSP/Components/hts221 -I../../../../../../../../Drivers/BSP/Components/lps22hb -I../../../../../../../../Drivers/BSP/Components/lsm6dsl -I../../../../../../../../Drivers/BSP/Components/lsm303agr -I/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/LmHandler/Packages -Os -ffunction-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"
Middlewares/LoRaWAN/Mac/Region/RegionCommon.o: /home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionCommon.c Middlewares/LoRaWAN/Mac/Region/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DSTM32L072xx -DUSE_B_L072Z_LRWAN1 -DCMWX1ZZABZ0XX -c -I../../../LoRaWAN/App -I../../../LoRaWAN/Target -I../../../Core/Inc -I../../../../../../../../Utilities/misc -I../../../../../../../../Utilities/timer -I../../../../../../../../Utilities/trace/adv_trace -I../../../../../../../../Utilities/lpm/tiny_lpm -I../../../../../../../../Utilities/sequencer -I../../../../../../../../Drivers/BSP/B-L072Z-LRWAN1 -I../../../../../../../../Drivers/BSP/CMWX1ZZABZ_0xx -I../../../../../../../../Drivers/STM32L0xx_HAL_Driver/Inc -I../../../../../../../../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../../../../../../../../Drivers/CMSIS/Include -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy/sx1276 -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Crypto -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac/Region -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Utilities -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler/packages -I../../../../../../../../Drivers/BSP/IKS01A2 -I../../../../../../../../Drivers/BSP/Components/Common -I../../../../../../../../Drivers/BSP/Components/hts221 -I../../../../../../../../Drivers/BSP/Components/lps22hb -I../../../../../../../../Drivers/BSP/Components/lsm6dsl -I../../../../../../../../Drivers/BSP/Components/lsm303agr -I/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/LmHandler/Packages -Os -ffunction-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"
Middlewares/LoRaWAN/Mac/Region/RegionEU433.o: /home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionEU433.c Middlewares/LoRaWAN/Mac/Region/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DSTM32L072xx -DUSE_B_L072Z_LRWAN1 -DCMWX1ZZABZ0XX -c -I../../../LoRaWAN/App -I../../../LoRaWAN/Target -I../../../Core/Inc -I../../../../../../../../Utilities/misc -I../../../../../../../../Utilities/timer -I../../../../../../../../Utilities/trace/adv_trace -I../../../../../../../../Utilities/lpm/tiny_lpm -I../../../../../../../../Utilities/sequencer -I../../../../../../../../Drivers/BSP/B-L072Z-LRWAN1 -I../../../../../../../../Drivers/BSP/CMWX1ZZABZ_0xx -I../../../../../../../../Drivers/STM32L0xx_HAL_Driver/Inc -I../../../../../../../../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../../../../../../../../Drivers/CMSIS/Include -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy/sx1276 -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Crypto -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac/Region -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Utilities -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler/packages -I../../../../../../../../Drivers/BSP/IKS01A2 -I../../../../../../../../Drivers/BSP/Components/Common -I../../../../../../../../Drivers/BSP/Components/hts221 -I../../../../../../../../Drivers/BSP/Components/lps22hb -I../../../../../../../../Drivers/BSP/Components/lsm6dsl -I../../../../../../../../Drivers/BSP/Components/lsm303agr -I/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/LmHandler/Packages -Os -ffunction-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"
Middlewares/LoRaWAN/Mac/Region/RegionEU868.o: /home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionEU868.c Middlewares/LoRaWAN/Mac/Region/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DSTM32L072xx -DUSE_B_L072Z_LRWAN1 -DCMWX1ZZABZ0XX -c -I../../../LoRaWAN/App -I../../../LoRaWAN/Target -I../../../Core/Inc -I../../../../../../../../Utilities/misc -I../../../../../../../../Utilities/timer -I../../../../../../../../Utilities/trace/adv_trace -I../../../../../../../../Utilities/lpm/tiny_lpm -I../../../../../../../../Utilities/sequencer -I../../../../../../../../Drivers/BSP/B-L072Z-LRWAN1 -I../../../../../../../../Drivers/BSP/CMWX1ZZABZ_0xx -I../../../../../../../../Drivers/STM32L0xx_HAL_Driver/Inc -I../../../../../../../../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../../../../../../../../Drivers/CMSIS/Include -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy/sx1276 -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Crypto -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac/Region -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Utilities -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler/packages -I../../../../../../../../Drivers/BSP/IKS01A2 -I../../../../../../../../Drivers/BSP/Components/Common -I../../../../../../../../Drivers/BSP/Components/hts221 -I../../../../../../../../Drivers/BSP/Components/lps22hb -I../../../../../../../../Drivers/BSP/Components/lsm6dsl -I../../../../../../../../Drivers/BSP/Components/lsm303agr -I/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/LmHandler/Packages -Os -ffunction-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"
Middlewares/LoRaWAN/Mac/Region/RegionIN865.o: /home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionIN865.c Middlewares/LoRaWAN/Mac/Region/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DSTM32L072xx -DUSE_B_L072Z_LRWAN1 -DCMWX1ZZABZ0XX -c -I../../../LoRaWAN/App -I../../../LoRaWAN/Target -I../../../Core/Inc -I../../../../../../../../Utilities/misc -I../../../../../../../../Utilities/timer -I../../../../../../../../Utilities/trace/adv_trace -I../../../../../../../../Utilities/lpm/tiny_lpm -I../../../../../../../../Utilities/sequencer -I../../../../../../../../Drivers/BSP/B-L072Z-LRWAN1 -I../../../../../../../../Drivers/BSP/CMWX1ZZABZ_0xx -I../../../../../../../../Drivers/STM32L0xx_HAL_Driver/Inc -I../../../../../../../../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../../../../../../../../Drivers/CMSIS/Include -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy/sx1276 -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Crypto -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac/Region -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Utilities -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler/packages -I../../../../../../../../Drivers/BSP/IKS01A2 -I../../../../../../../../Drivers/BSP/Components/Common -I../../../../../../../../Drivers/BSP/Components/hts221 -I../../../../../../../../Drivers/BSP/Components/lps22hb -I../../../../../../../../Drivers/BSP/Components/lsm6dsl -I../../../../../../../../Drivers/BSP/Components/lsm303agr -I/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/LmHandler/Packages -Os -ffunction-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"
Middlewares/LoRaWAN/Mac/Region/RegionKR920.o: /home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionKR920.c Middlewares/LoRaWAN/Mac/Region/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DSTM32L072xx -DUSE_B_L072Z_LRWAN1 -DCMWX1ZZABZ0XX -c -I../../../LoRaWAN/App -I../../../LoRaWAN/Target -I../../../Core/Inc -I../../../../../../../../Utilities/misc -I../../../../../../../../Utilities/timer -I../../../../../../../../Utilities/trace/adv_trace -I../../../../../../../../Utilities/lpm/tiny_lpm -I../../../../../../../../Utilities/sequencer -I../../../../../../../../Drivers/BSP/B-L072Z-LRWAN1 -I../../../../../../../../Drivers/BSP/CMWX1ZZABZ_0xx -I../../../../../../../../Drivers/STM32L0xx_HAL_Driver/Inc -I../../../../../../../../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../../../../../../../../Drivers/CMSIS/Include -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy/sx1276 -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Crypto -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac/Region -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Utilities -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler/packages -I../../../../../../../../Drivers/BSP/IKS01A2 -I../../../../../../../../Drivers/BSP/Components/Common -I../../../../../../../../Drivers/BSP/Components/hts221 -I../../../../../../../../Drivers/BSP/Components/lps22hb -I../../../../../../../../Drivers/BSP/Components/lsm6dsl -I../../../../../../../../Drivers/BSP/Components/lsm303agr -I/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/LmHandler/Packages -Os -ffunction-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"
Middlewares/LoRaWAN/Mac/Region/RegionRU864.o: /home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionRU864.c Middlewares/LoRaWAN/Mac/Region/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DSTM32L072xx -DUSE_B_L072Z_LRWAN1 -DCMWX1ZZABZ0XX -c -I../../../LoRaWAN/App -I../../../LoRaWAN/Target -I../../../Core/Inc -I../../../../../../../../Utilities/misc -I../../../../../../../../Utilities/timer -I../../../../../../../../Utilities/trace/adv_trace -I../../../../../../../../Utilities/lpm/tiny_lpm -I../../../../../../../../Utilities/sequencer -I../../../../../../../../Drivers/BSP/B-L072Z-LRWAN1 -I../../../../../../../../Drivers/BSP/CMWX1ZZABZ_0xx -I../../../../../../../../Drivers/STM32L0xx_HAL_Driver/Inc -I../../../../../../../../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../../../../../../../../Drivers/CMSIS/Include -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy/sx1276 -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Crypto -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac/Region -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Utilities -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler/packages -I../../../../../../../../Drivers/BSP/IKS01A2 -I../../../../../../../../Drivers/BSP/Components/Common -I../../../../../../../../Drivers/BSP/Components/hts221 -I../../../../../../../../Drivers/BSP/Components/lps22hb -I../../../../../../../../Drivers/BSP/Components/lsm6dsl -I../../../../../../../../Drivers/BSP/Components/lsm303agr -I/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/LmHandler/Packages -Os -ffunction-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"
Middlewares/LoRaWAN/Mac/Region/RegionUS915.o: /home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/Mac/Region/RegionUS915.c Middlewares/LoRaWAN/Mac/Region/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DSTM32L072xx -DUSE_B_L072Z_LRWAN1 -DCMWX1ZZABZ0XX -c -I../../../LoRaWAN/App -I../../../LoRaWAN/Target -I../../../Core/Inc -I../../../../../../../../Utilities/misc -I../../../../../../../../Utilities/timer -I../../../../../../../../Utilities/trace/adv_trace -I../../../../../../../../Utilities/lpm/tiny_lpm -I../../../../../../../../Utilities/sequencer -I../../../../../../../../Drivers/BSP/B-L072Z-LRWAN1 -I../../../../../../../../Drivers/BSP/CMWX1ZZABZ_0xx -I../../../../../../../../Drivers/STM32L0xx_HAL_Driver/Inc -I../../../../../../../../Drivers/CMSIS/Device/ST/STM32L0xx/Include -I../../../../../../../../Drivers/CMSIS/Include -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy/sx1276 -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Crypto -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Mac/Region -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/Utilities -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler -I../../../../../../../../Middlewares/Third_Party/LoRaWAN/LmHandler/packages -I../../../../../../../../Drivers/BSP/IKS01A2 -I../../../../../../../../Drivers/BSP/Components/Common -I../../../../../../../../Drivers/BSP/Components/hts221 -I../../../../../../../../Drivers/BSP/Components/lps22hb -I../../../../../../../../Drivers/BSP/Components/lsm6dsl -I../../../../../../../../Drivers/BSP/Components/lsm303agr -I/home/local/Téléchargements/STM32CubeExpansion_LRWAN_V2.1.0/Middlewares/Third_Party/LoRaWAN/LmHandler/Packages -Os -ffunction-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-Middlewares-2f-LoRaWAN-2f-Mac-2f-Region

clean-Middlewares-2f-LoRaWAN-2f-Mac-2f-Region:
	-$(RM) ./Middlewares/LoRaWAN/Mac/Region/Region.cyclo ./Middlewares/LoRaWAN/Mac/Region/Region.d ./Middlewares/LoRaWAN/Mac/Region/Region.o ./Middlewares/LoRaWAN/Mac/Region/Region.su ./Middlewares/LoRaWAN/Mac/Region/RegionAS923.cyclo ./Middlewares/LoRaWAN/Mac/Region/RegionAS923.d ./Middlewares/LoRaWAN/Mac/Region/RegionAS923.o ./Middlewares/LoRaWAN/Mac/Region/RegionAS923.su ./Middlewares/LoRaWAN/Mac/Region/RegionAU915.cyclo ./Middlewares/LoRaWAN/Mac/Region/RegionAU915.d ./Middlewares/LoRaWAN/Mac/Region/RegionAU915.o ./Middlewares/LoRaWAN/Mac/Region/RegionAU915.su ./Middlewares/LoRaWAN/Mac/Region/RegionBaseUS.cyclo ./Middlewares/LoRaWAN/Mac/Region/RegionBaseUS.d ./Middlewares/LoRaWAN/Mac/Region/RegionBaseUS.o ./Middlewares/LoRaWAN/Mac/Region/RegionBaseUS.su ./Middlewares/LoRaWAN/Mac/Region/RegionCN470.cyclo ./Middlewares/LoRaWAN/Mac/Region/RegionCN470.d ./Middlewares/LoRaWAN/Mac/Region/RegionCN470.o ./Middlewares/LoRaWAN/Mac/Region/RegionCN470.su ./Middlewares/LoRaWAN/Mac/Region/RegionCN779.cyclo ./Middlewares/LoRaWAN/Mac/Region/RegionCN779.d ./Middlewares/LoRaWAN/Mac/Region/RegionCN779.o ./Middlewares/LoRaWAN/Mac/Region/RegionCN779.su ./Middlewares/LoRaWAN/Mac/Region/RegionCommon.cyclo ./Middlewares/LoRaWAN/Mac/Region/RegionCommon.d ./Middlewares/LoRaWAN/Mac/Region/RegionCommon.o ./Middlewares/LoRaWAN/Mac/Region/RegionCommon.su ./Middlewares/LoRaWAN/Mac/Region/RegionEU433.cyclo ./Middlewares/LoRaWAN/Mac/Region/RegionEU433.d ./Middlewares/LoRaWAN/Mac/Region/RegionEU433.o ./Middlewares/LoRaWAN/Mac/Region/RegionEU433.su ./Middlewares/LoRaWAN/Mac/Region/RegionEU868.cyclo ./Middlewares/LoRaWAN/Mac/Region/RegionEU868.d ./Middlewares/LoRaWAN/Mac/Region/RegionEU868.o ./Middlewares/LoRaWAN/Mac/Region/RegionEU868.su ./Middlewares/LoRaWAN/Mac/Region/RegionIN865.cyclo ./Middlewares/LoRaWAN/Mac/Region/RegionIN865.d ./Middlewares/LoRaWAN/Mac/Region/RegionIN865.o ./Middlewares/LoRaWAN/Mac/Region/RegionIN865.su ./Middlewares/LoRaWAN/Mac/Region/RegionKR920.cyclo ./Middlewares/LoRaWAN/Mac/Region/RegionKR920.d ./Middlewares/LoRaWAN/Mac/Region/RegionKR920.o ./Middlewares/LoRaWAN/Mac/Region/RegionKR920.su ./Middlewares/LoRaWAN/Mac/Region/RegionRU864.cyclo ./Middlewares/LoRaWAN/Mac/Region/RegionRU864.d ./Middlewares/LoRaWAN/Mac/Region/RegionRU864.o ./Middlewares/LoRaWAN/Mac/Region/RegionRU864.su ./Middlewares/LoRaWAN/Mac/Region/RegionUS915.cyclo ./Middlewares/LoRaWAN/Mac/Region/RegionUS915.d ./Middlewares/LoRaWAN/Mac/Region/RegionUS915.o ./Middlewares/LoRaWAN/Mac/Region/RegionUS915.su

.PHONY: clean-Middlewares-2f-LoRaWAN-2f-Mac-2f-Region

