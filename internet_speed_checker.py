from tkinter import *
import speedtest as st
import threading


def run_speedtest():
    sp = st.Speedtest()
    sp.get_servers()
    sp.get_best_server()
    down = str(round(sp.download() / (10**6), 3)) + " Mbps"
    up = str(round(sp.upload() / (10**6), 3)) + " Mbps"
    lab_down.config(text=down)
    lab_up.config(text=up)
    button.config(state=NORMAL, text="CHECK SPEED")  # reset button


def speedcheck():
    button.config(state=DISABLED, text="Testing...")  # disable button while running
    threading.Thread(target=run_speedtest).start()


sp = Tk()
sp.title("Internet Speed Tester")
sp.geometry("500x600")
sp.config(bg="lightblue")

lab = Label(sp, text="Internet Speed Test", font=("Times New Roman", 20), bg="lightblue")
lab.place(x=60, y=40, height=50, width=380)

lab = Label(sp, text="Download Speed", font=("Times New Roman", 20))
lab.place(x=60, y=130, height=50, width=380)

lab_down = Label(sp, text="00", font=("Times New Roman", 20))
lab_down.place(x=60, y=200, height=50, width=380)

lab = Label(sp, text="Upload Speed", font=("Times New Roman", 20))
lab.place(x=60, y=290, height=50, width=380)

lab_up = Label(sp, text="00", font=("Times New Roman", 20))
lab_up.place(x=60, y=360, height=50, width=380)

button = Button(sp, text="CHECK SPEED", font=("Times New Roman", 30, "bold"),
                relief=RAISED, command=speedcheck)
button.place(x=60, y=460, height=50, width=380)

sp.mainloop()
