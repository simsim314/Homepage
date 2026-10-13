#!/usr/bin/env python3
"""Solid 3D blue tiles and a zero-padded glider input assembly.

Standalone Python file. Dependencies: numpy, matplotlib, trimesh, manifold3d.
    python blue_tiles_3d.py
    python blue_tiles_3d.py --out /tmp/blue-tiles

Confirmed with Michael:
- Each complete Life cell has ONE value, identical at all four corner outputs.
- Circle=0; plus=1. Previous layer outputs protrude; blue inputs are recesses.
- Life corner centres: L/6 and 5L/6. Blue input centres: L/3 and 2L/3.
- Blue input REGION is a contiguous 2x2 of L/3 squares, with L/6 margins.
- Life pitch = blue width = L=60, centred between FOUR adjacent cells.
- Blue top: four repeated 2x2 groups, each 0.4L wide, with nine raised X blockers in the 0.2L cross separator.

Rendering dimensions (body thickness and stud height/radius) are modelling choices, not recovered production specifications.
Inputs are exact nominal counterparts of the lower studs. There is no
wildcard or unfilled socket in the intended assembled interfaces. No snap
retention, fabrication clearance, or other computational layers are included.
An unmatched piece may physically rest on a blank surface; that is NOT full
fit. The tests distinguish collision from unused socket volume.
"""

from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from itertools import product
import json
from pathlib import Path

import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource, to_rgba
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

LIFE = 60.0
BLUE = LIFE
OUTPUT_GAP = .2
OUTPUT_CENTRES = (.1, .3, .7, .9)
LIFE_H = 5.0
BLUE_H = 6.0
STUD_H = 2.0
OUTER_R = 2.6
INNER_R = 1.7
BAR_W = .9
SECTIONS = 48
PAPER = '#f6f5ef'
INK = '#233c43'
GLIDER = ((0, 1, 0), (0, 0, 1), (1, 1, 1))
FACE_NAMES = ('All circles', 'One plus', 'Two adjacent pluses',
              'Two diagonal pluses', 'Three pluses', 'All pluses')


def rotate(face):
    return tuple(tuple(row) for row in zip(*face[::-1]))


def canonical(face):
    versions = []
    for _ in range(4):
        versions.append(face)
        face = rotate(face)
    return min(versions)


def output(face):
    return tuple(tuple(face[r % 2][c % 2] for c in range(4)) for r in range(4))


def box(width, length, height):
    shape = trimesh.creation.box(extents=(width, length, height))
    shape.apply_translation((width / 2, length / 2, height / 2))
    return shape


@lru_cache(maxsize=None)
def symbol(bit, height=STUD_H):
    """A real annular extrusion or a plus formed by two crossed bars."""
    if bit == 0:
        shape = trimesh.creation.annulus(r_min=INNER_R, r_max=OUTER_R,
                                         height=height, sections=SECTIONS)
        shape.apply_translation((0, 0, height / 2))
        return shape
    a = trimesh.creation.box(extents=(2 * OUTER_R, BAR_W, height))
    b = trimesh.creation.box(extents=(BAR_W, 2 * OUTER_R, height))
    a.apply_translation((0, 0, height / 2))
    b.apply_translation((0, 0, height / 2))
    return trimesh.boolean.union((a, b), engine='manifold')



@lru_cache(maxsize=None)
def fixed_blocker():
    """One fixed X per separator square. Not a don't-care connector."""
    radius, width = BLUE*.075, BLUE/60
    a=trimesh.creation.box(extents=(2*radius,width,STUD_H))
    b=trimesh.creation.box(extents=(width,2*radius,STUD_H))
    shape=trimesh.boolean.union((a,b),engine='manifold')
    shape.apply_transform(trimesh.transformations.rotation_matrix(np.pi/4,(0,0,1)))
    shape.apply_translation((0,0,STUD_H/2))
    return shape


def moved(mesh, xyz):
    mesh = mesh.copy()
    mesh.apply_translation(xyz)
    return mesh


def annotate(mesh, body, studs, cavity=False):
    colors = np.tile(to_rgba(body), (len(mesh.faces), 1))
    z = mesh.triangles_center[:, 2]
    threshold = BLUE_H if cavity else LIFE_H
    colors[z > threshold + .01] = to_rgba(studs)
    if cavity:
        colors[(z > .01) & (z < STUD_H + .01)] = to_rgba('#264b63')
    mesh.visual.face_colors = (colors * 255).astype(np.uint8)
    return mesh


