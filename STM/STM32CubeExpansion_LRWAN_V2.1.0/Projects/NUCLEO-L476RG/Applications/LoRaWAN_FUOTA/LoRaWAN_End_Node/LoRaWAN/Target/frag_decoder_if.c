/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file    frag_decoder_if.c
  * @author  MCD Application Team
  * @brief   Implements the Data Distribution Agent
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2020 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under Ultimate Liberty license
  * SLA0044, the "License"; You may not use this file except in compliance with
  * the License. You may obtain a copy of the License at:
  *                             www.st.com/SLA0044
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "platform.h"
#include "frag_decoder_if.h"
#include "sys_app.h"
#include "utilities.h"
#include "flash_if.h"
#include "fw_update_agent.h"

#if defined(__CC_ARM)||defined(__ARMCC_VERSION)
#include "mapping_fwimg.h"
#elif defined(__ICCARM__)||defined(__GNUC__)
#include "mapping_export.h"         /* to access to the definition of REGION_SLOT_1_START*/
#endif

/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* External variables ---------------------------------------------------------*/
/* USER CODE BEGIN EV */

/* USER CODE END EV */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/*!
 * Defines the maximum size for the buffer receiving the fragmentation result.
 *
 * \remark By default frag_decoder_if.h defines:
 *         \ref FRAG_MAX_NB   313
 *         \ref FRAG_MAX_SIZE 216
 *
 *         In interop test mode will be
 *         \ref FRAG_MAX_NB   20
 *         \ref FRAG_MAX_SIZE 50
 *
 *         FileSize = FRAG_MAX_NB * FRAG_MAX_SIZE
 *
 *         If bigger file size is to be received or is fragmented differently
 *         one must update those parameters.
 *
 * \remark  Memory allocation is done at compile time. Several options have to be foreseen
 *          in order to optimize the memory. Will depend of the Memory management used
 *          Could be Dynamic allocation --> malloc method
 *          Variable Length Array --> VLA method
 *          pseudo dynamic allocation --> memory pool method
 *          Other option :
 *          In place of using the caching memory method we can foreseen to have a direct
 *          flash memory copy. This solution will depend of the SBSFU constraint
 *
 */
#define UNFRAGMENTED_DATA_SIZE                      ( FRAG_MAX_NB * FRAG_MAX_SIZE )

/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
/**
  * Fragmentation package callbacks parameters
  */
const LmhpFragmentationParams_t FRAG_DECODER_IF_FragmentationParams =
{
  .DecoderCallbacks =
  {
    .FragDecoderErase = FRAG_DECODER_IF_Erase,
    .FragDecoderWrite = FRAG_DECODER_IF_Write,
    .FragDecoderRead = FRAG_DECODER_IF_Read,
  },
  .OnProgress = FRAG_DECODER_IF_OnProgress,
  .OnDone = FRAG_DECODER_IF_OnDone
};

#if (CACHING_MODE == 1)  /*write fragment in RAM - Caching mode*/
/**
  * Un-fragmented data storage.
  */
static uint8_t UnfragmentedData[UNFRAGMENTED_DATA_SIZE];
#else
/**
  * Temp buffer to store fragment in RAM to avoid several Flash write
  */
static uint8_t FRAG_DECODER_IF_RAM_buffer[FLASH_PAGE_SIZE];
#endif /* CACHING_MODE */

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/

/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Exported functions --------------------------------------------------------*/
int32_t FRAG_DECODER_IF_Erase(void)
{
  /* USER CODE BEGIN FRAG_DECODER_IF_Erase_1 */

  /* USER CODE END FRAG_DECODER_IF_Erase_1 */
  int32_t status = FLASH_OK;
#if (CACHING_MODE == 1)
  uint32_t size = UNFRAGMENTED_DATA_SIZE;
  uint8_t *dst8 = UnfragmentedData;

  while (size--)
  {
    *dst8++ = 0xFF;
  }

#else /* CACHING_MODE == 0 */
  uint32_t first_page = PAGE(FRAG_DECODER_DWL_REGION_START);
  uint32_t nb_pages = PAGE(FRAG_DECODER_DWL_REGION_START + FRAG_DECODER_DWL_REGION_SIZE - 1) - first_page + 1U;

  if (HAL_FLASH_Unlock() == HAL_OK)
  {
    status = FLASH_IF_EraseByPages(first_page, nb_pages, 0U);
    /* Lock the Flash to disable the flash control register access (recommended
    to protect the FLASH memory against possible unwanted operation) *********/
    HAL_FLASH_Lock();
  }
  else
  {
    status = FLASH_LOCK_ERROR;
  }

#endif /* CACHING_MODE */
  if (status != FLASH_OK)
  {
    status = FLASH_ERROR;
  }
  return status;
  /* USER CODE BEGIN FRAG_DECODER_IF_Erase_2 */

  /* USER CODE END FRAG_DECODER_IF_Erase_2 */
}

