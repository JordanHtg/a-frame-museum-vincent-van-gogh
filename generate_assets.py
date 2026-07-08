import os
import struct
import math
import zlib

def ensure_dirs():
    os.makedirs('assets/images', exist_ok=True)
    os.makedirs('assets/textures', exist_ok=True)
    os.makedirs('assets/models', exist_ok=True)

# Helper to write raw PNG file from RGB pixel buffer (pure Python without PIL)
def write_png(filename, width, height, pixels):
    # pixels is a flat list/bytes of RGB values (3 bytes per pixel)
    def png_chunk(tag, data):
        return struct.pack('!I', len(data)) + tag + data + struct.pack('!I', zlib.crc32(tag + data) & 0xFFFFFFFF)
    
    # PNG Header
    header = b'\x89PNG\r\n\x1a\n'
    # IHDR chunk
    ihdr = struct.pack('!IIBBBBB', width, height, 8, 2, 0, 0, 0)
    
    # Raw scanlines with filter byte 0
    raw_rows = bytearray()
    row_len = width * 3
    for y in range(height):
        raw_rows.append(0) # filter None
        start = y * row_len
        raw_rows.extend(pixels[start:start + row_len])
        
    compressed = zlib.compress(bytes(raw_rows), 9)
    
    with open(filename, 'wb') as f:
        f.write(header)
        f.write(png_chunk(b'IHDR', ihdr))
        f.write(png_chunk(b'IDAT', compressed))
        f.write(png_chunk(b'IEND', b''))

