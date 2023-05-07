from os import environ
import disnake
import openai  # хуета

import sqlite3
from random import choice
from disnake.ext import commands
from disnake import Intents, ApplicationCommandInteraction, Message, ButtonStyle, ui, MessageInteraction, DMChannel

# set API key for OpenAI
openai.api_key = environ.get("OPENAI_TOKEN")

# create bot object
bot = commands.Bot(
    intents=Intents.all(),
    command_prefix="!"
)

# set up database connection
conn = sqlite3.connect('GDB.db', check_same_thread=False)
c = conn.cursor()


class RatingFromUser(disnake.ui.View):
    message: disnake.Message

    def __init__(self):
        super().__init__(timeout=1.0)

    async def on_timeout(self):
        self.disabled = True
        await self.message.edit(view=self)

    @disnake.ui.button(emoji="👎", style=ButtonStyle.red)
    async def bad(self, button: ui.Button, inter: MessageInteraction):
        await inter.response.send_message(f"Оценка {button.label} принята", ephemeral=True)
        self.stop()

    @disnake.ui.button(emoji="🤝", style=ButtonStyle.grey)
    async def normal(self, button: disnake.ui.Button, inter: MessageInteraction):
        await inter.response.send_message(f"Оценка {button.label} принята", ephemeral=True)
        self.stop()

    @disnake.ui.button(emoji="👍", style=ButtonStyle.green)
    async def good(self, button: disnake.ui.Button, inter: MessageInteraction):
        await inter.response.send_message(f"Оценка {button.label} принята", ephemeral=True)
        self.stop()


async def request_to_ai(text: str) -> str:
    prompt_prefix = "Понятен ли тебе мой промпт(не твой, а мой)? Дай ему оценку(моему промпту). Что мне надо в нём " \
                    "исправить(укажи так, чтобы было понятно тебе), чтобы тебе было понятно, что я хочу(не ты хочешь, " \
                    "а я), может надо что-то уточнить(для темы промпта)? Дай на это ответ по пунктам.\n//"
    full_prompt = prompt_prefix + text
    # send prompt to OpenAI API
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=full_prompt,
        max_tokens=1024,
        temperature=0.5
    )
    output_text = response.choices[0].text

    return output_text


@bot.listen()
async def on_ready():
    print(f"Logged in {bot.user.display_name} ({bot.user.id})!")


@bot.listen()
async def on_message(message: Message):
    if isinstance(message.channel, DMChannel) and not message.author.bot:
        await message.add_reaction("👀")
        text = await request_to_ai(message.content)
        view = RatingFromUser()
        await message.channel.send(content=text, view=view)

    if not message.content.startswith("@Clyde"):
        return

    await message.add_reaction(choice(["👍", "🤝", "👎"]))


@bot.slash_command(name="оцени")
async def estimate_command(
        inter: ApplicationCommandInteraction, *,
        text = commands.Param(name="запрос", description="Текст запроса для оценки")
    ):
    """Оценю качество запроса и дам рекомендации"""
    await inter.response.defer(ephemeral=True)
    text = await request_to_ai(text)
    view = RatingFromUser()
    await inter.edit_original_response(content=text, view=view)
    view.message = inter.original_message()


bot.run(environ.get("DISCORD_TOKEN"))
