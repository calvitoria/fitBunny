import discord
from discord.ext import commands
import os
from config import DISCORD_TOKEN, GUILD_ID
from discord import Object


class FitBunny(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        self.guild = Object(id=GUILD_ID)

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded cog: {filename}")

        self.tree.copy_global_to(guild=self.guild)
        await self.tree.sync(guild=self.guild)
        print("Slash commands synced.")

    async def on_ready(self):
        print("🐇 FitBunny is online!")


bot = FitBunny()
bot.run(DISCORD_TOKEN)
