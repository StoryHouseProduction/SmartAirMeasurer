from machine import Pin, ADC
import time
import utime
from dht import DHT11   # if the sensor is DHT11, import DHT11 instead of DHT22
from mq135 import MQ135
import ujson

# Setupo DHT 11 & MQ135
dht = DHT11(Pin(0)) # DHT11 sensor is connected to GPIO 0
mq135 = MQ135(27) # MQ135 sensor is connected to GPIO 27 (ADC1)

# Setup Sharp GP2Y1010AU0F Dust Sensor.
measure_pin = ADC(Pin(26))  # Connect output of the sensor to GPIO 26 (ADC1)
led_power = Pin(12, Pin.OUT) # Connect LED to GPIO 10
led_power.value(1)  # Initialize LED power to off

# Variables for dust sensor
sampling_time = 280
delta_time = 40
sleep_time = 9680

# Get Dust Sensor readings
def measure_dust_density():
    # Turn on LED (active low for most dust sensors)
    led_power.low()
    utime.sleep_us(sampling_time)
    
    # Read analog value (0-65535 range)
    vo_measured = measure_pin.read_u16()
    utime.sleep_us(delta_time)
    
    # Turn off LED
    led_power.high()
    utime.sleep_us(sleep_time)
    
    # Convert to voltage (Pico uses 3.3V reference)
    calc_voltage = vo_measured * (3.3 / 65535.0)
    
    # Calculate dust density 
    # Note: You might need to calibrate this formula for your specific sensor
    dust_density = 170 * calc_voltage - 0.1
    
    return dust_density

while True:
    # Get DHT22 sensor readings
    dht.measure()
    temp = dht.temperature()
    hum = dht.humidity()

    # Get MQ135 sensor readings
    rzero = mq135.get_rzero()
    crzero = mq135.get_corrected_rzero(temp, hum)
    res = mq135.get_resistance()
    ppm = mq135.get_ppm().real
    cppm = mq135.get_corrected_ppm(temp, hum).real

    # Create JSON object
    json_data = {
        "temp": abs(temp),
        "humid": abs(hum),
        "carbon_ppm": abs(cppm),
        "dust_mg": measure_dust_density()
    }
    
    # Serialize JSON and print to serial
    json_str = ujson.dumps(json_data)
    print(json_str)
   
    # delay of 2 secs because DHT22 takes a reading once every 2 secs
    time.sleep(2)