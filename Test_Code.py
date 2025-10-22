from machine import Pin, UART
import time, ujson

# === UART Setup ===
uart = UART(0, baudrate=921600, tx=Pin(0), rx=Pin(1))

# === Motor Setup ===
IN1 = Pin(2, Pin.OUT)
IN2 = Pin(3, Pin.OUT)
IN3 = Pin(4, Pin.OUT)
IN4 = Pin(5, Pin.OUT)

def stop(): IN1.value(0); IN2.value(0); IN3.value(0); IN4.value(0)
def forward(): IN1.value(1); IN2.value(0); IN3.value(1); IN4.value(0)
def backward(): IN1.value(0); IN2.value(1); IN3.value(0); IN4.value(1)
def left(): IN1.value(0); IN2.value(1); IN3.value(1); IN4.value(0)
def right(): IN1.value(1); IN2.value(0); IN3.value(0); IN4.value(1)

# === Classification Mapping ===
CLASS_NAMES = ["Rock", "Paper", "Scissors"]

def invoke_once(timeout_ms=300):
    """Run one inference and parse result"""
    while uart.any(): uart.read()  # flush
    uart.write("AT+INVOKE=1,0,1\r")
    buf = b""
    depth = 0
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < timeout_ms:
        if uart.any():
            data = uart.read()
            for ch in data:
                buf += bytes([ch])
                if ch == ord("{"): depth += 1
                elif ch == ord("}"): depth -= 1
                if depth == 0:
                    raw = buf[buf.find(b"{"):]
                    try:
                        js = ujson.loads(raw)
                        buf = b""
                        if js.get("type") == 1:
                            return js["data"]
                    except: buf=b""
        else:
            time.sleep_ms(2)
    return None

# === Main Loop ===
print("🚀 Grove Vision AI + L298N Motors")

while True:
    data = invoke_once(timeout_ms=400)
    if data is None:
        print("⏱️ Timeout")
        stop()
        continue

    if "classes" in data:
        classes = data["classes"]
        if classes:
            score, label = classes[0]  # first prediction
            name = CLASS_NAMES[label] if label < len(CLASS_NAMES) else str(label)
            print(f"🎯 {name} ({label}) → {score}%")

            # ===== Motor Logic Based on Class =====
            if name == "Rock":
                forward()
            elif name == "Paper":
                backward()
            elif name == "Scissors":
                left()
            else:
                stop()
    else:
        stop()
    time.sleep(1)
