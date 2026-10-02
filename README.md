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

In early builds, the program was really slow, so slow that it took up to 64s for a 576x324 schematic!

Even in version 2.0, where I introduced multiprocessing, it still was quite slow. So in the end i decided to get help
from a really fast language, C!

As of version 3.3 and on, the whole generator in written in C. Image processing, resize, block matching and writing the `.litematic` schematic.

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

Images with an alpha value, such as RGBA images, support transparency. Some image modes are not handled correctly yet and may generate unexpected blocks in areas that should be transparent.

Transparent pixels are treated as empty space and become **air** in the generated schematic.

---

## Litematica

The generated files use the `.litematic` format and can be loaded directly using the **Litematica** Minecraft mod.

---

## Built With

The project is built using:

- **Python 3.14.7**
- **C** for the generator backend
- **Tkinter / ttk / Custom Tkinter** for the GUI
- **Pillow** for image processing (up to version 3.1)
- **Litemapy** for creating the `.litematic` files (up to version 3.1)
- **stb** library for loading image in C (version 3.3+)
- **libnbt** for writing the schematics (version 3.3+)
- **miniz** for gzip/zlib compression (version 3.3+)

---

## Running From Source

If you prefer to run the project directly from the source code, download and extract Sources.zip from the latest release.

---

## Credits

- **Litemapy** (For version up to 3.1)

This project uses Litemapy to create Minecraft `.litematic` schematic files.
https://github.com/SmylerMC/litemapy

From version 3.3 and on:

Special thanks to the developers of the following libraries used in this project:

- **stb** by Sean Barrett and contributors  
  Used for image loading and resizing (`stb_image.h`, `stb_image_resize2.h`).  
  https://github.com/nothings/stb

- **libnbt** by Celisium
  Used for creating and writing Minecraft NBT / `.litematic` files.
  https://github.com/Celisium/libnbt

- **miniz** by Rich Geldreich and contributors  
  Used by the NBT writer for gzip/zlib compression.  
  https://github.com/richgel999/miniz

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
