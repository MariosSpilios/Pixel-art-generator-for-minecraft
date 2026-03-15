# from PIL import Image
# from PIL import ImageFile
import os
import csv
import sys
from litemapy import Schematic, Region, BlockState
import math
import threading
import time
import tkinter as tk
from tkinter import * # type: ignore
from tkinter import filedialog
from tkinter import ttk
from PIL import * # type: ignore
import PIL.Image as Img

WINDOW_WIDTH: int = 500
WINDOW_HEIGHT: int = 400
BLACK: str = "#000000"
WHITE: str = "#FFFFFF"

class App():

    photoFilePath: str = ""
    photoFileName: str = ""
    schematicWidth: int = 0
    schematicHeight: int = 0
    defaultCSVFile: str = f"{os.path.dirname(__file__)}\\csv.csv"
    checkButtonVars: list[IntVar] = []
    checkButtons: list[tk.Checkbutton] = []
    startGenerateTime = 0
    endGenerateTime = 0

    dither: bool = False

    img = None

    def __init__(self, mainWindow: tk.Tk) -> None:

        print("Program messages\n-----------------------------------------------------------------------------------------")
        self.root: tk.Tk = mainWindow
        self.selectBlocksWindow = None

        App.isPhotoTransparentForDropdownList = StringVar(value="No")

        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.geometry("+750+25")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.root.title("Pixel Art Generator")
        self.root.__setitem__("bg", BLACK)

        self.selectPhotoButton = tk.Button(self.root, text="Select photo", command=self.getPhotoFilePath)
        self.selectPhotoButton.place(x=25, y=50)
        self.selectPhotoButtonLabel: tk.Label = tk.Label(self.root, text=f"Selected photo: {App.photoFilePath}")
        self.selectPhotoButtonLabel.place(x=105, y=53)

        self.schematicWidthSpinbox: tk.Spinbox = tk.Spinbox(self.root, from_=10, to=1000, width=10, relief="sunken", fg="black", command=self.updateSchematicWidthFromSpinbox)
        self.schematicWidthSpinbox.config(state="normal", justify="center", wrap=True)
        self.schematicWidthSpinbox.place(x=25, y=80)
        self.schematicWidthSpinboxLabel: tk.Label = tk.Label(self.root, text="Schematic Width (10 - 1000)")
        self.schematicWidthSpinboxLabel.place(x=105, y=80)

        self.schematicHeightSpinbox: tk.Spinbox = tk.Spinbox(self.root, from_=10, to=383, width=10, relief="sunken", fg="black", command=self.updateSchematicHeightFromSpinbox)
        self.schematicHeightSpinbox.config(state="normal", justify="center", wrap=True)
        self.schematicHeightSpinbox.place(x=25, y=105)
        self.schematicHeightSpinboxLabel: tk.Label = tk.Label(self.root, text="Schematic Height (10 - 383)")
        self.schematicHeightSpinboxLabel.place(x=105, y=105)

        self.ditherDropdownList: ttk.Combobox = ttk.Combobox(main_window, values=["Yes", "No"], width=9, state="readonly")
        self.ditherDropdownList.set("Yes")
        self.ditherDropdownList.place(x=25, y=130)
        self.ditherLabel: tk.Label = tk.Label(main_window, text="Dither?")
        self.ditherLabel.place(x=105, y=130)

        self.generateButton: tk.Button = tk.Button(self.root, text="Generate schematic!", command=self.generator)
        self.generateButton.place(x=25, y=220)

        self.selectBlocksButton: tk.Button = tk.Button(self.root, text="Select blocks", command=self.openSelectBlocksWindow)
        self.selectBlocksButton.place(x=25, y=250)

    def openSelectBlocksWindow(self, *args) -> None:
        App.checkButtons.clear()
        if (self.selectBlocksWindow is not None and self.selectBlocksWindow.winfo_exists()):
            self.selectBlocksWindow.lift()
            self.selectBlocksWindow.focus_force()
            return
    
        def updateAvailableBlockList() -> None:
            saveBlockList.config(text="Saved!")
            Palette.activeBlockList.clear()
            Palette.disabledBlockList.clear()

            for i in range(Palette.allBlocksList.__len__()):
                if (App.checkButtonVars[i].get() == 1):
                    Palette.activeBlockList.append(Palette.allBlocksList[i])
                else:
                    Palette.disabledBlockList.append(Palette.allBlocksList[i])

            print("-----------------------------------------------------------------------------------------")
            print("Blocks saved!")
            print(f"New available blocks: {Palette.activeBlockList.__len__()}")
            print(f"Disabled blocks: {Palette.disabledBlockList.__len__()}")

        self.selectBlocksWindow = tk.Toplevel(self.root)
        self.selectBlocksWindow.geometry(f"{1700}x{900}+100+50")
        self.selectBlocksWindow.geometry("+100+50")
        self.selectBlocksWindow.resizable(False, False)
        self.selectBlocksWindow.protocol("WM_DELETE_WINDOW", self.closeSelectBlocksWindow)
        self.selectBlocksWindow.title("Block selection")
        self.selectBlocksWindow.__setitem__("bg", WHITE)
        idx: int = 10
        idy: int = 25
        frameHeight: int = 2000

        canvas = Canvas(self.selectBlocksWindow)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(self.selectBlocksWindow, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        scrollable_frame = Frame(canvas, width=1700, height=frameHeight)

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        saveBlockList: tk.Button = tk.Button(scrollable_frame, text="Save blocks", command=updateAvailableBlockList)
        saveBlockList.place(x=10, y=550)

        index: int = 0
        tk.Label(scrollable_frame, text="CONCRETE POWDER BLOCKS", bg=BLACK, fg=WHITE).place(x=12, y=0)
        for i in range(Palette.concretePowder.__len__()):
            App.checkButtons.append(tk.Checkbutton(scrollable_frame, text=Palette.concretePowder[index].rid[10:], variable=App.checkButtonVars[index]))
            App.checkButtons[index].place(x=idx, y=idy)
            index += 1
            idy += 30

        # CONCRETE BLOCKS
        idx = 200
        idy = 25
        tk.Label(scrollable_frame, text="CONCRETE BLOCKS", bg=BLACK, fg=WHITE).place(x=205, y=0)
        for i in range(Palette.concreteBlocks.__len__()):
            App.checkButtons.append(tk.Checkbutton(scrollable_frame, text=Palette.concreteBlocks[i].rid[10:], variable=App.checkButtonVars[index]))
            App.checkButtons[index].place(x=idx, y=idy)
            index += 1
            idy += 30

        # WOOL BLOCKS
        idx = 340
        idy = 25
        tk.Label(scrollable_frame, text="WOOL BLOCKS", bg=BLACK, fg=WHITE).place(x=345, y=0)
        for i in range(Palette.woolBlocks.__len__()):
            App.checkButtons.append(tk.Checkbutton(scrollable_frame, text=Palette.woolBlocks[i].rid[10:], variable=App.checkButtonVars[index]))
            App.checkButtons[index].place(x=idx, y=idy)
            index += 1
            idy += 30
            
        # TERRACOTTA
        idx = 455
        idy = 25
        tk.Label(scrollable_frame, text="TERRACOTTA BLOCKS", bg=BLACK, fg=WHITE).place(x=460, y=0)
        for i in range(Palette.terracottaBlocks.__len__()):
            App.checkButtons.append(tk.Checkbutton(scrollable_frame, text=Palette.terracottaBlocks[i].rid[10:], variable=App.checkButtonVars[index]))
            App.checkButtons[index].place(x=idx, y=idy)
            index += 1
            idy += 30

        # GLAZED TERRACOTTA
        idx = 605
        idy = 25
        tk.Label(scrollable_frame, text="GLAZED TERRACOTTA BLOCKS", bg=BLACK, fg=WHITE).place(x=610, y=0)
        for i in range(Palette.glazedTerracottaBlocks.__len__()):
            App.checkButtons.append(tk.Checkbutton(scrollable_frame, text=Palette.glazedTerracottaBlocks[i].rid[10:], variable=App.checkButtonVars[index]))
            App.checkButtons[index].place(x=idx, y=idy)
            index += 1
            idy += 30

        # LOG BLOCKS
        idx = 795
        idy = 25
        tk.Label(scrollable_frame, text="LOGS", bg=BLACK, fg=WHITE).place(x=800, y=0)
        for i in range(Palette.logBlocks.__len__()):
            App.checkButtons.append(tk.Checkbutton(scrollable_frame, text=Palette.logBlocks[i].rid[10:], variable=App.checkButtonVars[index]))
            App.checkButtons[index].place(x=idx, y=idy)
            index += 1
            idy += 30

        # OTHER BLOCKS
        idx = 950
        idy = 25
        tk.Label(scrollable_frame, text="OTHER BLOCKS", bg=BLACK, fg=WHITE, width=100).place(x=955, y=0)
        for i in range(Palette.allTheOtherBlocks.__len__()):

            App.checkButtons.append(tk.Checkbutton(scrollable_frame, text=f"{Palette.allTheOtherBlocks[i].rid[10:]} | {Palette.allTheOtherBlocks[i].blockStateToString()}", variable=App.checkButtonVars[index]))
            App.checkButtons[index].place(x=idx, y=idy)
            index += 1
            if (idy + 2*30 > frameHeight):
                idx += 250
                idy = 25
            else:
                idy += 30

    def closeSelectBlocksWindow(self, *args) -> None:
        if (self.selectBlocksWindow is not None):
            self.selectBlocksWindow.destroy()
            self.selectBlocksWindow = None
    
    def getPhotoFilePath(self) -> None:
        App.photoFilePath = filedialog.askopenfilename(title="Photo selection", filetypes=
            [
            ("Image files", "*.png *.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
            ]
        )

        self.selectPhotoButtonLabel.__setitem__("text", f"Selected photo: {App.photoFilePath.split("/")[-1]}")
        print("-----------------------------------------------------------------------------------------")
        print(f"Photo updated: {App.photoFilePath.split("/")[-1]}")

    def updateSchematicWidthFromSpinbox(self) -> None:
        try:
            temp = int(self.schematicWidthSpinbox.get())
        except:
            App.schematicWidth = 10
            return
        if (temp < 10): App.schematicWidth = 10
        elif (temp > 1000): App.schematicWidth = 1000
        else: App.schematicWidth = temp
    def updateSchematicHeightFromSpinbox(self) -> None:
        try:
            temp = int(self.schematicHeightSpinbox.get())
        except:
            App.schematicHeight = 10
            return
        if (temp < 10): App.schematicHeight = 10
        elif (temp > 383): App.schematicHeight = 383
        else: App.schematicHeight = temp
    def updateDithering(self) -> None:
        if (str(self.ditherDropdownList.get()) == "Yes"):
            App.dither = True
        else:
            App.dither = False

    def onClosing(self, *args) -> None:
        self.root.destroy()

    def generator(self, *args) -> None:

        if (App.photoFilePath == ""):
            print("No photo selected! Can't generate schematic :(")
            return
        try:
            Img.open(App.photoFilePath).close()
        except:
            self.selectPhotoButtonLabel.config(text="Wrong file type, please select a photo with a valid file type")
            return
        
        App.startGenerateTime = time.time()
        self.updateSchematicWidthFromSpinbox()
        self.updateSchematicHeightFromSpinbox()
        self.updateDithering()
        print("-----------------------------------------------------------------------------------------")
        print(f"Schematic width | height: {App.schematicWidth} | {App.schematicHeight}")

        App.img = Img.open(App.photoFilePath)
        resized = App.img.resize((App.schematicWidth, App.schematicHeight))
        App.img.close()
        resized = resized.transpose(Img.Transpose.ROTATE_270)
        resized = resized.convert("RGBA")

        reg = Region(0, 0, 0, 1, App.schematicHeight, App.schematicWidth)
        schem = reg.as_schematic(name=App.photoFilePath.split("/")[-1], author="some1", description="Generated with Pixel Art Generator")

        print("Generating...\nIt might seem that the program has crashed, but don't worry..., its generating the schematic!\nIt just takes some time... (up to a minute)")
        if (App.dither):
            for h in range(App.schematicHeight-1):
                for w in range(1, App.schematicWidth-1):
                    
                    # Floyd-Steinberg dithering https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering
                    
                    oldRGB = resized.getpixel((h, w))
                    if (oldRGB[3] <= 0): # type: ignore
                        continue
                    else:

                        oldR = oldRGB[0] # type: ignore
                        oldG = oldRGB[1] # type: ignore
                        oldB = oldRGB[2] # type: ignore

                        newRGB = self.findBestBlockMatch(oldRGB) # type: ignore
                        newR = newRGB[0]
                        newG = newRGB[1]
                        newB = newRGB[2]

                        errorR = oldR - newR
                        errorG = oldG - newG
                        errorB = oldB - newB

                        rgb = resized.getpixel((h, w + 1))
                        r = rgb[0] # type: ignore
                        g = rgb[1] # type: ignore
                        b = rgb[2] # type: ignore
                        r = r + errorR * 7//16
                        g = g + errorG * 7//16
                        b = b + errorB * 7//16
                        resized.putpixel((h, w + 1), (r, g, b))

                        rgb = resized.getpixel((h + 1, w - 1))
                        r = rgb[0] # type: ignore
                        g = rgb[1] # type: ignore
                        b = rgb[2] # type: ignore
                        r = r + errorR * 3//16
                        g = g + errorG * 3//16
                        b = b + errorB * 3//16
                        resized.putpixel((h + 1, w - 1), (r, g, b))

                        rgb = resized.getpixel((h + 1, w))
                        r = rgb[0] # type: ignore
                        g = rgb[1] # type: ignore
                        b = rgb[2] # type: ignore
                        r = r + errorR * 5//16
                        g = g + errorG * 5//16
                        b = b + errorB * 5//16
                        resized.putpixel((h + 1, w), (r, g, b))

                        rgb = resized.getpixel((h + 1, w + 1))
                        r = rgb[0] # type: ignore
                        g = rgb[1] # type: ignore
                        b = rgb[2] # type: ignore
                        r = r + errorR * 1//16
                        g = g + errorG * 1//16
                        b = b + errorB * 1//16
                        resized.putpixel((h + 1, w + 1), (r, g, b))
            
        for h in range(App.schematicHeight):
            for w in range(App.schematicWidth):
                rgb = resized.getpixel((h, w))

                if ((rgb[3] <= 0)): # type: ignore
                    reg[0, h, w] = BlockState("minecraft:air")
                else:
                    
                    minEuclideanDistance = math.inf
                    mini = 0
                    for i in range(Palette.activeBlockList.__len__()):

                        tempBpl = Palette.activeBlockList[i]
                        if ((abs(rgb[0] - tempBpl.average.RED) + abs(rgb[1] - tempBpl.average.GREEN) + abs(rgb[2] - tempBpl.average.BLUE)) < minEuclideanDistance):  # type: ignore
                            minEuclideanDistance = (abs(rgb[0] - tempBpl.average.RED) + abs(rgb[1] - tempBpl.average.GREEN) + abs(rgb[2] - tempBpl.average.BLUE)) # type: ignore
                            mini = i

                    reg[0, h, w] = BlockState(Palette.activeBlockList[mini].rid, **Palette.activeBlockList[mini].blockStateProperties)

        if (not os.path.exists(f"{os.path.dirname(__file__)}\\output schematics")): os.makedirs(f"{os.path.dirname(__file__)}\\output schematics")
        schem.save(f"{os.path.dirname(__file__)}\\output schematics\\{App.photoFilePath.split("/")[-1].split(".")[0]}.litematic")
        
        App.endGenerateTime = time.time()
        print("Generated!")
        print(f"Schematic saved in: {os.path.dirname(__file__)}\\output\\{App.photoFilePath.split("/")[-1].split(".")[0]}.litematic")
        print(f"Time: {(App.endGenerateTime - App.startGenerateTime):.2f} seconds")
    
    @staticmethod
    def findBestBlockMatch(rgb: tuple[int, int, int, int]) -> tuple[int, int, int]:
        minEuclideanDistance: float = math.inf
        mini: int = -1
        for i in range(Palette.activeBlockList.__len__()):

            tempBpl = Palette.activeBlockList[i]
            if ((abs(rgb[0] - tempBpl.average.RED) + abs(rgb[1] - tempBpl.average.GREEN) + abs(rgb[2] - tempBpl.average.BLUE)) < minEuclideanDistance):  # type: ignore
                minEuclideanDistance = (abs(rgb[0] - tempBpl.average.RED) + abs(rgb[1] - tempBpl.average.GREEN) + abs(rgb[2] - tempBpl.average.BLUE)) # type: ignore
                mini = i
        return (int(Palette.activeBlockList[mini].average.RED), int(Palette.activeBlockList[mini].average.GREEN), int(Palette.activeBlockList[mini].average.BLUE))

    @staticmethod
    def readCSV() -> None:
        with open(App.defaultCSVFile, newline='') as f:
            reader = csv.reader(f, delimiter=",", quoting=csv.QUOTE_NONE)
            for row in reader:
                if ("RID" in row): continue
                if ("concrete_powder" in row[0]):
                    Palette.concretePowder.append(MinecraftBlock(RGBCOLOR(float(row[1]), float(row[2]), float(row[3])), row[0], App.parse(row[4])))
                elif ("concrete" in row[0]):
                    Palette.concreteBlocks.append(MinecraftBlock(RGBCOLOR(float(row[1]), float(row[2]), float(row[3])), row[0], App.parse(row[4])))
                elif ("wool" in row[0]):
                    Palette.woolBlocks.append(MinecraftBlock(RGBCOLOR(float(row[1]), float(row[2]), float(row[3])), row[0], App.parse(row[4])))
                elif ("glazed_terracotta" in row[0]):
                    Palette.glazedTerracottaBlocks.append(MinecraftBlock(RGBCOLOR(float(row[1]), float(row[2]), float(row[3])), row[0], App.parse(row[4])))
                elif ("terracotta" in row[0]):
                    Palette.terracottaBlocks.append(MinecraftBlock(RGBCOLOR(float(row[1]), float(row[2]), float(row[3])), row[0], App.parse(row[4])))
                elif ("log" in row[0]):
                    Palette.logBlocks.append(MinecraftBlock(RGBCOLOR(float(row[1]), float(row[2]), float(row[3])), row[0], App.parse(row[4])))
                else:
                    Palette.allTheOtherBlocks.append(MinecraftBlock(RGBCOLOR(float(row[1]), float(row[2]), float(row[3])), row[0], App.parse(row[4])))
        
        Palette.updateAllBlocksList()
        Palette.activeBlockList = Palette.allBlocksList.copy()
        App.checkButtonVars = [tk.IntVar(value=1) for i in range(Palette.allBlocksList.__len__())]

    @staticmethod
    def constructStringFromDict(d: dict[str, str]) -> str:
        x: str = ""
        for v in d:
            x += f"{v}={d[v]}~"
        return x
    
    @staticmethod
    def parse(s: str) -> dict[str, str]:
        if (s.__len__() == 0):
            return {}
        d = {}
        L: list = s.split("~")[0:-1]
        for value in L:
            x, y = value.split("=")
            d[x] = y
        return d

# Class that is specialized for the color of the minecraft block
class RGBCOLOR():
    def __init__(self, RED: float, GREEN: float, BLUE: float) -> None:
        self.RED = RED
        self.GREEN = GREEN
        self.BLUE = BLUE

# Class that has the average RGB color of the block, the id of the block and the properties of that block (if it has)
class MinecraftBlock():
    def __init__(self, average: RGBCOLOR, rid: str, blockStateProperties: dict[str, str] | None = None) -> None:
        self.average = average
        self.rid = rid
        self.blockStateProperties = blockStateProperties or {}

    def blockStateToString(self) -> str:
        return App.constructStringFromDict(self.blockStateProperties)

class Palette():
    
    concretePowder: list[MinecraftBlock] = []
    concreteBlocks: list[MinecraftBlock] = []
    woolBlocks: list[MinecraftBlock] = []
    terracottaBlocks: list[MinecraftBlock] = []
    glazedTerracottaBlocks: list[MinecraftBlock] = []
    logBlocks: list[MinecraftBlock] = []
    allTheOtherBlocks: list[MinecraftBlock] = []

    allBlocksList: list[MinecraftBlock] = []

    activeBlockList: list[MinecraftBlock] = []
    disabledBlockList: list[MinecraftBlock] = []

    @staticmethod
    def updateAllBlocksList() -> None:
        Palette.allBlocksList = Palette.concretePowder + Palette.concreteBlocks + Palette.woolBlocks + Palette.terracottaBlocks + Palette.glazedTerracottaBlocks + Palette.logBlocks + Palette.allTheOtherBlocks

# WINDOW SHIT
main_window = tk.Tk()
App(main_window)
App.readCSV()
main_window.mainloop()
print("\n\n-----------------------------------------------------------------------------------------\nBye!")
os.system("PAUSE")