import discord
from loguru import logger
from src.helper.config import Config

class PromptModal(discord.ui.Modal, title='Send command to host'):
    def __init__(self):
        super().__init__()
        self.config = Config()

    host_command = discord.ui.TextInput(label='Prompt', style=discord.TextStyle.long, placeholder='Enter the prompt you want to give to the model.')

    async def on_submit(self, interaction: discord.Interaction):
        raise NotImplementedError("PromptModal submit is not implemented yet.")

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        logger.error(f'An error occurred with PromptModal: {error}')
        await interaction.response.send_message(f'Oops! Something went wrong: {error}', ephemeral=True)