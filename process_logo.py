import struct
import zlib
from collections import deque

def remove_background(input_bmp_path, output_png_path):
    with open(input_bmp_path, 'rb') as f:
        header = f.read(54)
        raw_data = f.read()

    w, h = struct.unpack('<ii', header[18:26])
    top_down = (h < 0)
    h = abs(h)
    
    print(f"Processing image: {w}x{h}, top_down={top_down}")

    # Build 2D RGB array
    # BMP is 24-bit BGR
    img = []
    for y in range(h):
        row_idx = y if top_down else (h - 1 - y)
        row_offset = row_idx * w * 3
        row = []
        for x in range(w):
            idx = row_offset + x * 3
            b, g, r = raw_data[idx:idx+3]
            row.append((r, g, b))
        img.append(row)

    # Flood-fill from borders
    # Border color is roughly R: [3, 15], G: [15, 30], B: [22, 40]
    # A pixel is considered background if it is connected to border and is dark
    is_bg = [[False]*w for _ in range(h)]
    queue = deque()

    # Seed with all 4 borders
    for x in range(w):
        queue.append((x, 0))
        queue.append((x, h - 1))
        is_bg[0][x] = True
        is_bg[h-1][x] = True
    for y in range(h):
        queue.append((0, y))
        queue.append((w - 1, y))
        is_bg[y][0] = True
        is_bg[y][w-1] = True

    def is_dark_bg(r, g, b):
        # Background is dark navy / black
        # Red is very low (< 38), Green (< 48), Blue (< 65)
        # Total brightness / luminance is low
        return (r < 40 and g < 50 and b < 65)

    while queue:
        cx, cy = queue.popleft()
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h and not is_bg[ny][nx]:
                r, g, b = img[ny][nx]
                if is_dark_bg(r, g, b):
                    is_bg[ny][nx] = True
                    queue.append((nx, ny))

    # Anti-aliasing / edge softness for border transition
    # Compute alpha (0 to 255)
    rgba = []
    for y in range(h):
        row = []
        for x in range(w):
            r, g, b = img[y][x]
            if is_bg[y][x]:
                row.append((r, g, b, 0))
            else:
                # Check if it has background neighbors (edge pixel)
                has_bg_neighbor = False
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and is_bg[ny][nx]:
                        has_bg_neighbor = True
                        break
                
                if has_bg_neighbor and (r < 70 and g < 70 and b < 70):
                    # Soft edge blend
                    lum = (r * 0.299 + g * 0.587 + b * 0.114)
                    alpha = int(min(255, max(0, (lum - 20) / 40 * 255)))
                    row.append((r, g, b, alpha))
                else:
                    row.append((r, g, b, 255))
        rgba.append(row)

    # Find bounding box of non-transparent pixels to crop tight
    min_x, max_x = w, 0
    min_y, max_y = h, 0
    for y in range(h):
        for x in range(w):
            if rgba[y][x][3] > 0:
                if x < min_x: min_x = x
                if x > max_x: max_x = x
                if y < min_y: min_y = y
                if y > max_y: max_y = y

    pad = 12
    min_x = max(0, min_x - pad)
    max_x = min(w - 1, max_x + pad)
    min_y = max(0, min_y - pad)
    max_y = min(h - 1, max_y + pad)

    crop_w = max_x - min_x + 1
    crop_h = max_y - min_y + 1
    print(f"Cropped emblem bounding box: [{min_x}:{max_x}], [{min_y}:{max_y}] -> {crop_w}x{crop_h}")

    # Build PNG data
    # Each scanline: filter_byte (0) + 4 bytes per pixel (R, G, B, A)
    raw_scanlines = bytearray()
    for y in range(min_y, max_y + 1):
        raw_scanlines.append(0) # Filter None
        for x in range(min_x, max_x + 1):
            r, g, b, a = rgba[y][x]
            raw_scanlines.extend((r, g, b, a))

    # Compress IDAT chunk
    compressed = zlib.compress(bytes(raw_scanlines), 9)

    # PNG File Structure:
    # 8-byte signature: 89 50 4E 47 0D 0A 1A 0A
    png_bytes = bytearray(b'\x89PNG\r\n\x1a\n')

    def make_chunk(chunk_type, chunk_data):
        chunk = bytearray()
        chunk.extend(struct.pack('>I', len(chunk_data)))
        chunk.extend(chunk_type)
        chunk.extend(chunk_data)
        crc = zlib.crc32(chunk_type + chunk_data) & 0xffffffff
        chunk.extend(struct.pack('>I', crc))
        return chunk

    # IHDR: width(4), height(4), bit_depth(1=8), color_type(1=6 RGBA), comp(0), filter(0), interlace(0)
    ihdr_data = struct.pack('>IIBBBBB', crop_w, crop_h, 8, 6, 0, 0, 0)
    png_bytes.extend(make_chunk(b'IHDR', ihdr_data))

    # IDAT
    png_bytes.extend(make_chunk(b'IDAT', compressed))

    # IEND
    png_bytes.extend(make_chunk(b'IEND', b''))

    with open(output_png_path, 'wb') as f:
        f.write(png_bytes)

    print(f"Successfully generated transparent PNG: {output_png_path} ({len(png_bytes)} bytes)")

if __name__ == '__main__':
    remove_background('test.bmp', 'logo_transparan.png')
