import discord
import os
import aiohttp
import random

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

IMAGEM_DIR = "imagens"
if not os.path.exists(IMAGEM_DIR):
    os.makedirs(IMAGEM_DIR)

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Só responde a menções diretas, ignorando replies
    if client.user in message.mentions and message.reference is None:
        attachments = message.attachments

        if attachments:
            # Salvar todas as imagens anexadas
            saved_any = False
            async with aiohttp.ClientSession() as session:
                for attachment in attachments:
                    if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                        async with session.get(attachment.url) as resp:
                            if resp.status == 200:
                                data = await resp.read()
                                filename = f"{message.id}_{attachment.filename}"
                                filepath = os.path.join(IMAGEM_DIR, filename)
                                with open(filepath, 'wb') as f:
                                    f.write(data)
                                saved_any = True
            if saved_any:
                await message.channel.send("Imagem(s) salva(s) com sucesso!")
            else:
                await message.channel.send("Nenhuma imagem válida para salvar.")
            return

        else:
            # Envia 1 imagem aleatória da pasta
            imagens_salvas = [
                os.path.join(IMAGEM_DIR, f)
                for f in os.listdir(IMAGEM_DIR)
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))
            ]
            if imagens_salvas:
                imagem_aleatoria = random.choice(imagens_salvas)
                await message.channel.send(file=discord.File(imagem_aleatoria))
            else:
                await message.channel.send("Ainda não há imagens salvas.")

# Lembre-se de rodar o bot usando o token como variável de ambiente!
import os
client.run(os.getenv("DISCORD_TOKEN"))



