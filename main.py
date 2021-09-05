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
        mem = round(psutil.virtual_memory().used / 1024 ** 2 / 1000, 1)
        process_name = ("⠀" * 10) + get_top_process()['name'].replace(".exe", "") + '\n'

        rpc.update(buttons=[
            {
                "label": f"CPU: {cpu_per}%",
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab"
            },

            {
                "label": f"RAM: {mem_per}% ({mem}GB)",
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab"
            }
        ],
            pid=get_top_process()['pid'],
            state=process_name,
            # start=l_time,
            # large_image=current_process if current_process != "" else "empty"
        )
        time.sleep(1)


if __name__ == "__main__":
    print("Discord Rich Presence launched!")

    main()
