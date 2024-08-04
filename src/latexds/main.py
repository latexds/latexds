import os
import sys
from tempfile import NamedTemporaryFile
from typing import Dict

from PIL import Image, ImageOps
import discord
from discord import app_commands
from discord.ext import commands
import sympy


class LaTeXConverter(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.allowed_installs(users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(
        name="latex",
        description="Convert LaTeX to image"
    )
    @app_commands.describe(
        text="LaTeX formatted text"
    )
    async def latex_cmd(
        self,
        interaction: discord.Interaction,

        text: str
    ) -> None:
        with NamedTemporaryFile(delete_on_close=False, suffix=".png") as fp:
            fp.close()
            try:
                sympy.preview(
                    f"$${text}$$",
                    output="png",
                    viewer="file",
                    filename=fp.name,
                    euler=False,
                    dvioptions=['-D', '400']
                )
            except RuntimeError as exc:
                text = str(exc).replace('\\n', '\n')
                out = text[text.find('! '):]
                out = out[:out.find('\n')]
                await interaction.response.send_message(
                    out,
                    ephemeral=True
                )
            else:
                with Image.open(fp.name) as img:
                    img_borders = ImageOps.expand(
                        img,
                        border=20,
                        fill='white'
                    )
                    img_borders.save(fp.name)
                with open(fp.name, "rb") as f:
                    await interaction.response.send_message(
                        file=discord.File(f)
                    )


class Bot(commands.Bot):
    def __init__(self) -> None:
        self.root_import = __name__[:__name__.rfind('.')]

        self._extensions: Dict[str, str] = {}

        super(Bot, self).__init__(
            command_prefix="!",
            intents=discord.Intents.default()
        )

    async def on_ready(self) -> None:
        await self.add_cog(LaTeXConverter(self))
        await self.tree.sync()


def main() -> None:
    bot = Bot()
    if (token := os.getenv("LATEXDS_TOKEN")) is not None:
        bot.run(token)
    elif (token_path := os.getenv("LATEXDS_TOKEN_FILE")) is not None:
        with open(token_path) as f:
            token = f.read()
        bot.run(token)
    else:
        print(f"{sys.argv[0]}: Neither LATEXDS_TOKEN nor LATEXDS_TOKEN_FILE are set", file=sys.stderr)
