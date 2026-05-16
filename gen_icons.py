import struct, zlib

def make_png(size, bg, fg):
    def chunk(name, data):
        c = zlib.crc32(name + data) & 0xffffffff
        return struct.pack('>I', len(data)) + name + data + struct.pack('>I', c)
    
    img = []
    for y in range(size):
        row = []
        for x in range(size):
            # Draw music note shape
            cx, cy = size//2, size//2
            r = size * 0.38
            # Circle at bottom right
            note_cx = cx + size*0.08
            note_cy = cy + size*0.18
            note_r = size * 0.13
            # Stem
            stem_x = note_cx + note_r * 0.7
            stem_y_top = cy - size*0.22
            stem_w = size * 0.06
            
            in_note = ((x - note_cx)**2 + (y - note_cy)**2) < note_r**2
            in_stem = (stem_x - stem_w < x < stem_x + stem_w and stem_y_top < y < note_cy)
            in_flag = (stem_x - stem_w < x < stem_x + size*0.16 and stem_y_top < y < stem_y_top + size*0.18 and x > stem_x)
            
            if in_note or in_stem or in_flag:
                row += list(fg)
            else:
                row += list(bg)
        img.append(row)
    
    raw = b''
    for row in img:
        raw += b'\x00' + bytes(row)
    
    compressed = zlib.compress(raw)
    
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', compressed)
    png += chunk(b'IEND', b'')
    return png

# Background: deep blue, icon: white
bg = (26, 115, 232)  # accent blue
fg = (255, 255, 255)  # white

for size, name in [(192, 'icon-192.png'), (512, 'icon-512.png'), (180, 'apple-touch-icon.png')]:
    with open(f'pwa/{name}', 'wb') as f:
        f.write(make_png(size, bg, fg))
    print(f'Created {name}')
