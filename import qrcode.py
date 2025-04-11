import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from PIL import Image, ImageDraw, ImageFont

data = input("Enter the URL or text to encode in the QR code: ")

qr = qrcode.QRCode(
    version=1,
    box_size=30,
    border=5,
    error_correction=qrcode.constants.ERROR_CORRECT_H
)

qr.add_data(data)
qr.make(fit=True)

qr_img = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(),
    fill_color="red",
    back_color="black"
).convert("RGB")

try:
    logo = Image.open("logo.png")
    logo_size = 100
    logo = logo.resize((logo_size, logo_size))
    pos = ((qr_img.size[0] - logo_size) // 2, (qr_img.size[1] - logo_size) // 2)
    qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)
except FileNotFoundError:
    print("Logo not found — skipping logo embed.")

canvas = Image.new('RGB', (qr_img.width, qr_img.height + 80), 'black')
canvas.paste(qr_img, (0, 0))

draw = ImageDraw.Draw(canvas)
label = "Scan Me!"
bbox = draw.textbbox((0, 0), label)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
text_position = ((canvas.width - text_width) // 2, qr_img.height + 20)
draw.text(text_position, label, fill="white")

canvas.save("fancy_qr1.png")
print("✅ Fancy QR code saved as 'fancy_qr.png'")
