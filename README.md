# Wacky and cute-( self claimed :} ) Music Player 

**Music Player v1** is a interactive  media device (media form: music, voice recording, text, gifs? maybe video) powered by an ESP32-S3. Designed as a personalized gift,to play unique music, affirmations,  every single day pre-programmed schedule. v2 will have an APi endpoint to post voice recordings over the internet.

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



### Power Board
![Power PCB](images/power_pcb.png)
![Power traces](images/power_route.png)
### 3D Model for Case
A custom 3d model case from fusion 360

![3D Model Render](images/3dcasefront.png)
![3D Model Render](images/3dcaseback.png)
![3D Model Render](images/backplate_3dmodel.png)
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
| **BMS Board** | Custom made battery management system      | 1        |
---


##  Project Structure

* `firmware/pages`: Contains the class logic for each UI state (`Daily`, `Music`, `Record`, `History`).
* `main.py`: The primary async loop and state machine handler.
* `setup.py`: Hardware initialization and pin mapping.
* `master.json`: The central database for the daily gift schedule.



## File Structure:

* `/3d Model`: Contains fusion and 3d printing files for the case.
* `/firmware`: Contains the code
* `Kicad`: Kicad files (both power and main board)
       * `Power_kicad`: Custom made bms system kicad project
       * `main_kicad`: main pcb kicad project
* `/images`: For images of README.md

---


*Created with love❤️.*