# Near365 Gift 🎁

**Near365** is a smart, interactive daily gift device powered by an ESP32-S3. Designed as a personalized keepsake, it delivers unique music, affirmations, and helps brighten up someone's day, every single day pre-programmed schedule.

---

## Features

* **Daily Present:** Automatically fetches unique content (music and text(affiramtions/notes)) from an SD card based on the current date.
* **High-Fidelity Audio:** Uses I2S protocol with a MAX98357A DAC for clear, non-blocking WAV file playback.
* **Voice Recorder:** Record and save voice memos directly to the SD card for future playback ** Plans to stream it over the internet
* **Music Player:** Plays music playlists from the sd card
* **Peculiar Cute design** Cute 3d model case enclosure with a tounge sticking out 😛

---

##  Hardware Design

### Schematic
The system integrates an ESP32-S3 with I2S audio, SPI SD card communication, and I2C/SPI display interfacing.

![Schematic](images/schematic.png)
![Schematic](images/esp32wroom.png)


### PCB Design
A custom 2-layer PCB design from kicad.

![PCB Layout](images/pcb.png)
![PCB Layout](images/pcb3dmodel.png)

### 3D Model for Case
A custom 3d model case from fusion 360

![3D Model Render](images/3dcasefront.png)
![3D Model Render](images/3dcaseback.png)


---
##  Bill of Materials (BOM)

| Component           | Description                                  | Quantity |
| :------------------ | :------------------------------------------- | :------- |
| **Microcontroller** | ESP32-S3 (WROOM-1-N16R8)                     | 1        |
| **Display** | 2.4" TFT LCD (ILI9341 Driver)                | 1        |
| **Audio DAC/Amp** | MAX98357A I2S Class D Amplifier              | 1        |
| **Speaker** | 3W 4-Ohm Internal Speaker                    | 1        |
| **Rotary Encoder** | EC11 Encoder with Push-Button Switch         | 1        |
| **Touch Sensor** | TTP223 Capacitive Touch Module (Soft Power)  | 1        |
| **SD card module** | Adafruit Micro SD Card Breakout Board      | 1        |
| **Microphone** | INMP441 I2S Digital Omnidirectional Mic      | 1        |
| **RTC Module** | DS3231 High-Precision I2C RTC                | 1        |
| **Storage Card** | 16GB Micro SD Card       | 1        |

---
Find the full BOM in the CSV file: [near365.csv](./near365.csv)

##  Project Structure

* `/pages`: Contains the class logic for each UI state (`Daily`, `Music`, `Record`, `History`).
* `/assets`: Fonts (`ArcadePix`), icons, and images.
* `main.py`: The primary async loop and state machine handler.
* `setup.py`: Hardware initialization and pin mapping.
* `master.json`: The central database for the daily gift schedule.

---


*Created with love❤️.*