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
    
            
    
