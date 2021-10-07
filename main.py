import win32process
import win32gui
from win32gui import GetWindowText, GetForegroundWindow
from pypresence import Presence
import time
import psutil


def parse():
    ''' returns a dictionary with delay_id and delay '''

    client_id = None
    delay = None

    with open("client_id.txt", "r") as file:
        client_id = file.readline()
        client_id = client_id.split("=")[1]  # the file will look like this (client_id=None)
                                             # and I will split the string in two and take the second part

        delay = file.readline()
        delay = float(delay.split("=")[1])

    if client_id is None:
        print("client_id is not found! Please check client_id.txt")

    return {"client_id": client_id, "delay": delay}


def get_top_process():
    process = GetWindowText(GetForegroundWindow())

    print(f"top process {process}")

    return process


def get_top_process_pid():
    hwnd = win32gui.FindWindow(None, get_top_process())

    threadid, pid = win32process.GetWindowThreadProcessId(hwnd)

    return pid


def main():
    rpc = Presence(parse()["client_id"])

    rpc.connect()

    print(f"\nDEBUG | client_id: {parse()['client_id']}")
    print(f"DEBUG | delay: {parse()['delay']}")

    while True:
        cpu_per = round(psutil.cpu_percent(), 1)
        mem_per = round(psutil.virtual_memory().percent, 1)
        mem = round(psutil.virtual_memory().used / 1024 ** 2 / 1024, 1)

        process_name = get_top_process() + '\n'

        rpc.update(buttons=[
            {
                "label": f"CPU: {cpu_per}%",
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab"  # this is not rickroll, honestly
            },

            {
                "label": f"RAM: {mem_per}% ({mem}GB)",
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab"
            }
        ],
            pid=get_top_process_pid(),
            state=process_name,
            # start=l_time,                # turn on if you need a timer by type (1m left...)
        )

        time.sleep(parse()["delay"])  # the higher the value, the lower the CPU consumption, but looks worse


if __name__ == "__main__":
    print("Discord Rich Presence launched!")

    main()
