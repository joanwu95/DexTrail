"""Render geometry-only web editions; original publication plates stay reusable.

Draws fresh scenes using the existing native renderers, without their editorial
headers or explanatory footers. One union of all frame bounds keeps animation
size and framing fixed. Does not read or edit any existing bitmap.
"""
from pathlib import Path
import importlib.util
import json
from html import escape
from PIL import Image, ImageDraw, ImageChops

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'website/docs/images/knowledge/concept-diagrams'
REVIEW = ROOT / 'research/previews/concept-index-refresh-2026-10-05'


def module(filename):
    spec = importlib.util.spec_from_file_location(filename.replace('-', '_'), ROOT / 'scripts' / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def bounds(frames, paper, margin=24):
    boxes = [ImageChops.difference(frame, Image.new('RGB', frame.size, paper)).getbbox() for frame in frames]
    boxes = [box for box in boxes if box]
    w, h = frames[0].size
    return (max(0, min(box[0] for box in boxes) - margin),
            max(0, min(box[1] for box in boxes) - margin),
            min(w, max(box[2] for box in boxes) + margin),
            min(h, max(box[3] for box in boxes) + margin))


def save_gif(frames, path, duration):
    sample = Image.new('RGB', (frames[0].width * 4, frames[0].height * 2))
    for j in range(8):
        sample.paste(frames[j * len(frames) // 8], ((j % 4) * frames[0].width, (j // 4) * frames[0].height))
    palette = sample.quantize(colors=96, method=Image.Quantize.MEDIANCUT)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    indexed[0].save(path, save_all=True, append_images=indexed[1:], duration=duration, loop=0, optimize=True, disposal=1)


def save_review(slug, frames, paper):
    # Six distinct phases per animated entry, with the same bounds as its GIF.
    width = 480
    height = round(frames[0].height * width / frames[0].width)
    sheet = Image.new('RGB', (width * 3, height * 2), paper)
    for j in range(6):
        frame = frames[j * len(frames) // 6].resize((width, height), Image.Resampling.LANCZOS)
        sheet.paste(frame, ((j % 3) * width, (j // 3) * height))
    sheet.save(REVIEW / (slug + '-phases.png'))


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true')
    parser.add_argument('--only', nargs='+', help='Regenerate selected concept slugs')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    grasp = module('render-grasp-concepts.py')

    class DiagramCanvas(grasp.Canvas):
        def __init__(self, plate):
            self.plate = plate
            self.im = Image.new('RGB', (grasp.W * grasp.AA, grasp.H * grasp.AA), grasp.PAPER)
            self.d = ImageDraw.Draw(self.im)
            self.svg = [f'<rect width="{grasp.W}" height="{grasp.H}" fill="{grasp.PAPER}"/>']
            self.text_boxes = []

        def footer(self, *args, **kwargs):
            pass

        def text(self, point, value, *args, **kwargs):
            if self.plate['slug'] == 'underactuation' and value == 'Tendon + passive joint':
                super().text(point, 'Tendon +', *args, **kwargs)
                super().text((point[0], point[1] + 25), 'passive joint', *args, **kwargs)
                return
            if value.casefold() != self.plate['title'].casefold():
                super().text(point, value, *args, **kwargs)

    grasp.Canvas = DiagramCanvas
    records = []
    for plate in grasp.PLATES:
        if args.only and plate['slug'] not in args.only:
            continue
        count = grasp.FRAMES if plate['animated'] and not args.preview else 1
        scenes = [grasp.scene(plate, i / count if count > 1 else .28) for i in range(count)]
        frames = [scene.finish() for scene in scenes]
        box = bounds(frames, grasp.PAPER)
        frames = [frame.crop(box) for frame in frames]
        frames[min(len(frames) - 1, 22)].save(OUT / (plate['slug'] + '.png'))
        x, y, right, bottom = box
        width, height = right - x, bottom - y
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="{x} {y} {width} {height}" role="img"><title>{escape(plate["title"])}</title><desc>{escape(plate["alt"])}</desc>'
        (OUT / (plate['slug'] + '.svg')).write_text(svg + '\n' + '\n'.join(scenes[min(len(scenes)-1, 22)].svg) + '\n</svg>', encoding='utf-8')
        if count > 1:
            save_gif(frames, OUT / (plate['slug'] + '.gif'), grasp.MS)
            save_review(plate['slug'], frames, grasp.PAPER)
        records.append({'slug': plate['slug'], 'size': [width, height], 'frames': count, 'loop': 0 if count > 1 else None, 'labels': sorted({value for scene in scenes for value, _ in scene.text_boxes})})
        print('Web diagram: ' + plate['slug'], flush=True)

    motions = module('render-hand-motions-dextrail.py')
    original_canvas = motions.EditorialCanvas

    class MotionDiagramCanvas(original_canvas):
        def text(self, xy, value, *args, **kwargs):
            if value != 'Circumduction' and xy != (400, 643):
                super().text(xy, value, *args, **kwargs)

        def line(self, pts, *args, **kwargs):
            if pts != [(34, 576), (766, 576)]:
                super().line(pts, *args, **kwargs)

    motions.EditorialCanvas = MotionDiagramCanvas

    def heading(canvas, *args):
        canvas.diagram = True

    def status(canvas, first, second, outward, hold, cn):
        # Phase labels carry time-varying state, rather than restating a title.
        if not second:
            return
        canvas.diagram = False
        word = first if outward else second
        canvas.text((400, 592), word, 20, motions.ACCENT, center=True)

    motions.heading = motions.m.heading = heading
    motions.status = motions.m.status = status
    motions.m.Canvas = MotionDiagramCanvas
    motions.m.palm = motions.palm
    renderers = motions.m.RENDERERS[:3] + [('thumb-palmar-abduction-adduction', motions.palmar_abduction), motions.m.RENDERERS[4], ('finger-circumduction', motions.circumduction)]
    for slug, render in renderers:
        if args.only and slug not in args.only:
            continue
        count = 1 if args.preview else motions.FRAMES
        frames = [render(i if count > 1 else 32) for i in range(count)]
        box = bounds(frames, motions.PAPER)
        frames = [frame.crop(box) for frame in frames]
        frames[min(32, count - 1)].save(OUT / (slug + '.png'))
        if count > 1:
            save_gif(frames, OUT / (slug + '.gif'), motions.DURATION)
            save_review(slug, frames, motions.PAPER)
        records.append({'slug': slug, 'size': list(frames[0].size), 'frames': count, 'loop': 0 if count > 1 else None})
        print('Web motion: ' + slug, flush=True)
    audit = REVIEW / 'geometry-audit.json'
    if args.only and audit.exists():
        merged = {record['slug']: record for record in json.loads(audit.read_text(encoding='utf-8'))}
        merged.update({record['slug']: record for record in records})
        records = list(merged.values())
    anatomy = OUT / 'hand-anatomy.png'
    if anatomy.exists() and not any(record['slug'] == 'hand-anatomy' for record in records):
        with Image.open(anatomy) as im:
            records.append({'slug': 'hand-anatomy', 'size': list(im.size), 'frames': 1, 'loop': None})
    audit.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    # Named inventory: every web diagram is present in the visual review.
    sheet = Image.new('RGB', (1600, 8 * 270), grasp.PAPER)
    draw = ImageDraw.Draw(sheet)
    for j, record in enumerate(records):
        with Image.open(OUT / (record['slug'] + '.png')) as im:
            im.thumbnail((380, 220), Image.Resampling.LANCZOS)
            x, y = (j % 4) * 400, (j // 4) * 270
            sheet.paste(im, (x + (400 - im.width) // 2, y + 35))
            draw.text((x + 10, y + 10), record['slug'], fill=grasp.INK, font=grasp.font(7))
    sheet.save(REVIEW / 'all-geometry-diagrams.png')


if __name__ == '__main__':
    main()