def create_textures():
    print("Generating museum textures...")
    
    # 1. Wood Floor Texture (Herringbone / Parquet Warm Wood #8B5E3C & #5A3E2B)
    w, h = 256, 256
    pixels = bytearray()
    for y in range(h):
        for x in range(w):
            plank_w = 32
            plank_h = 64
            idx = (x // plank_w) + (y // plank_h)
            grain = int(math.sin(x * 0.3 + y * 0.1) * 12 + math.cos(y * 0.5) * 8)
            border = 1 if ((x % plank_w == 0) or (y % plank_h == 0)) else 0
            if border:
                r, g, b = 70, 45, 30
            else:
                base_r = 139 if idx % 2 == 0 else 125
                base_g = 94 if idx % 2 == 0 else 82
                base_b = 60 if idx % 2 == 0 else 52
                r = max(0, min(255, base_r + grain))
                g = max(0, min(255, base_g + grain // 2))
                b = max(0, min(255, base_b + grain // 3))
            pixels.extend([r, g, b])
    write_png('assets/textures/wood_floor.png', w, h, pixels)

    # 2. Museum Wall Plaster (#F7F1E5 warm textured gallery wall)
    pixels = bytearray()
    for y in range(h):
        for x in range(w):
            noise = int(math.sin(x * 12.3 + y * 45.6) * math.cos(x * 7.8 - y * 9.1) * 6)
            r = max(0, min(255, 247 + noise))
            g = max(0, min(255, 241 + noise))
            b = max(0, min(255, 229 + noise))
            pixels.extend([r, g, b])
    write_png('assets/textures/wall_plaster.png', w, h, pixels)

    # 3. Gold Frame Texture (#DDB967 metallic finish)
    pixels = bytearray()
    for y in range(h):
        for x in range(w):
            pattern = int(math.sin((x + y) * 0.15) * 18 + math.cos(x * 0.4) * 12)
            r = max(0, min(255, 221 + pattern))
            g = max(0, min(255, 185 + int(pattern * 0.8)))
            b = max(0, min(255, 103 + int(pattern * 0.4)))
            pixels.extend([r, g, b])
    write_png('assets/textures/gold_frame.png', w, h, pixels)

    # 4. Artistic Starry Night stylized canvas (swirling blues, yellows, golds)
    w_art, h_art = 512, 384
    pixels = bytearray()
    for y in range(h_art):
        for x in range(w_art):
            nx = x / w_art
            ny = y / h_art
            # Swirl math
            dx = nx - 0.55
            dy = ny - 0.4
            dist = math.sqrt(dx*dx + dy*dy)
            angle = math.atan2(dy, dx) + dist * 12.0
            swirl = math.sin(angle * 5) * math.cos(dist * 20)
            
            # Star moon at top right
            mdx = nx - 0.82
            mdy = ny - 0.22
            moon = math.exp(-(mdx*mdx + mdy*mdy) * 80)
            
            # Cypress tree at left
            in_cypress = (nx < 0.25) and (ny > 0.3 - nx*0.5) and abs(nx - 0.15) < (0.12 * ny)
            
            if in_cypress:
                r, g, b = 25, 35, 20
            else:
                base_b = int(140 + swirl * 40 - ny * 50)
                base_r = int(30 + moon * 220 + max(0, swirl) * 40)
                base_g = int(60 + moon * 190 + max(0, swirl) * 50)
                r = max(0, min(255, base_r))
                g = max(0, min(255, base_g))
                b = max(0, min(255, base_b))
            pixels.extend([r, g, b])
    write_png('assets/images/starry_night.png', w_art, h_art, pixels)

    # 5. Sunflowers stylized canvas (warm yellow ochre vase and blooming sunflowers)
    pixels = bytearray()
    for y in range(h_art):
        for x in range(w_art):
            nx = x / w_art
            ny = y / h_art
            # Background warm yellow-ochre
            r, g, b = 235, 195, 100
            
            # Table bottom
            if ny > 0.72:
                r, g, b = 185, 135, 65
            # Vase
            dxv = nx - 0.5
            dyv = ny - 0.65
            if abs(dxv) < 0.12 and 0.5 < ny < 0.8:
                r, g, b = 210, 165, 70
            # Sunflower heads
            centers = [(0.5, 0.35), (0.38, 0.42), (0.62, 0.4), (0.45, 0.25), (0.58, 0.28)]
            for cx, cy in centers:
                d = math.sqrt((nx-cx)**2 + (ny-cy)**2)
                if d < 0.05: # Center brown
                    r, g, b = 90, 55, 25
                elif d < 0.12: # Petals bright gold
                    petals = math.sin(math.atan2(ny-cy, nx-cx)*12) * 0.02
                    if d < 0.11 + petals:
                        r, g, b = 255, 215, 30
            pixels.extend([r, g, b])
    write_png('assets/images/sunflowers.png', w_art, h_art, pixels)

    # 6. Bedroom in Arles stylized canvas (iconic blue walls, wooden bed, warm floor)
    pixels = bytearray()
    for y in range(h_art):
        for x in range(w_art):
            nx = x / w_art
            ny = y / h_art
            if ny < 0.55:
                # Blue bedroom walls
                r, g, b = 110, 155, 195
            else:
                # Reddish terracotta floor
                r, g, b = 185, 120, 95
            # Bed on right side
            if 0.45 < nx < 0.88 and 0.48 < ny < 0.82:
                # Bed frame yellow wood
                r, g, b = 225, 180, 75
                if 0.52 < nx < 0.85 and 0.52 < ny < 0.72:
                    # Red blanket
                    r, g, b = 190, 45, 40
            pixels.extend([r, g, b])
    write_png('assets/images/bedroom_in_arles.png', w_art, h_art, pixels)
    print("All textures created successfully.")

# Function to build a clean, valid GLB (glTF 2.0 Binary) 3D Model
# We will create a low-poly stylized 3D Character sculpture of Vincent Van Gogh (Bust with Straw Hat, Beard, Coat, and Pedestal)
def create_vangogh_glb():
    print("Generating 3D GLB models...")
    # Let's generate a valid GLB file with vertices, indices, normals, and colors for a stylized low-poly Van Gogh bust
    # A GLB consists of:
    # Header (12 bytes): magic 0x46546C67 ('glTF'), version 2, length
    # Chunk 0 (JSON): length, type 0x4E4F534A ('JSON'), JSON bytes (padded to 4-byte alignment)
    # Chunk 1 (BIN): length, type 0x004E4942 ('BIN'), binary buffer
    
    # Let's construct vertices (position x, y, z + normal nx, ny, nz + color r, g, b)
    # We will build colored boxes/prisms for:
    # 1. Base pedestal (Warm Dark Wood #5A3E2B)
    # 2. Torso / Blue Artist Coat (#2B4C6F)
    # 3. Neck & Head / Facial Skin (#E8C5A0)
    # 4. Reddish-Orange Beard & Hair (#D35400)
    # 5. Iconic Yellow Straw Hat (#F1C40F)
    # 6. Artist Palette held in front (#DDB967 with color dabs)
    
    import json
    
    vertices = [] # flat list of float32 (pos_x, pos_y, pos_z, norm_x, norm_y, norm_z)
    colors = []   # flat list of float32 (r, g, b, a)
    indices = []  # flat list of uint16
    
    def add_box(center, size, color):
        cx, cy, cz = center
        sx, sy, sz = [s/2.0 for s in size]
        r, g, b = color
        base_idx = len(vertices) // 6
        
        # 8 corners
        corners = [
            (cx-sx, cy-sy, cz-sz), (cx+sx, cy-sy, cz-sz),
            (cx+sx, cy+sy, cz-sz), (cx-sx, cy+sy, cz-sz),
            (cx-sx, cy-sy, cz+sz), (cx+sx, cy-sy, cz+sz),
            (cx+sx, cy+sy, cz+sz), (cx-sx, cy+sy, cz+sz),
        ]
        
        # 6 faces (each face has 4 vertices with proper normals)
        faces = [
            ([0, 1, 2, 3], (0, 0, -1)), # back
            ([5, 4, 7, 6], (0, 0, 1)),  # front
            ([4, 0, 3, 7], (-1, 0, 0)), # left
            ([1, 5, 6, 2], (1, 0, 0)),  # right
            ([3, 2, 6, 7], (0, 1, 0)),  # top
            ([4, 5, 1, 0], (0, -1, 0))  # bottom
        ]
        
        for quad, normal in faces:
            start_i = len(vertices) // 6
            for idx in quad:
                pos = corners[idx]
                vertices.extend([pos[0], pos[1], pos[2], normal[0], normal[1], normal[2]])
                colors.extend([r, g, b, 1.0])
            indices.extend([start_i, start_i+1, start_i+2, start_i, start_i+2, start_i+3])

    # 1. Pedestal Base
    add_box((0.0, 0.2, 0.0), (0.9, 0.4, 0.9), (0.35, 0.24, 0.17))
    add_box((0.0, 0.45, 0.0), (0.75, 0.1, 0.75), (0.86, 0.72, 0.40)) # Gold plaque rim
    
    # 2. Torso / Artist Coat (Deep Blue)
    add_box((0.0, 0.9, 0.0), (0.6, 0.8, 0.35), (0.16, 0.30, 0.45))
    # Lapel / Scarf (Warm Ochre)
    add_box((0.0, 1.1, 0.16), (0.25, 0.4, 0.08), (0.85, 0.65, 0.25))

    # 3. Head & Neck
    add_box((0.0, 1.35, 0.0), (0.2, 0.15, 0.2), (0.91, 0.77, 0.62)) # Neck
    add_box((0.0, 1.6, 0.03), (0.34, 0.38, 0.34), (0.91, 0.77, 0.62)) # Face
    
    # 4. Iconic Reddish-Orange Beard & Mustache
    add_box((0.0, 1.48, 0.18), (0.36, 0.16, 0.12), (0.83, 0.33, 0.05)) # Beard bottom
    add_box((0.0, 1.55, 0.21), (0.24, 0.06, 0.06), (0.83, 0.33, 0.05)) # Mustache
    
    # 5. Eyes & Eyebrows
    add_box((-0.09, 1.66, 0.21), (0.06, 0.04, 0.03), (0.18, 0.35, 0.30)) # Left eye
    add_box((0.09, 1.66, 0.21), (0.06, 0.04, 0.03), (0.18, 0.35, 0.30))  # Right eye
    add_box((-0.09, 1.71, 0.21), (0.08, 0.03, 0.04), (0.75, 0.30, 0.05)) # Left brow
    add_box((0.09, 1.71, 0.21), (0.08, 0.03, 0.04), (0.75, 0.30, 0.05))  # Right brow
    
    # 6. Yellow Straw Hat (Brim & Crown)
    add_box((0.0, 1.82, 0.02), (0.65, 0.06, 0.65), (0.94, 0.77, 0.15)) # Brim
    add_box((0.0, 1.95, 0.02), (0.38, 0.22, 0.38), (0.94, 0.77, 0.15)) # Crown
    add_box((0.0, 1.86, 0.02), (0.39, 0.05, 0.39), (0.15, 0.28, 0.50)) # Hat blue ribbon
    
    # 7. Artist Palette in front
    add_box((-0.25, 0.9, 0.25), (0.35, 0.03, 0.28), (0.80, 0.60, 0.35)) # Wood palette
    add_box((-0.3, 0.92, 0.2), (0.06, 0.03, 0.06), (0.95, 0.85, 0.15))  # Yellow paint dab
    add_box((-0.2, 0.92, 0.3), (0.06, 0.03, 0.06), (0.15, 0.40, 0.80))  # Blue paint dab
    add_box((-0.15, 0.92, 0.18), (0.06, 0.03, 0.06), (0.85, 0.25, 0.15)) # Red paint dab

    # Convert binary buffers
    pos_norm_bytes = bytearray()
    for val in vertices:
        pos_norm_bytes.extend(struct.pack('<f', val))
    
    col_bytes = bytearray()
    for val in colors:
        col_bytes.extend(struct.pack('<f', val))
        
    ind_bytes = bytearray()
    for val in indices:
        ind_bytes.extend(struct.pack('<H', val))
        
    # Align buffers to 4 bytes
    def align_pad(b):
        pad = (4 - (len(b) % 4)) % 4
        return b + b'\x00' * pad

    pos_norm_bytes = align_pad(pos_norm_bytes)
    col_bytes = align_pad(col_bytes)
    ind_bytes = align_pad(ind_bytes)

    bin_buffer = pos_norm_bytes + col_bytes + ind_bytes
    
    num_vertices = len(vertices) // 6
    num_indices = len(indices)
    
    # Compute min/max for positions
    positions = [vertices[i*6:i*6+3] for i in range(num_vertices)]
    min_pos = [min(p[j] for p in positions) for j in range(3)]
    max_pos = [max(p[j] for p in positions) for j in range(3)]
    
    gltf_json = {
        "asset": {"version": "2.0", "generator": "VanGogh Museum Generator"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": "VincentVanGoghSculpture"}],
        "meshes": [
            {
                "name": "VanGoghMesh",
                "primitives": [
                    {
                        "attributes": {
                            "POSITION": 0,
                            "NORMAL": 1,
                            "COLOR_0": 2
                        },
                        "indices": 3,
                        "material": 0
                    }
                ]
            }
        ],
        "materials": [
            {
                "name": "VertexColorMaterial",
                "pbrMetallicRoughness": {
                    "roughnessFactor": 0.6,
                    "metallicFactor": 0.1
                }
            }
        ],
        "accessors": [
            {
                "bufferView": 0,
                "byteOffset": 0,
                "componentType": 5126,
                "count": num_vertices,
                "type": "VEC3",
                "min": min_pos,
                "max": max_pos
            },
            {
                "bufferView": 0,
                "byteOffset": 12,
                "componentType": 5126,
                "count": num_vertices,
                "type": "VEC3"
            },
            {
                "bufferView": 1,
                "byteOffset": 0,
                "componentType": 5126,
                "count": num_vertices,
                "type": "VEC4"
            },
            {
                "bufferView": 2,
                "byteOffset": 0,
                "componentType": 5123,
                "count": num_indices,
                "type": "SCALAR"
            }
        ],
        "bufferViews": [
            {
                "buffer": 0,
                "byteOffset": 0,
                "byteLength": len(pos_norm_bytes),
                "byteStride": 24,
                "target": 34962
            },
            {
                "buffer": 0,
                "byteOffset": len(pos_norm_bytes),
                "byteLength": len(col_bytes),
                "byteStride": 16,
                "target": 34962
            },
            {
                "buffer": 0,
                "byteOffset": len(pos_norm_bytes) + len(col_bytes),
                "byteLength": len(ind_bytes),
                "target": 34963
            }
        ],
        "buffers": [
            {
                "byteLength": len(bin_buffer)
            }
        ]
    }

    json_str = json.dumps(gltf_json, separators=(',', ':')).encode('utf-8')
    pad_json = (4 - (len(json_str) % 4)) % 4
    json_bytes = json_str + b' ' * pad_json

    total_length = 12 + 8 + len(json_bytes) + 8 + len(bin_buffer)

    header = struct.pack('<I4sI', 0x46546C67, b'\x02\x00\x00\x00'[:4], total_length)
    # Fix header struct pack: magic uint32 0x46546C67, version uint32 2, total_len uint32
    header = struct.pack('<III', 0x46546C67, 2, total_length)

    chunk0_header = struct.pack('<I4s', len(json_bytes), b'JSON')
    chunk1_header = struct.pack('<I4s', len(bin_buffer), b'BIN\x00')

    with open('assets/models/van_gogh_character.glb', 'wb') as f:
        f.write(header)
        f.write(chunk0_header)
        f.write(json_bytes)
        f.write(chunk1_header)
        f.write(bin_buffer)
        
    print("Created assets/models/van_gogh_character.glb successfully!")

if __name__ == '__main__':
    ensure_dirs()
    create_textures()
    create_vangogh_glb()
