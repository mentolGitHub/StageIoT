/**
  ******************************************************************************
  * @file    adc.c
  * @brief   This file provides code for the configuration
  *          of the ADC instances.
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2021 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under Ultimate Liberty license
  * SLA0044, the "License"; You may not use this file except in compliance with
  * the License. You may obtain a copy of the License at:
  *                             www.st.com/SLA0044
  *
  ******************************************************************************
  */

/* Includes ------------------------------------------------------------------*/
#include "adc.h"

/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

ADC_HandleTypeDef hadc;

/* ADC init function */
void MX_ADC_Init(void)
{

  /* USER CODE BEGIN ADC_Init 0 */

  /* USER CODE END ADC_Init 0 */

  /* USER CODE BEGIN ADC_Init 1 */

  /* USER CODE END ADC_Init 1 */
  /** Configure the global features of the ADC (Clock, Resolution, Data Alignment and number of conversion)
  */
  hadc.Instance  = ADC1;

  hadc.Init.ClockPrescaler        = ADC_CLOCK_ASYNC_DIV4;
  hadc.Init.Resolution            = ADC_RESOLUTION_12B;
  hadc.Init.ScanConvMode          = ADC_SCAN_DISABLE;
  hadc.Init.ContinuousConvMode    = DISABLE;
  hadc.Init.ExternalTrigConv      = ADC_EXTERNALTRIGCONVEDGE_NONE;
  hadc.Init.LowPowerAutoWait      = ADC_AUTOWAIT_UNTIL_DATA_READ; /* ADC_DelaySelectionConfig( ADC1, ADC_DelayLength_Freeze ); */
  hadc.Init.LowPowerAutoPowerOff  = ADC_AUTOPOWEROFF_IDLE_DELAY_PHASES;
  if (HAL_ADC_Init(&hadc) != HAL_OK)
  {
    Error_Handler();
  }

  /* USER CODE BEGIN ADC_Init 2 */

  /* USER CODE END ADC_Init 2 */

}

void HAL_ADC_MspInit(ADC_HandleTypeDef *adcHandle)
{

  if (adcHandle->Instance == ADC1)
  {
    /* USER CODE BEGIN ADC_MspInit 0 */

    /* USER CODE END ADC_MspInit 0 */
    /* ADC clock enable */
    __HAL_RCC_ADC1_CLK_ENABLE();
    /* USER CODE BEGIN ADC_MspInit 1 */

    /* USER CODE END ADC_MspInit 1 */
  }
}

void HAL_ADC_MspDeInit(ADC_HandleTypeDef *adcHandle)
{

  if (adcHandle->Instance == ADC1)
  {
    /* USER CODE BEGIN ADC_MspDeInit 0 */

    /* USER CODE END ADC_MspDeInit 0 */

    __HAL_RCC_ADC1_FORCE_RESET();
    __HAL_RCC_ADC1_RELEASE_RESET();
    /* Peripheral clock disable */
    __HAL_RCC_ADC1_CLK_DISABLE();
    /* USER CODE BEGIN ADC_MspDeInit 1 */

    /* USER CODE END ADC_MspDeInit 1 */
  }
}

/* USER CODE BEGIN 1 */

/* USER CODE END 1 */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
