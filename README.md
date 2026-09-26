# Minecraft Pixel Art Generator

A 'fast' and easy-to-use tool for converting images into **Minecraft pixel art** and exporting them directly as `.litematic` schematics.

The program analyzes every pixel of an image, finds the closest matching Minecraft block from the selected palette, and automatically generates a schematic that can be loaded with the **Litematica** mod.

---

## Features

- 🖼️ Convert images into Minecraft pixel art
- 📐 Choose the generated schematic size
- 🧱 Large Minecraft block palette
- ✅ Enable or disable individual blocks
- 📦 Enable or disable entire block categories
- 🔍 Block textures displayed directly in the selection menu
- 🌐 Transparent pixels are automatically converted to air
- 🪟 Simple graphical interface

---

## Download

The easiest way to use the program is to download the latest version from the **Releases** section of this repository.

Download the latest `.exe`, open it, and you are ready to go.

No Python installation is required when using the executable version.

---

## How to Use

1. Download and open the latest **Pixel Art Generator vX.X.exe**.
2. Select the image you want to convert.
3. Choose the dimensions of the schematic.
4. Open the block selection menu and select which Minecraft blocks you want the generator to use.
5. Click **`Generate Schematic`**
6. Preview the generated schematic.
7. Open the schematic in Minecraft using the **Litematica** mod.

---

## How It Works

For every pixel in the source image, the generator compares its color against the available Minecraft block palette.

The block with the closest matching color is selected and placed in the corresponding position inside the schematic.

Transparent pixels are coded as **air**.

---

## Performance

In early builds, the program was really slow, so slow that it took up to 64s for a 500x500 schematic!

Even in version 2.0 where i introduced multiprocessing it still was quiet slow. So in the end i decided to get help
from a realy fast language, C!

I implemented the block matcher in C which greatly reduced the generation time of the schematic by more than half the old time,
but it still wasn't fast enough!

I dag into litemapy's functions and methods and found out i can bypass litemapy's Region.__setitem__() and directly insert the blocks into the schematic
and also using the programs own block palette.

The performance can still be improved by using libraries other than litemapy, like nucleation, which in tests has
shown way better peformance than litemapy.

---

## Block Selection

You are not forced to use the entire Minecraft block palette.

The block selection menu allows you to control which blocks can appear in the generated pixel art.

You can:

- Enable or disable individual blocks
- Enable or disable entire block categories
- See the texture of each block directly in the select blocks menu

This is useful if you want to:

- Avoid expensive blocks
- Create pixel art using a specific block theme
- Restrict the generator to blocks you already have

---

## Transparency

Images containing transparent pixels are supported, but it doesn't work all the time. Some photos might generate with random blocks in transparent locations if the photo's mode is different (the A value in RGBA mode).

Pixels with transparent pixels are treated as empty space and become **air** in the generated schematic.

---

## Litematica

The generated files use the `.litematic` format and can be loaded directly using the **Litematica** Minecraft mod.

---

## Built With

The project is built using:

- **Python 3.14.7**
- **C** for fast block matching
- **Tkinter / ttk / Custom Tkinter** for the GUI
- **Pillow** for image processing
- **Litemapy** for creating the `.litematic` files

---

## Running From Source

If you prefer to run the project directly from the source code, clone the repository and make sure the required Python dependencies are installed.
Then unzip the Source.zip archive from the latest release and you will find the sources for the program.

---

## Credits

### Litemapy

A huge thanks to the developers of **Litemapy**.

This project uses Litemapy to create Minecraft `.litematic` schematic files.

https://github.com/SmylerMC/litemapy

Without their work, implementing `.litematic` support would have been significantly more difficult.

---

## Feedback & Bug Reports

If you find a bug, experience a crash, or have an idea for a new feature, feel free to open an **Issue** on GitHub.

When reporting a bug include the following information for more help:

- Program version
- Image resolution
- Generation size
- Number of selected blocks
- Screenshot or error message
- Steps needed to reproduce the problem
