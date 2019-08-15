# This tool uses the PNG lib in Python to convert between a BTM format, which is a monochrome bitmap that supports transparency, and the PNG format, which is heavily used
# It was made after a failed attempt between BTM and BMP

# Quick BTM documentation:
#   -First two bytes are width and height, respectively, and the rest is pixel data
#   -The palette (at least the given one) is: [white, black, transparent (white), transparent (black) [inverts the color of the previous layer]
#   -For now, the pixel data has a depth of 2. If this is ever changed, it can be inputted in the palette and pixelsize, in the function

import png # obviously, it needs the PNG library

def btmToPng (btmPath, pngPath,
              palette = [(0xff, 0xff, 0xff, 0xff), (0x00, 0x00, 0x00, 0xff), (0xff, 0xff, 0xff, 0x00), (0x00, 0x00, 0x00, 0x00)],
              pixelsize = 2,
              transparency = True):
    # If the transparency option is disabled, each color will change to a different one if transparent:
    #   -00: White  -01: Black   -10: Magenta    -11: Red
    if not transparency:
        count = 0
        for color in palette:
            if color[3] == 0x00:
                palette[count] = {0:(0xff,0xff,0xff), 1:(0x00,0x00,0x00), 2:(0xff,0x00,0xff), 3:(0xff,0x00,0x00)}[count]
            else:
                palette[count] = color[:3]
            count += 1
    
    # Both the original BTM and the PNG file it will write to
    btm = open(btmPath, "rb").read()
    endfile = open(pngPath, "wb") # The PNG file where the image will be written to
    
    # Interpret the btm's data
    width = btm[0]
    height = btm[1]
    pxdata = bin(int.from_bytes(btm[2:], "big"))[2:] # Get the pixel data, in the form of a binary string
    while len(pxdata) % width * pixelsize != 0:
        pxdata = "0" + pxdata     # This ensures that the binary string can be properly divided in rows
    rows = [] # Here's where the final row will go
    for row in [pxdata[i:i+(width * pixelsize)] for i in range(0, len(pxdata), (width * pixelsize))]: #Iterates in a list of separated rows
        rowlist = [] # Exported data from the row here
        pixel = ""
        for bit in row:
            pixel += bit
            if len(pixel) == pixelsize:
                rowlist.append(int(pixel, 2))
                pixel = ""
        rows.append(rowlist)
    
    # Write the data to the file:
    writer = png.Writer(width, height, palette=palette, bitdepth=pixelsize)
    writer.write(endfile, rows)

btmToPng("a.btm", "b.png", transparency = False)