@lru_cache(maxsize=None)
def life_cell(bit):
    anchors = (LIFE / 6, LIFE * 5 / 6)
    pieces = [box(LIFE, LIFE, LIFE_H)]
    # ONE value drives ALL FOUR ports. No independent corner assignments.
    for y, x in product(anchors, repeat=2):
        pieces.append(moved(symbol(bit), (x, y, LIFE_H)))
    mesh = trimesh.boolean.union(pieces, engine='manifold')
    return annotate(mesh, '#e8e7df' if bit == 0 else '#274b5e', '#5f899b' if bit == 0 else '#85c3c8')


@lru_cache(maxsize=None)
def blue_tile(face):
    mesh = box(BLUE, BLUE, BLUE_H)
    cuts = []
    for r, c in product(range(2), repeat=2):
        x, y = (BLUE / 3, BLUE * 2 / 3)[c], (BLUE / 3, BLUE * 2 / 3)[r]
        # Extend just below the surface to make a reliably open cavity;
        # its roof remains exactly at STUD_H, matching the raised lower stud.
        cuts.append(moved(symbol(face[r][c], STUD_H + .01), (x, y, -.01)))
    mesh = trimesh.boolean.difference([mesh, *cuts], engine='manifold')
    top = output(face)
    studs = [moved(symbol(top[r][c]), (OUTPUT_CENTRES[c] * BLUE,
                                    OUTPUT_CENTRES[r] * BLUE, BLUE_H))
             for r, c in product(range(4), repeat=2)]
    studs.extend(moved(fixed_blocker(),((c+.5)*BLUE/5,(r+.5)*BLUE/5,BLUE_H))
                 for r,c in product(range(5),repeat=2) if r==2 or c==2)
    assert len(studs)==25  # 16 data outputs plus nine fixed registration blockers.
    mesh = trimesh.boolean.union([mesh, *studs], engine='manifold')
    return annotate(mesh, '#7795b1', '#64b6bc', True)


def orient_tile(mesh, turns):
    mesh = moved(mesh, (-BLUE / 2, -BLUE / 2, 0))
    mesh.apply_transform(trimesh.transformations.rotation_matrix(turns * np.pi / 2, (0, 0, 1)))
    mesh.apply_translation((BLUE / 2, BLUE / 2, 0))
    return mesh


def variant(face):
    base = canonical(face)
    candidate = base
    for turns in range(4):
        if candidate == face:
            return orient_tile(blue_tile(base), turns), base, turns
        candidate = rotate(candidate)
    raise AssertionError('Missing blue orientation')


def intersection_volume(a, b):
    result = trimesh.boolean.intersection((a, b), engine='manifold')
    if not len(result.faces):
        return 0.0
    triangles = result.triangles
    # Coplanar contact can have zero volume. Compute signed tetrahedra
    # directly rather than requesting a centre of mass for a zero-volume set.
    return abs(float(np.einsum('ij,ij->i', triangles[:, 0],
                              np.cross(triangles[:, 1], triangles[:, 2])).sum() / 6))


def build_assembly():
    field = ((0, 0, 0, 0, 0),) + tuple((0, *row, 0) for row in GLIDER) + ((0, 0, 0, 0, 0),)
    lower, upper, records = [], [], []
    for r, c in product(range(5), repeat=2):
        lower.append((f'life-{r}-{c}', moved(life_cell(field[r][c]), (c * LIFE, r * LIFE, 0))))
    worst = 0.0
    checked = 0
    for r, c in product(range(4), repeat=2):
        face = tuple(tuple(field[r + dr][c + dc] for dc in range(2)) for dr in range(2))
        tile, base, turns = variant(face)
        origin = (c * LIFE + LIFE * .5, r * LIFE + LIFE * .5, LIFE_H)
        tile.apply_translation(origin)
        upper.append((f'blue-{r}-{c}', tile))
        records.append({'junction': [r + 1, c + 1], 'input': face,
                        'top': output(face), 'canonical': base, 'quarter_turns': turns,
                        'origin': origin})
        for dr, dc in product(range(2), repeat=2):
            lower_mesh = lower[(r + dr) * 5 + c + dc][1]
            volume = intersection_volume(tile, lower_mesh)
            worst = max(worst, volume)
            assert volume < .002, (r, c, dr, dc, volume)
            # Exact nominal cavity profiles match the actual cell's one bit.
            assert face[dr][dc] == field[r + dr][c + dc]
            local_x = (BLUE / 3, BLUE * 2 / 3)[dc] + origin[0]
            local_y = (BLUE / 3, BLUE * 2 / 3)[dr] + origin[1]
            lower_x = (c + dc) * LIFE + (LIFE * 5 / 6 if dc == 0 else LIFE / 6)
            lower_y = (r + dr) * LIFE + (LIFE * 5 / 6 if dr == 0 else LIFE / 6)
            assert np.allclose((local_x, local_y), (lower_x, lower_y))
            checked += 1
        for dr, dc in product(range(2), repeat=2):
            assert tuple(tuple(output(face)[dr * 2 + a][dc * 2 + b] for b in range(2))
                         for a in range(2)) == face
    assert sum(map(sum, field)) == 5
    return lower, upper, {'input_grid': field, 'life_cells': 25, 'live_cells': 5,
                          'blue_pieces': 16, 'verified_interfaces': checked,
                          'maximum_solid_overlap_volume': worst, 'tiles': records}