int32_t FRAG_DECODER_IF_Write(uint32_t addr, uint8_t *data, uint32_t size)
{
  /* USER CODE BEGIN FRAG_DECODER_IF_Write_1 */

  /* USER CODE END FRAG_DECODER_IF_Write_1 */
  int32_t status = FLASH_OK;

#if (CACHING_MODE == 1)  /*write fragment in RAM - Caching mode*/
  UTIL_MEM_cpy_8(&UnfragmentedData[addr], data, size);
#else /* CACHING_MODE == 0 */

  if (HAL_FLASH_Unlock() == HAL_OK)
  {
    status = FLASH_IF_Write(FRAG_DECODER_DWL_REGION_START + addr, data, size, FRAG_DECODER_IF_RAM_buffer);
    HAL_FLASH_Lock();
  }
  else
  {
    status = FLASH_LOCK_ERROR;
  }

  if (status != FLASH_OK)
  {
    APP_LOG(TS_OFF, VLEVEL_M, "\r\n....... !! FLASH_IF_WRITE_ERROR: %d !! .......\r\n", status);
  }
#endif /* CACHING_MODE */
  if (status != FLASH_OK)
  {
    status = FLASH_ERROR;
  }
  return status;
  /* USER CODE BEGIN FRAG_DECODER_IF_Write_2 */

  /* USER CODE END FRAG_DECODER_IF_Write_2 */
}

int32_t FRAG_DECODER_IF_Read(uint32_t addr, uint8_t *data, uint32_t size)
{
  /* USER CODE BEGIN FRAG_DECODER_IF_Read_1 */

  /* USER CODE END FRAG_DECODER_IF_Read_1 */
#if (CACHING_MODE == 1)   /*Read fragment in RAM - Caching mode*/
  UTIL_MEM_cpy_8(data, &UnfragmentedData[addr], size);
#else /* CACHING_MODE == 0 */
  UTIL_MEM_cpy_8(data, (void *)(FRAG_DECODER_DWL_REGION_START + addr), size);
#endif /* CACHING_MODE */

  return FLASH_OK;
  /* USER CODE BEGIN FRAG_DECODER_IF_Read_2 */

  /* USER CODE END FRAG_DECODER_IF_Read_2 */
}

void FRAG_DECODER_IF_OnProgress(uint16_t fragCounter, uint16_t fragNb, uint8_t fragSize, uint16_t fragNbLost)
{
  /* USER CODE BEGIN FRAG_DECODER_IF_OnProgress_1 */

  /* USER CODE END FRAG_DECODER_IF_OnProgress_1 */
  APP_LOG(TS_OFF, VLEVEL_M, "\r\n....... FRAG_DECODER in Progress .......\r\n");
  APP_LOG(TS_OFF, VLEVEL_M, "RECEIVED    : %5d / %5d Fragments\r\n", fragCounter, fragNb);
  APP_LOG(TS_OFF, VLEVEL_M, "              %5d / %5d Bytes\r\n", fragCounter * fragSize, fragNb * fragSize);
  APP_LOG(TS_OFF, VLEVEL_M, "LOST        :       %7d Fragments\r\n\r\n", fragNbLost);

#if (INTEROP_TEST_MODE == 1)
  LED_Toggle(LED_BLUE);
#endif /* INTEROP_TEST_MODE == 1 */
  /* USER CODE BEGIN FRAG_DECODER_IF_OnProgress_2 */

  /* USER CODE END FRAG_DECODER_IF_OnProgress_2 */
}

void FRAG_DECODER_IF_OnDone(int32_t status, uint32_t size)
{
  /* USER CODE BEGIN FRAG_DECODER_IF_OnDone_1 */

  /* USER CODE END FRAG_DECODER_IF_OnDone_1 */
  APP_LOG(TS_OFF, VLEVEL_M, "\r\n....... FRAG_DECODER Finished .......\r\n");
  APP_LOG(TS_OFF, VLEVEL_M, "STATUS      : %d\r\n", status);

#if (INTEROP_TEST_MODE == 0)

  /* copy the file from RAM to FLASH & ASK to reboot the device*/
  if (FwUpdateAgentDataTransferFromRamToFlash(UnfragmentedData, SLOT_DWL_1_START, size) == HAL_OK)
  {
    APP_PRINTF("\r\n...... Transfer file RAM to Flash success --> Run  ......\r\n");
    FwUpdateAgentRun();
  }
  else
  {
    APP_PRINTF("\r\n...... Transfer file RAM to Flash Failed  ......\r\n");
  }

#else /* INTEROP_TEST_MODE*/
  uint32_t FileRxCrc = Crc32(UnfragmentedData, size);
  APP_LOG(TS_OFF, VLEVEL_M, "Size      : %d\r\n", size);
  APP_LOG(TS_OFF, VLEVEL_M, "CRC         : %08X\r\n\r\n", FileRxCrc);

  LED_Off(LED_BLUE);
#endif /* INTEROP_TEST_MODE == 1 */
  /* USER CODE BEGIN FRAG_DECODER_IF_OnDone_2 */

  /* USER CODE END FRAG_DECODER_IF_OnDone_2 */
}

/* USER CODE BEGIN EF */

/* USER CODE END EF */

/* Private Functions Definition -----------------------------------------------*/

/* USER CODE BEGIN PrFD */

/* USER CODE END PrFD */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
