import os

def list_all_songs():
    import context
    
    try:
        os_list = os.listdir("/sd")
    except Exception as e:
        os_list = []
        print("Error:" ,e)
        
    music_list = []
    for file in os_list:
        if file.lower().endswith(".wav"):
            title = file[:-4] #grabs the title - removing the .wav
            song = {
                "title":title,
                "filename":file
                }
            music_list.append(song) #storing the dicts on array
            
    #at last push the array's context to context file for global access
            
    context.songs_list = music_list
    print(f"Loaded {len(music_list)} into context")
    
            
    

def connect_to_wifi():
    import network
    import time 
    from context import SSID, PASS
            
    sta_if = network.WLAN(0)
    
    if not sta_if.isconnected():
        print("Activating Wi-Fi interface...")
        sta_if.active(True)
        

        time.sleep(0.5) 
        
        print("Connecting to wifi...")
        sta_if.connect(SSID, PASS)      
        attempts = 0
        while not sta_if.isconnected():
            print(f"Waiting for connection... Attempt {attempts}")
            time.sleep(1)
            attempts += 1
            
            if attempts % 10 == 0:
                print("Still trying, re-sending credentials...")
                sta_if.connect(SSID, PASS)
            
    print("Connected to wifi with IP:", sta_if.ifconfig()[0])
        

        
def get_time():
    from context import API_URL
    import urequests
    import context
    try:
        print("Fetching time from API")
        response = urequests.get(API_URL)
        data = response.json()
        current_time = data.get("utc_time", "Time not found")
        date = current_time.split("T")[0]
        print("Current date fetched:", date)
        context.current_date = date
        response.close()
    
    except Exception as e:
        print("Error fetching time:", e)
        return None
    
    
def get_today_present():
    import context
    import json
    try:
        with open("master.json" , "r") as file:
            data = json.load(file)
            
    except Exception as e:
        print(f"Couldnt read the file. {e}")
    
    if context.current_date: #if there is a date then checks the file 
        if context.current_date in data:
            today_data = data[context.current_date]
            context.today_present = today_data
            print("Today's present found and saved")
        else:
            print("There seems to be no present for today")
            

