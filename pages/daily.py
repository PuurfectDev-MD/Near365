import json
import uasyncio as asyncio
from machine import I2S, Pin

class Daily:
    def __init__(self, system):
        self.system = system
        self.wav = None
        self.playing = False
        
        self.PLAY = 0
        self.STOP = 1
        self.state = self.STOP
        
        # Pre-allocate buffers to prevent memory fragmentation
        self.wav_samples = bytearray(10000)
        self.wav_samples_mv = memoryview(self.wav_samples)
        self.silence = bytearray(1000)

    async def run_page_loop(self, target_date):
        """Main loop for the Daily Page. Returns to menu when 'Back' is pressed."""
        print(f"Entering Daily Page: {target_date}")
        
        # Initial Screen Draw
        self.system.display.clear()
        self.system.display.draw_text(10, 10, "--- Daily Present ---", 0xFFFF)
        
        # Start the search and audio playback
        found = self.start_audio(target_date)
        
        if not found:
            # If nothing found, wait 2 seconds then auto-exit back to menu
            await asyncio.sleep(2)
            return

        # 3. Local Loop: until user exits
        while True:
            #btn 2 is the back button
            if self.system.controls.btn2.value() == 0:
                print("Exiting Daily Page...")
                self.stop_audio()
                break # Exit the while loop
            
            # Optional: Visual feedback while playing
            if self.playing:
                # to incoporte LVGL library here
                pass

            # Handle Encoder  - for volume
            if self.system.controls.read_encoder():
                vol = self.system.controls.map_encoder_values(10)
                # system.i2s.volume(vol) have to check if this work or not
            
            await asyncio.sleep_ms(50)

    def start_audio(self, target_date):
        try:           #location for master
            with open("/sd/master.json", "r") as f:
                data = json.load(f)
            
            presents = data.get("presents", [])
            match = next((item for item in presents if item["date"] == target_date), None)
            
            if match:
                file_path = f"/sd/{match['music']}"
                message = match["message"]
                
                # Update UI with the message
                self.system.display.draw_text(10, 80, "Message:", 0x07E0) 
                self.system.display.draw_text(10, 110, message, 0xFFFF)
                
                # Prepare WAV file
                if self.wav: self.wav.close()
                self.wav = open(file_path, "rb")
                self.wav.seek(44) # Skip WAV header
                
                # Set up Non-Blocking I2S IRQ
                self.state = self.PLAY
                self.playing = True
                self.system.i2s.irq(self.i2s_callback)
                
                # Kickstart with a small write
                self.system.i2s.write(self.silence)
                return True
            else:
                self.system.display.draw_text(10, 100, "No data for today!", 0xF800) # Red
                return False

        except Exception as e:
            print(f"Daily Start Error: {e}")
            return False

    def stop_audio(self):
        """Cleanup audio resources."""
        self.state = self.STOP
        self.playing = False
        if self.wav:
            self.wav.close()
            self.wav = None
        # Write silence to clear the I2S hardware buffer
        self.system.i2s.write(self.silence)

    def i2s_callback(self, arg):
        """Interrupt Service Routine: Runs whenever I2S needs more data."""
        if self.state == self.PLAY and self.wav:
            num_read = self.wav.readinto(self.wav_samples_mv)
            
            if num_read == 0:
                # End of file reached
                self.state = self.STOP
                self.playing = False
                self.wav.close()
                self.wav = None
                self.system.i2s.write(self.silence)
                print("Playback complete.")
            else:
                # Write next chunk to I2S
                self.system.i2s.write(self.wav_samples_mv[:num_read])