def verify_mesh(mesh):
    assert mesh.is_watertight
    assert mesh.is_winding_consistent
    assert mesh.volume > 0
    assert len(mesh.split()) == 1
    return {'triangles': len(mesh.faces), 'volume': float(mesh.volume),
            'watertight': True, 'connected': True}


def add_mesh(ax, mesh, elev=48, azim=-65):
    # Cull rear faces before Matplotlib's painter sorting, so triangulated
    # backs cannot paint over the exposed top or the underside recesses.
    el, az = np.radians((elev, azim))
    toward_camera = np.array([np.cos(az)*np.cos(el), -np.sin(az)*np.cos(el), np.sin(el)])
    visible = mesh.face_normals @ toward_camera > 1e-8
    colors = mesh.visual.face_colors[visible].astype(float) / 255
    collection = Poly3DCollection(mesh.triangles[visible], facecolors=colors,
                                  linewidths=0, shade=True,
                                  lightsource=LightSource(azdeg=315, altdeg=52))
    ax.add_collection3d(collection)


def frame(ax, bounds, elev=37, azim=-62):
    low, high = np.array(bounds)
    span = high - low
    center = (high + low) / 2
    margin = max(span[0], span[1]) * .06
    ax.set_xlim(center[0] - span[0] / 2 - margin, center[0] + span[0] / 2 + margin)
    ax.set_ylim(center[1] - span[1] / 2 - margin, center[1] + span[1] / 2 + margin)
    ax.set_zlim(min(0, low[2]), high[2] + margin * .2)
    ax.set_box_aspect((span[0] + 2 * margin, span[1] + 2 * margin, max(span[2], 5)))
    ax.invert_yaxis()  # Rows run downwards, as in the original glider grid.
    ax.view_init(elev=elev, azim=azim)
    ax.set_proj_type('ortho')
    ax.set_axis_off()
    ax.set_facecolor(PAPER)


def draw_catalogue(faces, path):
    fig = plt.figure(figsize=(19, 11), facecolor=PAPER)
    fig.suptitle('Six blue tiles — 16 data outputs + nine raised X blockers',
                 color=INK, fontsize=22, y=.98)
    for i, face in enumerate(faces):
        ax = fig.add_subplot(2, 3, i + 1, projection='3d')
        top = blue_tile(face).copy()
        bottom = moved(top, (-BLUE / 2, -BLUE / 2, 0))
        bottom.apply_transform(trimesh.transformations.rotation_matrix(np.pi, (1, 0, 0)))
        bottom.apply_translation((BLUE / 2 + BLUE + 18, BLUE / 2, BLUE_H + STUD_H))
        add_mesh(ax, top)
        add_mesh(ax, bottom)
        frame(ax, ((0, 0, 0), (2 * BLUE + 18, BLUE, 8)), elev=48, azim=-65)
        ax.set_title(FACE_NAMES[i], fontsize=16, color=INK, pad=5)
        ax.text2D(.18, .07, 'TOP · data + X blockers', transform=ax.transAxes, fontsize=10, color=INK)
        ax.text2D(.57, .07, 'BOTTOM · 4 recesses', transform=ax.transAxes, fontsize=10, color=INK)
    fig.text(.5, .015, 'Right-hand copies are physically flipped to expose the underside. Circle = 0; plus = live. Nominal geometry, no print clearance.',
             ha='center', fontsize=11, color=INK)
    fig.subplots_adjust(top=.91, bottom=.06, left=.01, right=.99, hspace=.13, wspace=.01)
    fig.savefig(path, dpi=160, facecolor=PAPER)
    plt.close(fig)


