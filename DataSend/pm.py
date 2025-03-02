import machine
import utime

# Pin configuration
measure_pin = machine.ADC(26)  # ADC input pin
led_power = machine.Pin(12, machine.Pin.OUT)  # LED power pin

# Timing constants
sampling_time = 280  # microseconds
delta_time = 40      # microseconds
sleep_time = 9680    # microseconds

def main():
    while True:
        # Power on the LED
        led_power.low()
        utime.sleep_us(sampling_time)
        
        # Read the dust value
        vo_measured = measure_pin.read_u16()  # Pico uses 16-bit ADC (0-65535)
        
        utime.sleep_us(delta_time)
        
        # Turn the LED off
        led_power.high()
        utime.sleep_us(sleep_time)
        
        # Convert to voltage (Pico ADC is 0-65535 mapped to 0-3.3V)
        calc_voltage = vo_measured * (3.3 / 65535)
        
        # Calculate dust density
        # Using the same linear equation from the original code
        dust_density = 0.17 * calc_voltage - 0.1
        
        # Print results
        print(f"Raw Signal Value (0-65535): {vo_measured}")
        print(f"Voltage: {calc_voltage:.4f}")
        print(f"Dust Density: {dust_density:.4f}")
        
        # Delay between measurements
        utime.sleep(1)

# Run the main function
if __name__ == '__main__':
    main()