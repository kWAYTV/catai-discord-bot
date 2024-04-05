import discord
from loguru import logger
from src.helper.config import Config
from src.controller.ai.prompt_controller import PromptController

class PromptModal(discord.ui.Modal, title='Send command to host'):
    def __init__(self):
        self.config = Config()
        self.prompt_controller = PromptController.get_instance()
        super().__init__()

    user_prompt = discord.ui.TextInput(label='Prompt', style=discord.TextStyle.long, placeholder='Enter the prompt you want to give to the model.')

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        # Send the initial response message.
        message = await interaction.followup.send('Please wait for an answer from the model...', ephemeral=True)

        # Typing indicator context manager.
        async with interaction.channel.typing():
            # Process the prompt.
            response = await self.prompt_controller.send_prompt(interaction.user.id, self.user_prompt.value)

        # Check the response and edit the message accordingly.
        if response is None:
            await message.edit(content='An error occurred while trying to get a response from the model.')
        else:
            await message.edit(content=response)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        logger.error(f'An error occurred with PromptModal: {error}')
        await interaction.response.send_message(f'Oops! Something went wrong: {error}', ephemeral=True)
