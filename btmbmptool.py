#See http://www.dragonwins.com/domains/getteched/bmp/bmpfileformat.htm for bitmap format specification
def btmToBmp(btmPath, bmpPath):
    btm = open(btmPath, "rb").read()
    bmp = open(bmpPath, "wb")
    #File header (14 bytes)
    bfType = b"BM"
    bfSize = b""
    bfReserved = b"\x00\x00" #appears twice, as bfReserved1 and bfReserved2
    bfOffBits = b"\x76\x00\x00\x00"

    #Image header (40 bytes)
    biSize = b"\x28\x00\x00\x00"
    biWidth = bytes([btm[0]]) + b"\x00\x00\x00"
    biHeight = bytes([btm[1]]) + b"\x00\x00\x00"
    biPlanes = b"\x01\x00"
    biBitCount = b"\x04\x00"
    biCompression = b"\x00\x00\x00\x00"
    biSizeImage = b"\x00\x00\x00\x00"
    biXPelsPerMeter = b"\x10\x00\x00\x00"
    biYPelsPerMeter = b"\x10\x00\x00\x00"
    biClrUsed = b"\x04\x00\x00\x00"
    biClrImportant = b"\x03\x00\x00\x00"

    #Color table (64 bytes)
    colorTable = b"\xFF\xFF\xFF\x00\x00\x00\x00\x00\xFF\x00\xFF\x00\xFF\x00\xFF\x00\xFF\xFF\xFF\x00\x00\x00\x00\x00\xFF\x00\xFF\x00\xFF\x00\xFF\x00\xFF\xFF\xFF\x00\x00\x00\x00\x00\xFF\x00\xFF\x00\xFF\x00\xFF\x00\xFF\xFF\xFF\x00\x00\x00\x00\x00\xFF\x00\xFF\x00\xFF\x00\xFF\x00" #each 4 bytes are a color, in order: white (#fffff), black (#000000), magenta/transparent (#ff00ff), unused magenta/transparent (same as before)
    header = len(bfType+bfReserved+bfReserved+bfOffBits+biSize+biWidth+biHeight+biPlanes+biBitCount+biCompression+biSizeImage+biXPelsPerMeter+biYPelsPerMeter+biClrUsed+biClrImportant+colorTable)
    pixelSize = 2    # The size of each pixel, in bits. This will be useful later on
    btmdata = bin(int.from_bytes(btm[2:], "big"))[2:] # Get the bit data of the btm file as a variable named btmdata
    rows = [btmdata[i:i+(btm[0] * pixelSize*2)] for i in range(0, len(btmdata), (btm[0] * pixelSize))]    # Separate the btmdata into rows; btm[0] is the width byte

    imgdata = b''    # The final, returned data
    for row in reversed(rows):    # Note: Scanlines are stored from bottom to top, so reverse the rows.
        b = 0
        for pixels in ([row[i:i + pixelSize] for i in range(0, len(row), pixelSize)]):    # Get each pixel in the row.
            imgdata += bytes([int(pixels[:pixelSize]+"0"*(4-pixelSize)+pixels[pixelSize:], 2)])    # Add everything to the final data, while turning the bytes to nibbles
            b += 1
        imgdata += bytes(b % 4) # Add padding because for some reason bmp is retarded and needs each scanline to be a multiple of 4
    out = header + len(imgdata)
    bfSize = (out+4).to_bytes(4, "little")
    header = bfType+bfSize+bfReserved+bfReserved+bfOffBits+biSize+biWidth+biHeight+biPlanes+biBitCount+biCompression+biSizeImage+biXPelsPerMeter+biYPelsPerMeter+biClrUsed+biClrImportant+colorTable
    out = header + imgdata
    print (out)                          #Debug function
    print (len(out))                     #Debug function
    print (int.from_bytes(bfSize,"little")) #Debug function
    bmp.write(out)
    bmp.close()
btmToBmp("a.btm","b.bmp")
