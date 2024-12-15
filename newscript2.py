import network
import time
import machine
import math
import utime
from mq135 import MQ135
from umqtt.simple import MQTTClient

# ---------------------------
# Настройки Wi-Fi и MQTT
# ---------------------------
WIFI_SSID = "Ufanet_40"
WIFI_PASSWORD = "72921478"
MQTT_BROKER_IP = "192.168.0.152"
MQTT_CLIENT_ID = "esp8266_sensors"
MQTT_TOPIC_MQ135_PPM = "sensors/mq135/ppm"
MQTT_TOPIC_MQ135_RAW = "sensors/mq135/raw_adc"  # Новый топик для сырых значений
MQTT_TOPIC_ULTRASONIC = "sensors/ultrasonic/distance"

# ---------------------------
# Функция подключения к Wi-Fi
# ---------------------------
def connect_wifi():
    station = network.WLAN(network.STA_IF)
    if not station.isactive():
        station.active(True)
    if not station.isconnected():
        print("Подключение к WiFi...")
        station.connect(WIFI_SSID, WIFI_PASSWORD)
        while not station.isconnected():
            time.sleep(1)
    print("WiFi подключен, IP адрес:", station.ifconfig()[0])

# ---------------------------
# Инициализация датчиков
# ---------------------------
# MQ135 подключен к A0 (ADC0)
temperature = 25.0
humidity = 35.0

mq135 = MQ135(pin=0)

# Ультразвуковой датчик
trig = machine.Pin(13, machine.Pin.OUT)  # D7
echo = machine.Pin(12, machine.Pin.IN)   # D6

def get_distance():
    trig.off()
    utime.sleep_us(2)
    trig.on()
    utime.sleep_us(10)
    trig.off()

    # Ждем начала эха
    timeout = utime.ticks_add(utime.ticks_us(), 30000)  # Таймаут 30 мс
    while echo.value() == 0:
        if utime.ticks_diff(timeout, utime.ticks_us()) <= 0:
            return None
    t1 = utime.ticks_us()

    # Ждем окончания эха
    timeout = utime.ticks_add(utime.ticks_us(), 30000)
    while echo.value() == 1:
        if utime.ticks_diff(timeout, utime.ticks_us()) <= 0:
            return None
    t2 = utime.ticks_us()

    duration = utime.ticks_diff(t2, t1)
    cm = duration / 58.0
    return cm

# ---------------------------
# Подключение к MQTT
# ---------------------------
def connect_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER_IP)
    client.connect()
    print("Подключено к MQTT брокеру по адресу {}".format(MQTT_BROKER_IP))
    return client

# ---------------------------
# Основная функция
# ---------------------------
def main():
    # connect_wifi()
    client = connect_mqtt()

    while True:
        try:
            # Чтение MQ135
            ppm = mq135.get_ppm()
            corrected_ppm = mq135.get_corrected_ppm(temperature, humidity)

            # Чтение сырых значений АЦП
            raw_adc = machine.ADC(0).read()  # Считывание сырых значений АЦП

            # Чтение ультразвукового датчика
            distance = get_distance()

            # Печать значений в консоль
            print("MQ135 PPM:", ppm, "Corrected PPM:", corrected_ppm, "Raw ADC:", raw_adc, "Distance:", distance)

            # Публикация в MQTT
            if corrected_ppm != -1:
                client.publish(MQTT_TOPIC_MQ135_PPM, str(corrected_ppm))

            # Публикация сырых значений АЦП
            client.publish(MQTT_TOPIC_MQ135_RAW, str(raw_adc))

            if distance is not None:
                client.publish(MQTT_TOPIC_ULTRASONIC, "{:.2f}".format(distance))

        except Exception as e:
            print("Ошибка во время цикла:", e)
            try:
                client = connect_mqtt()  # Попытка переподключиться
            except:
                pass

        time.sleep(5)  # Пауза между отправками, например 5 секунд

if __name__ == "__main__":
    main()