def draw_glider(lower, upper, path):
    fig = plt.figure(figsize=(20, 10), facecolor=PAPER)
    fig.suptitle('Glider + one zero-cell border — uniform Life cells below, blue routing above',
                 color=INK, fontsize=22, y=.98)
    for i, gap in enumerate((0.0, 35.0)):
        ax = fig.add_subplot(1, 2, i + 1, projection='3d')
        for _, mesh in lower:
            add_mesh(ax, mesh, azim=-76)
        for _, mesh in upper:
            add_mesh(ax, moved(mesh, (0, 0, gap)), azim=-76)
        frame(ax, ((0, 0, 0), (300, 300, 13 + gap)), elev=48, azim=-76)
        ax.set_title('Assembled: inputs seated on matching outputs' if not gap else 'Exploded: blue pieces lifted for inspection',
                     color=INK, fontsize=15, pad=6)
    fig.text(.5, .035, '25 Life cells; 5 live. Each cell has four IDENTICAL corner outputs. 16 blue pieces each read four ADJACENT cells.',
             ha='center', color=INK, fontsize=12)
    fig.text(.5, .012, 'This is the input + blue-routing structure, not a complete Life-generation computer. Live-cell bodies are dark; zero-cell bodies are light.',
             ha='center', color=INK, fontsize=11)
    fig.subplots_adjust(top=.88, bottom=.09, left=.01, right=.99, wspace=.015)
    fig.savefig(path, dpi=160, facecolor=PAPER)
    plt.close(fig)


def export_scene(parts, path):
    scene = trimesh.Scene()
    for name, mesh in parts:
        scene.add_geometry(mesh, geom_name=name, node_name=name)
    path.write_bytes(scene.export(file_type='glb'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path(__file__).parent / 'blue-solids')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    faces = sorted({canonical((bits[:2], bits[2:])) for bits in product((0, 1), repeat=4)})
    assert len(faces) == 6
    mesh_report = {}
    catalogue = []
    for i, face in enumerate(faces):
        mesh = blue_tile(face)
        mesh_report[f'blue-{i}'] = verify_mesh(mesh)
        mesh.export(args.out / f'blue-{i}.stl')
        catalogue.append((f'blue-{i}', moved(mesh, ((i % 3) * (BLUE+18), (i // 3) * (BLUE+18), 0))))
        print(f'Built blue-{i}: {FACE_NAMES[i]}', flush=True)
    for bit in (0, 1):
        mesh_report[f'life-{bit}'] = verify_mesh(life_cell(bit))
        life_cell(bit).export(args.out / f'life-{bit}.stl')
    lower, upper, report = build_assembly()
    report['meshes'] = mesh_report
    report['output_geometry'] = {'gap_fraction': OUTPUT_GAP, 'group_width_fraction': .4,
                                 'symbol_centre_fractions': OUTPUT_CENTRES,
                                 'fixed_X_blockers':9,'blocker_half_arm_length':BLUE*.075,
                                 'blocker_bar_width':BLUE/60}
    report['dimensions'] = {'life_width': LIFE, 'blue_width': BLUE, 'life_body_height': LIFE_H,
                            'blue_body_height': BLUE_H, 'stud_height': STUD_H,
                            'circle_outer_radius': OUTER_R, 'circle_inner_radius': INNER_R,
                            'plus_bar_width': BAR_W}
    report['scope'] = 'Nominal modelling dimensions. Full-fit intended interfaces verified; no print tolerance or snap-fit validation.'
    (args.out / 'validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf8')
    export_scene(catalogue, args.out / 'six-blue-tiles.glb')
    export_scene(lower + upper, args.out / 'glider-assembled.glb')
    export_scene(lower + [(name, moved(mesh, (0, 0, 35))) for name, mesh in upper],
                 args.out / 'glider-exploded.glb')
    draw_catalogue(faces, args.out / 'six-blue-tiles.png')
    draw_glider(lower, upper, args.out / 'glider-structure.png')
    print(f'PASS: 8 connected watertight meshes; {report["verified_interfaces"]} assembled interfaces.', flush=True)
    print(args.out, flush=True)


if __name__ == '__main__':
    main()
