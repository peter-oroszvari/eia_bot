import io
from PIL import Image
import discord


async def save_and_send_image(interaction, filename):
    img = Image.open(filename)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    await interaction.followup.send(file=discord.File(img_bytes, filename))
