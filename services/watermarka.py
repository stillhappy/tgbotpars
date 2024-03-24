from PIL import Image, ImageDraw, ImageFont

def add_watermark_overlay(input_image_path, output_image_path, watermark_text):
    input_image = Image.open(input_image_path)
    input_image = input_image.convert('RGBA')
    width, height = input_image.size

    overlay = Image.new('RGBA', input_image.size, (255, 255, 255, 0))

    draw = ImageDraw.Draw(overlay)
    watermark_color_pattern = (255, 255, 255, 30)
    for i in range(0, width+height, 50):
        draw.line([(0, height - i), (i, height)], fill=watermark_color_pattern, width=5)

    font_size = 50
    font = ImageFont.truetype('OpenSans-Regular.ttf', font_size)

    text_bbox = draw.textbbox((0, 0), watermark_text, font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    x = (width - text_width) // 2
    y = (height - text_height) // 2
    watermark_color_text = (1, 255, 100, 50)

    draw.text((x, y), watermark_text, fill=watermark_color_text, font=font)

    watermarked_image = Image.alpha_composite(input_image, overlay)

    watermarked_image.save(output_image_path)

