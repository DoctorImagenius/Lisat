# 🛰️ Light-Based Satellite Communication Project (Demo Version)

This project demonstrates a basic wireless light+bluetooth communication system between a **Ground Station** and a **Satellite Module** using **ESP32 microcontrollers** and **Python**. This setup is designed for prototyping and educational purposes.

> ⚠️ **Note:** This is just a demo code. A complete Arduino-compatible library will be released soon for cleaner integration.

---

## 📁 Project Structure

| Folder / File                | Description |
|-----------------------------|-------------|
| `/solidworks/`              | SolidWorks design file for the satellite. |
| `/block_diagram/`           | System block diagram to understand the architecture. |
| `/circuit_diagram/`         | Wiring and circuit diagrams for ESP32 and modules. |
| `/esp32_rx_tx_code/`        | ESP32 Arduino code for TX (satellite-1) and RX (satellite-2) communication over light. |
| `/ground_station_python/`   | Python code for the ground station interface. |

---

## 🚀 Features

- 📡 **Bidirectional Communication** between ground and satellite modules using ESP32.
- 🧠 **Python-based Ground Station UI** for real-time command and response.
- 🔄 **Arduino-compatible code** for ESP32 boards (TX & RX).
- 🔧 SolidWorks designs and circuit diagrams for complete hardware understanding.
- 🔜 Future plans include a full **Arduino Library** for easier integration.

---

## 🛠️ Technologies Used

- **ESP32** (Microcontroller)
- **Python 3** (Ground station)
- **Arduino IDE** (For ESP32 programming)
- **SolidWorks** (Design)
- **Serial+Light Communication**

---


## 🧪 How to Run (Demo)

### Requirements:

- 2x ESP32 Boards
- Arduino IDE with ESP32 board package
- Python 3 and PySerial library
- USB cables for serial connection

### Setup:

1. **Upload** `tx_code_arduino` to the Satellite ESP32 (TX).
2. **Upload** `rx_code_arduino` to the Satellite ESP32 (RX).
3. Connect TX ESP32 to your PC ober bluetooth.
4. Run the Python ground station software
