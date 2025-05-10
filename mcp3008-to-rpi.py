import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
import time
from adafruit_mcp3xxx.analog_in import AnalogIn
from pythonosc.udp_client import SimpleUDPClient

ip = "127.0.0.1"
port = 5009
client = SimpleUDPClient(ip, port)

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select) for the single MCP3008 chip
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

# Create arrays to store our different types of inputs
pot_channels = []
toggle_channels = []
pushbutton_channels = []

# We'll use the first 3 pins for potentiometers
for pin in [MCP.P0, MCP.P1, MCP.P2]:
    pot_channels.append(AnalogIn(mcp, pin))

# Use the next 3 pins for toggle switches
for pin in [MCP.P3, MCP.P4, MCP.P5]:
    toggle_channels.append(AnalogIn(mcp, pin))

# Use the last 2 pins for pushbuttons
for pin in [MCP.P6, MCP.P7]:
    pushbutton_channels.append(AnalogIn(mcp, pin))

while True:
    # Read and send potentiometer values
    for i, chan in enumerate(pot_channels):
        print(f'Raw ADC Value Pot {i}: {chan.value}')
        print(f'ADC Voltage Pot {i}: {chan.voltage}V')
        client.send_message(f"/POT{i}", chan.value)
    
    # Read and send toggle switch values
    for i, chan in enumerate(toggle_channels):
        toggle_state = 1 if chan.value > 512 else 0  # Assume a threshold for on/off state
        print(f'Toggle {i}: {"ON" if toggle_state else "OFF"}')
        client.send_message(f"/TOGGLE{i}", toggle_state)
    
    # Read and send pushbutton values
    for i, chan in enumerate(pushbutton_channels):
        button_state = 1 if chan.value > 512 else 0  # Assume a threshold for pressed/released state
        print(f'Pushbutton {i}: {"PRESSED" if button_state else "RELEASED"}')
        client.send_message(f"/BUTTON{i}", button_state)
    
    time.sleep(0.001)