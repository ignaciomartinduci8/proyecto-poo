from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage
from Controlador import Controlador
from Servidor import Servidor
from DataLog import DataLog

GREEN = "\033[92m"
RESET = "\033[0m"
ROJO = "\033[91m"
LIGHT_BLUE = "\033[94m"
IDENTATION = f"{LIGHT_BLUE}>{RESET}"


class GUI:
    def __init__(self,user):
        self.servidor1 = None
        self.dataLog = DataLog(user)
        self.controlador = Controlador(self.dataLog)
        self.serverUser = user
        self.dataLog.logProgram(True)

        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(r"./build/assets/frame0")

        self.window=Tk()
        self.window.geometry("1450x717")
        self.window.configure(bg="#A4A4A4")

        self.canvas = Canvas(
            self.window,
            bg="#A4A4A4",
            height=717,
            width=1450,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )   
        self.canvas.create_text(
            246.0,
            11.0,
            anchor="nw",
            text="Robot “Grupo Negro” - Servidor",
            fill="#FFFFFF",
            font=("InriaSans Regular", 64 * -1)
        )
        self.canvas.place(x=0, y=0)

        self.create_widgets()
        self.window.resizable(False, False)
        self.window.mainloop()

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def create_widgets(self):
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(131.0, 185.0, image=self.image_image_1)

        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(164.0, 199.0, image=self.entry_image_1)
        self.entry_1 = Entry(bd=0, bg="#9B9B9B", fg="#000716", highlightthickness=0)
        self.entry_1.place(x=112.0, y=181.0, width=104.0, height=34.0)

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.button_1.place(x=688.0, y=406.0, width=233.0, height=47.0)

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(897.0, 194.0, image=self.image_image_2)

        self.entry_image_2 = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(973.5, 200.0, image=self.entry_image_2)
        self.entry_2 = Entry(bd=0, bg="#9B9B9B", fg="#000716", highlightthickness=0)
        self.entry_2.place(x=953.0, y=184.0, width=41.0, height=30.0)

        self.image_image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.image_3 = self.canvas.create_image(597.0, 194.0, image=self.image_image_3)

        self.entry_image_3 = PhotoImage(file=self.relative_to_assets("entry_3.png"))
        self.entry_bg_3 = self.canvas.create_image(668.5, 210.0, image=self.entry_image_3)
        self.entry_3 = Entry(bd=0, bg="#9B9B9B", fg="#000716", highlightthickness=0)
        self.entry_3.place(x=643.0, y=192.0, width=51.0, height=34.0)

        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        self.button_2.place(
            x=465.0,
            y=590.0,
            width=161.0,
            height=46.0
        )

        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))  #estado del robot
        self.button_3 = Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        self.button_3.place(
            x=465.0,
            y=275.0,
            width=226.0,
            height=39.0
        )

        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_4.png"))

        self.button_4 = Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_4 clicked"),
            relief="flat"
        )
        self.button_4.place(x=1119.0, y=247.0, width=206.0, height=44.0)

        self.button_image_5 = PhotoImage(file=self.relative_to_assets("button_5.png"))
        self.button_5 = Button(
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_5 clicked"),
            relief="flat"
        )
        self.button_5.place(x=465.0, y=340.0, width=211.0, height=45.0)

        self.button_image_6 = PhotoImage(file=self.relative_to_assets("button_6.png"))
        self.button_6 = Button(
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_6 clicked"),
            relief="flat"
        )
        self.button_6.place(x=17.0, y=609.0, width=123.0, height=36.0)

        self.button_image_7 = PhotoImage(file=self.relative_to_assets("button_7.png"))
        self.button_7 = Button(
            image=self.button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_7 clicked"),
            relief="flat"
        )
        self.button_7.place(x=688.0, y=340.0, width=236.0, height=45.0)

        self.button_image_8 = PhotoImage(file=self.relative_to_assets("button_8.png"))
        self.button_8 = Button(
            image=self.button_image_8,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_8 clicked"),
            relief="flat"
        )
        self.button_8.place(x=16.0, y=545.0, width=230.0, height=45.0)

        self.button_image_9 = PhotoImage(file=self.relative_to_assets("button_9.png"))
        self.button_9 = Button(
            image=self.button_image_9,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_9 clicked"),
            relief="flat"
        )
        self.button_9.place(x=17.0, y=475.0, width=229.0, height=49.0)

        self.button_image_10 = PhotoImage(file=self.relative_to_assets("button_10.png"))
        self.button_10 = Button(
            image=self.button_image_10,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_10 clicked"),
            relief="flat"
        )
        self.button_10.place(x=465.0, y=406.0, width=207.0, height=47.0)

        self.button_image_11 = PhotoImage(file=self.relative_to_assets("button_11.png"))
        self.button_11 = Button(
            image=self.button_image_11,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_11 clicked"),
                relief="flat"
        )
        self.button_11.place(x=1119.0, y=193.0, width=200.0, height=36.0)

        self.button_image_12 = PhotoImage(file=self.relative_to_assets("button_12.png"))
        self.button_12 = Button(
            image=self.button_image_12,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_button_12_click(),  #listado automatic files
            relief="flat"
        )
        self.button_12.place(x=702.0, y=275.0, width=281.0, height=39.0)

        self.button_image_13 = PhotoImage(file=self.relative_to_assets("button_13.png"))
        self.button_13 = Button(
            image=self.button_image_13,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_13 clicked"),
            relief="flat"
        )
        self.button_13.place(x=1119.0, y=135.0, width=132.0, height=35.0)

        self.image_image_4 = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.image_4 = self.canvas.create_image(699.0, 520.0, image=self.image_image_4)

        self.entry_image_4 = PhotoImage(file=self.relative_to_assets("entry_4.png"))
        self.entry_bg_4 = self.canvas.create_image(780.5, 528.0, image=self.entry_image_4)
        self.entry_4 = Entry(bd=0, bg="#9B9B9B", fg="#000716", highlightthickness=0)
        self.entry_4.place(x=662.0, y=510.0, width=237.0, height=34.0)

        self.button_image_14 = PhotoImage(file=self.relative_to_assets("button_14.png"))
        self.button_14 = Button(
            image=self.button_image_14,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_14 clicked"),
            relief="flat"
        )
        self.button_14.place(x=16.0, y=252.0, width=100.0, height=38.0)

        self.image_image_5 = PhotoImage(file=self.relative_to_assets("image_5.png"))
        self.image_5 = self.canvas.create_image(205.0, 386.0, image=self.image_image_5)

        self.entry_image_5 = PhotoImage(file=self.relative_to_assets("entry_5.png"))
        self.entry_bg_5 = self.canvas.create_image(199.0, 413.0, image=self.entry_image_5)
        self.entry_5 = Entry(bd=0, bg="#9B9B9B", fg="#000716", highlightthickness=0)
        self.entry_5.place(x=31.0, y=396.0, width=336.0, height=32.0)

        self.image_image_6 = PhotoImage(file=self.relative_to_assets("image_6.png"))
        self.image_6 = self.canvas.create_image(1203.0, 509.0, image=self.image_image_6)

        self.canvas.create_rectangle(
            983.0,
            377.0,
            1424.0,
            681.0,
            fill="#000000",
            outline=""
        )

    def handle_button_12_click(self):
        try:

            res = self.controlador.listAutomaticFiles()

            print(f"{GREEN}Respuesta del proceso:{RESET}")

            for i in res:
                print(f"{IDENTATION}{i}{RESET}")

        except Exception as e:
            print(f"{ROJO}Error - {e}{RESET}")
