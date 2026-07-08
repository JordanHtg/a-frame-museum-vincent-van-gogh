import struct
import json

def create_simple_glb(filepath, mesh_name, boxes):
    # boxes: list of (center, size, color)
    vertices = []
    colors = []
    indices = []
    
    def add_box(center, size, color):
        cx, cy, cz = center
        sx, sy, sz = [s/2.0 for s in size]
        r, g, b = color
        
        corners = [
            (cx-sx, cy-sy, cz-sz), (cx+sx, cy-sy, cz-sz),
            (cx+sx, cy+sy, cz-sz), (cx-sx, cy+sy, cz-sz),
            (cx-sx, cy-sy, cz+sz), (cx+sx, cy-sy, cz+sz),
            (cx+sx, cy+sy, cz+sz), (cx-sx, cy+sy, cz+sz),
        ]
        
        faces = [
            ([0, 1, 2, 3], (0, 0, -1)),
            ([5, 4, 7, 6], (0, 0, 1)),
            ([4, 0, 3, 7], (-1, 0, 0)),
            ([1, 5, 6, 2], (1, 0, 0)),
            ([3, 2, 6, 7], (0, 1, 0)),
            ([4, 5, 1, 0], (0, -1, 0))
        ]
        
        for quad, normal in faces:
            start_i = len(vertices) // 6
            for idx in quad:
                pos = corners[idx]
                vertices.extend([pos[0], pos[1], pos[2], normal[0], normal[1], normal[2]])
                colors.extend([r, g, b, 1.0])
            indices.extend([start_i, start_i+1, start_i+2, start_i, start_i+2, start_i+3])

    for c, s, col in boxes:
        add_box(c, s, col)

    pos_norm_bytes = bytearray()
    for val in vertices:
        pos_norm_bytes.extend(struct.pack('<f', val))
    
    col_bytes = bytearray()
    for val in colors:
        col_bytes.extend(struct.pack('<f', val))
        
    ind_bytes = bytearray()
    for val in indices:
        ind_bytes.extend(struct.pack('<H', val))
        
    def align_pad(b):
        pad = (4 - (len(b) % 4)) % 4
        return b + b'\x00' * pad

    pos_norm_bytes = align_pad(pos_norm_bytes)
    col_bytes = align_pad(col_bytes)
    ind_bytes = align_pad(ind_bytes)

    bin_buffer = pos_norm_bytes + col_bytes + ind_bytes
    num_vertices = len(vertices) // 6
    num_indices = len(indices)
    
    positions = [vertices[i*6:i*6+3] for i in range(num_vertices)]
    min_pos = [min(p[j] for p in positions) for j in range(3)]
    max_pos = [max(p[j] for p in positions) for j in range(3)]
    
    gltf_json = {
        "asset": {"version": "2.0", "generator": "VanGogh Museum Generator"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": mesh_name}],
        "meshes": [
            {
                "name": mesh_name + "_mesh",
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
                "name": "Material",
                "pbrMetallicRoughness": {
                    "roughnessFactor": 0.5,
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
        "buffers": [{"byteLength": len(bin_buffer)}]
    }

    json_str = json.dumps(gltf_json, separators=(',', ':')).encode('utf-8')
    pad_json = (4 - (len(json_str) % 4)) % 4
    json_bytes = json_str + b' ' * pad_json

    total_length = 12 + 8 + len(json_bytes) + 8 + len(bin_buffer)
    header = struct.pack('<III', 0x46546C67, 2, total_length)
    chunk0_header = struct.pack('<I4s', len(json_bytes), b'JSON')
    chunk1_header = struct.pack('<I4s', len(bin_buffer), b'BIN\x00')

    with open(filepath, 'wb') as f:
        f.write(header)
        f.write(chunk0_header)
        f.write(json_bytes)
        f.write(chunk1_header)
        f.write(bin_buffer)

if __name__ == '__main__':
    # Museum Bench (Wood Seat + Gold/Brown Legs)
    bench_boxes = [
        ((0.0, 0.45, 0.0), (1.6, 0.08, 0.6), (0.55, 0.37, 0.24)), # seat
        ((-0.65, 0.22, -0.22), (0.08, 0.44, 0.08), (0.35, 0.24, 0.17)),
        ((0.65, 0.22, -0.22), (0.08, 0.44, 0.08), (0.35, 0.24, 0.17)),
        ((-0.65, 0.22, 0.22), (0.08, 0.44, 0.08), (0.35, 0.24, 0.17)),
        ((0.65, 0.22, 0.22), (0.08, 0.44, 0.08), (0.35, 0.24, 0.17)),
    ]
    create_simple_glb('assets/models/museum_bench.glb', 'MuseumBench', bench_boxes)

    # Decorative Flower Pot with Sunflowers
    pot_boxes = [
        ((0.0, 0.3, 0.0), (0.5, 0.6, 0.5), (0.35, 0.24, 0.17)), # Terracotta/Wood pot
        ((0.0, 0.62, 0.0), (0.56, 0.06, 0.56), (0.87, 0.73, 0.40)), # Gold rim
        ((0.0, 0.9, 0.0), (0.65, 0.5, 0.65), (0.15, 0.35, 0.18)), # Foliage
        ((0.15, 1.15, 0.1), (0.25, 0.25, 0.05), (0.95, 0.85, 0.15)), # Sunflower 1
        ((-0.15, 1.12, -0.1), (0.22, 0.22, 0.05), (0.95, 0.82, 0.15)), # Sunflower 2
    ]
    create_simple_glb('assets/models/flower_pot.glb', 'FlowerPot', pot_boxes)
    print("Bench and flower pot GLB files created!")
