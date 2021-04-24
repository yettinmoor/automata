import os
from PIL import Image, ImageDraw, ImageFont

W = 501
H = 1000
CELL_SIZE = 10


def draw_row(draw, row, drawn_rows):
    for i, x in enumerate(row):
        if x == 1:
            p1 = i * CELL_SIZE, drawn_rows * CELL_SIZE
            p2 = (i + 1) * CELL_SIZE, (drawn_rows + 1) * CELL_SIZE
            draw.rectangle((p1, p2), 'black')


def apply_rule(row, rule):
    above_seq = (row[i:i+3] for i in range(0, len(row) - 2))
    new_row = [
        1 if rule & (1 << (above[0] << 2 | above[1] << 1 | above[2])) else 0
        for x, above in zip(row[1:], above_seq)
    ]
    return [0] + new_row + [0]


font = ImageFont.truetype('Inconsolata-Regular.ttf', size=300)

try:
    os.mkdir('rules')
except:
    pass

for rule in range(0x100):
    print(f'Drawing rule {rule}')

    # Header
    header = Image.new('1', (W * CELL_SIZE, 600), color='white')
    title = f'Rule {rule}'
    fw, fh = font.getsize(title)
    ImageDraw.Draw(header).text(
        ((W * CELL_SIZE - fw) / 2, (header.height - fh) / 2), title, font=font)

    # Pattern
    pattern = Image.new('1', (W * CELL_SIZE, H * CELL_SIZE), color='white')

    drawn_rows = 0
    row = [0] * W
    row[len(row) // 2] = 1

    draw = ImageDraw.Draw(pattern)
    draw_row(draw, row, 0)

    for i in range(H):
        row = apply_rule(row, rule)
        draw_row(draw, row, i + 1)

    # Concat and save
    im = Image.new('1', (header.width, header.height + pattern.height))
    im.paste(header)
    im.paste(pattern, (0, header.height))

    im.save(f'rules/r{rule:02x}.png')
