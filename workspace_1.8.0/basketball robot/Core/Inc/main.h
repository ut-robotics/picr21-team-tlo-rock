/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2021 STMicroelectronics.
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
#define TIM2_CH1_M_1_PWM_1_Pin GPIO_PIN_0
#define TIM2_CH1_M_1_PWM_1_GPIO_Port GPIOA
#define TIM2_CH2_M_1_PWM_2_Pin GPIO_PIN_1
#define TIM2_CH2_M_1_PWM_2_GPIO_Port GPIOA
#define TIM15_CH1_M_3_PWM_1_Pin GPIO_PIN_2
#define TIM15_CH1_M_3_PWM_1_GPIO_Port GPIOA
#define TIM15_CH1_M_3_PWM_2_Pin GPIO_PIN_3
#define TIM15_CH1_M_3_PWM_2_GPIO_Port GPIOA
#define TIM3_CH2___ENC_B_Pin GPIO_PIN_4
#define TIM3_CH2___ENC_B_GPIO_Port GPIOA
#define GPIO_BALL_SENSOR_Pin GPIO_PIN_5
#define GPIO_BALL_SENSOR_GPIO_Port GPIOA
#define TIM3_CH1___ENC_A_Pin GPIO_PIN_6
#define TIM3_CH1___ENC_A_GPIO_Port GPIOA
#define TIM17_CH1_THW_SERVO_Pin GPIO_PIN_7
#define TIM17_CH1_THW_SERVO_GPIO_Port GPIOA
#define GPIO_DRV_OFF_Pin GPIO_PIN_0
#define GPIO_DRV_OFF_GPIO_Port GPIOB
#define TIM2_CH2_M_2_PWM_1_Pin GPIO_PIN_9
#define TIM2_CH2_M_2_PWM_1_GPIO_Port GPIOA
#define TIM2_CH2_M_2_PWM_2_Pin GPIO_PIN_10
#define TIM2_CH2_M_2_PWM_2_GPIO_Port GPIOA
#define TIM8_CH1_ENC_A_Pin GPIO_PIN_15
#define TIM8_CH1_ENC_A_GPIO_Port GPIOA
#define TIM16_CH1_THW_MOTOR_Pin GPIO_PIN_4
#define TIM16_CH1_THW_MOTOR_GPIO_Port GPIOB
#define TIM4_CH1_ENC_A_Pin GPIO_PIN_6
#define TIM4_CH1_ENC_A_GPIO_Port GPIOB
#define TIM4_CH2_ENC_B_Pin GPIO_PIN_7
#define TIM4_CH2_ENC_B_GPIO_Port GPIOB
#define TIM8_CH2_ENC_B_Pin GPIO_PIN_8
#define TIM8_CH2_ENC_B_GPIO_Port GPIOB
/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
