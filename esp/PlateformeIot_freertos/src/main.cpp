#include <stdio.h>
#include <string.h>
#include <inttypes.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "esp_system.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "esp_bt.h"
#include "esp_bt_main.h"
#include "esp_gap_bt_api.h"
#include "esp_bt_device.h"
#include "esp_spp_api.h"
#include "driver/uart.h"

#define SPP_TAG "SPP_ACCEPTOR"
#define UART_NUM UART_NUM_2
#define BUF_SIZE 1024

static QueueHandle_t uart_queue;
static QueueHandle_t bt_queue;

// Prototypes des fonctions
void bt_receive_task(void *pvParameters);
void uart_receive_task(void *pvParameters);
void data_process_task(void *pvParameters);
void esp_spp_cb(esp_spp_cb_event_t event, esp_spp_cb_param_t *param);
void traitementReceptionBluetooth(const char* data);

void app_main(void)
{
    esp_err_t ret;

    // Initialisation de NVS
    ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    // Initialisation du Bluetooth
    ESP_ERROR_CHECK(esp_bt_controller_mem_release(ESP_BT_MODE_BLE));

    esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();
    if ((ret = esp_bt_controller_init(&bt_cfg)) != ESP_OK) {
        ESP_LOGE(SPP_TAG, "%s initialize controller failed: %s\n", __func__, esp_err_to_name(ret));
        return;
    }

    if ((ret = esp_bt_controller_enable(ESP_BT_MODE_CLASSIC_BT)) != ESP_OK) {
        ESP_LOGE(SPP_TAG, "%s enable controller failed: %s\n", __func__, esp_err_to_name(ret));
        return;
    }

    esp_bluedroid_init_with_cfg_t bt_init_cfg = {
        .supported_profiles_mask = ESP_BLUEDROID_PROFILES_SPP
    };
    if ((ret = esp_bluedroid_init_with_cfg(&bt_init_cfg)) != ESP_OK) {
        ESP_LOGE(SPP_TAG, "%s initialize bluedroid failed: %s\n", __func__, esp_err_to_name(ret));
        return;
    }

    if ((ret = esp_bluedroid_enable()) != ESP_OK) {
        ESP_LOGE(SPP_TAG, "%s enable bluedroid failed: %s\n", __func__, esp_err_to_name(ret));
        return;
    }

    if ((ret = esp_spp_register_callback(esp_spp_cb)) != ESP_OK) {
        ESP_LOGE(SPP_TAG, "%s spp register failed: %s\n", __func__, esp_err_to_name(ret));
        return;
    }

    esp_spp_cfg_t spp_cfg = {
        .mode = ESP_SPP_MODE_CB,
        .enable_l2cap_ertm = true,
        .tx_buffer_size = 0, // Utilisez la taille de buffer par défaut
    };
    if ((ret = esp_spp_enhanced_init(&spp_cfg)) != ESP_OK) {
        ESP_LOGE(SPP_TAG, "%s spp init failed: %s\n", __func__, esp_err_to_name(ret));
        return;
    }

    // Configuration UART
    uart_config_t uart_config = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS,
        .parity    = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .rx_flow_ctrl_thresh = 122,
        .source_clk = UART_SCLK_REF_TICK
    };
    uart_param_config(UART_NUM, &uart_config);
    uart_set_pin(UART_NUM, 17, 16, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    uart_driver_install(UART_NUM, BUF_SIZE * 2, 0, 0, NULL, 0);

    // Création des files d'attente
    bt_queue = xQueueCreate(10, BUF_SIZE);
    uart_queue = xQueueCreate(10, BUF_SIZE);

    // Création des tâches
    xTaskCreate(bt_receive_task, "bt_receive_task", 2048, NULL, 5, NULL);
    xTaskCreate(uart_receive_task, "uart_receive_task", 2048, NULL, 5, NULL);
    xTaskCreate(data_process_task, "data_process_task", 4096, NULL, 4, NULL);
}

