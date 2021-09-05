from pypresence import Presence
import time
import psutil


def parse_id():
    client_id = None

    with open("client_id.txt", "r") as file:
        client_id = file.read()

    if client_id is None:
        print("client_id is not found! Please check client_id.txt")

    return client_id


def get_top_process():
    ''' creates process list and return top value (dict) by type [pid] [name] [username] '''
    list_of_proc_objects = []

    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
            list_of_proc_objects.append(pinfo)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    list_of_proc_objects_sorted = sorted(list_of_proc_objects, key=lambda procObj: procObj['vms'], reverse=True)

    return list_of_proc_objects_sorted[0]


def main():
    rpc = Presence(parse_id())

    rpc.connect()

    while True:
        cpu_per = round(psutil.cpu_percent(), 1)
        mem_per = round(psutil.virtual_memory().percent, 1)
        mem = round(psutil.virtual_memory().used / 1024 ** 2 / 1024, 1)
        
        #  aligns the process name in the profile
        #  with a word length of 9 and an indentation of 10, the text is perfectly centered
        #  so I compare the length of the process name with the reference
        
        #  works well, but could be better
        
        offset = 10

        process_name = ("⠀" * offset) + get_top_process()['name'].replace(".exe", "") + '\n'

        if len(process_name) - offset < 9:
            offset += 9 - (len(process_name) - offset)
        else:
            offset = 10

        process_name = ("⠀" * offset) + get_top_process()['name'].replace(".exe", "") + '\n'

        rpc.update(buttons=[
            {
                "label": f"CPU: {cpu_per}%",
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab" #  this is not rickroll, honestly
            },

            {
                "label": f"RAM: {mem_per}% ({mem}GB)",
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab"
            }
        ],
            pid=get_top_process()['pid'],  # does not affect anything but I'll leave it 
            state=process_name,
            # start=l_time,                  turn on if you need a timer by type (1m left...)
        )
        
        time.sleep(1) #  the higher the value, the lower the CPU consumption, but looks worse


if __name__ == "__main__":
    print("Discord Rich Presence launched!")

    main()
