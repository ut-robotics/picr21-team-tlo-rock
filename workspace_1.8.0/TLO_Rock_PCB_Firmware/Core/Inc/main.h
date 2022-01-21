/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2022 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32g4xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

void HAL_TIM_MspPostInit(TIM_HandleTypeDef *htim);

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define TIM2_CH1_M1_PWM_Pin GPIO_PIN_0
#define TIM2_CH1_M1_PWM_GPIO_Port GPIOA
#define M1_DIR_Pin GPIO_PIN_1
#define M1_DIR_GPIO_Port GPIOA
#define TIM_15_CH1_M3_PWM_Pin GPIO_PIN_2
#define TIM_15_CH1_M3_PWM_GPIO_Port GPIOA
#define M3_DIR_Pin GPIO_PIN_3
#define M3_DIR_GPIO_Port GPIOA
#define TIM3_CH2_ENCB_Pin GPIO_PIN_4
#define TIM3_CH2_ENCB_GPIO_Port GPIOA
#define BALL_SENSOR_Pin GPIO_PIN_5
#define BALL_SENSOR_GPIO_Port GPIOA
#define TIM3_CH1_ENCA_Pin GPIO_PIN_6
#define TIM3_CH1_ENCA_GPIO_Port GPIOA
#define TIM17_CH1_THW_SERVO_Pin GPIO_PIN_7
#define TIM17_CH1_THW_SERVO_GPIO_Port GPIOA
#define DRV_OFF_Pin GPIO_PIN_0
#define DRV_OFF_GPIO_Port GPIOB
#define TIM2_CH3_M2_PWM_Pin GPIO_PIN_9
#define TIM2_CH3_M2_PWM_GPIO_Port GPIOA
#define M2_DIR_Pin GPIO_PIN_10
#define M2_DIR_GPIO_Port GPIOA
#define TIM8_CH1_ENCA_Pin GPIO_PIN_15
#define TIM8_CH1_ENCA_GPIO_Port GPIOA
#define NSLEEP_PWM_Pin GPIO_PIN_3
#define NSLEEP_PWM_GPIO_Port GPIOB
#define TIM16_CH1_THW_MOTOR_Pin GPIO_PIN_4
#define TIM16_CH1_THW_MOTOR_GPIO_Port GPIOB
#define TIM4_CH1_ENCA_Pin GPIO_PIN_6
#define TIM4_CH1_ENCA_GPIO_Port GPIOB
#define TIM4_CH2_ENCB_Pin GPIO_PIN_7
#define TIM4_CH2_ENCB_GPIO_Port GPIOB
#define TIM8_CH2_ENCB_Pin GPIO_PIN_8
#define TIM8_CH2_ENCB_GPIO_Port GPIOB
/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