void bt_receive_task(void *pvParameters)
{
    (void)pvParameters; // Marque le paramètre comme non utilisé
    while (1) {
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

void uart_receive_task(void *pvParameters)
{
    (void)pvParameters; // Marque le paramètre comme non utilisé
    uint8_t* data = (uint8_t*) malloc(BUF_SIZE);
    while (1) {
        int len = uart_read_bytes(UART_NUM, data, BUF_SIZE, 20 / portTICK_PERIOD_MS);
        if (len > 0) {
            xQueueSend(uart_queue, data, portMAX_DELAY);
        }
    }
}

void data_process_task(void *pvParameters)
{
    (void)pvParameters; // Marque le paramètre comme non utilisé
    uint8_t data[BUF_SIZE];
    while (1) {
        if (xQueueReceive(bt_queue, data, portMAX_DELAY) == pdTRUE) {
            // Traitement des données Bluetooth
            ESP_LOGI(SPP_TAG, "Received from BT: %s", data);
            traitementReceptionBluetooth((const char*)data);
        }

        if (xQueueReceive(uart_queue, data, 0) == pdTRUE) {
            // Traitement des données UART
            ESP_LOGI(SPP_TAG, "Received from UART: %s", data);
            // Traitement des données UART comme dans la version Arduino
            if (data[0] == '0') {
                if (data[1] == '1') {
                    // Envoi du dev eui
                    esp_spp_write(0, strlen((char*)data) - 2, data + 2);
                }
            }
        }
    }
}

void esp_spp_cb(esp_spp_cb_event_t event, esp_spp_cb_param_t *param)
{
    switch (event) {
        case ESP_SPP_INIT_EVT:
            ESP_LOGI(SPP_TAG, "ESP_SPP_INIT_EVT");
            esp_bt_dev_set_device_name("Plateforme iot");
            esp_bt_gap_set_scan_mode(ESP_BT_CONNECTABLE, ESP_BT_GENERAL_DISCOVERABLE);
            esp_spp_start_srv(ESP_SPP_SEC_NONE,ESP_SPP_ROLE_SLAVE, 0, "SPP_SERVER");
            break;
        case ESP_SPP_DATA_IND_EVT:
            ESP_LOGI(SPP_TAG, "ESP_SPP_DATA_IND_EVT len=%"PRIu32" handle=%"PRIu32, param->data_ind.len, param->data_ind.handle);
            xQueueSend(bt_queue, param->data_ind.data, portMAX_DELAY);
            break;
        default:
            break;
    }
}

void traitementReceptionBluetooth(const char* data)
{
    char buffer[BUF_SIZE];
    strncpy(buffer, data, BUF_SIZE);
    
    char *token = strtok(buffer, ",");
    int i = 0;
    char timestamp[20], latitude[20], longitude[20], altitude[20], luminosite[20], 
         vitesseAngulaireX[20], vitesseAngulaireY[20], vitesseAngulaireZ[20], 
         pression[20], accelerationX[20], accelerationY[20], accelerationZ[20], 
         angle[20], azimut[20];

    while (token != NULL) {
        switch (i) {
            case 0:
                break;
            case 1:
                strncpy(timestamp, token, sizeof(timestamp));
                break;
            case 2:
                strncpy(latitude, token, sizeof(latitude));
                break;
            case 3:
                strncpy(longitude, token, sizeof(longitude));
                break;
            case 4:
                strncpy(altitude, token, sizeof(altitude));
                break;
            case 5:
                strncpy(luminosite, token, sizeof(luminosite));
                break;
            case 6:
                strncpy(vitesseAngulaireX, token, sizeof(vitesseAngulaireX));
                break;
            case 7:
                strncpy(vitesseAngulaireY, token, sizeof(vitesseAngulaireY));
                break;
            case 8:
                strncpy(vitesseAngulaireZ, token, sizeof(vitesseAngulaireZ));
                break;
            case 9:
                strncpy(pression, token, sizeof(pression));
                break;
            case 10:
                strncpy(accelerationX, token, sizeof(accelerationX));
                break;
            case 11:
                strncpy(accelerationY, token, sizeof(accelerationY));
                break;
            case 12:
                strncpy(accelerationZ, token, sizeof(accelerationZ));
                break;
            case 13:
                strncpy(angle, token, sizeof(angle));
                break;
            case 14:
                strncpy(azimut, token, sizeof(azimut));
                break;
            default:
                break;
        }
        token = strtok(NULL, ",");
        i++;
    }

    char loraPayload[BUF_SIZE];
    snprintf(loraPayload, BUF_SIZE, "2%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n",
             timestamp, latitude, longitude, altitude, luminosite, 
             vitesseAngulaireX, vitesseAngulaireY, vitesseAngulaireZ, 
             pression, accelerationX, accelerationY, accelerationZ, 
             angle, azimut);

    uart_write_bytes(UART_NUM, loraPayload, strlen(loraPayload));
    ESP_LOGI(SPP_TAG, "Sent to UART: %s", loraPayload);
}