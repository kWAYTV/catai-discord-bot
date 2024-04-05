import discord
from loguru import logger
from src.helper.config import Config
from src.database.schema.sessions import SessionSchema
from src.database.controller.sessions import SessionsController
from src.controller.ai.prompt_controller import PromptController
from src.controller.discord.schema.embed_schema import EmbedSchema
from src.controller.discord.embed_controller import EmbedController

class PromptModal(discord.ui.Modal, title='Send command to host'):
    def __init__(self):
        self.config = Config()
        self.sessions = SessionsController()
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
            async with self.prompt_controller as controller:
                response = await controller.send_prompt(self.user_prompt.value)

        embed_schema = EmbedSchema(
            title="AI Response",
            description="Answers should be double-checked for accuracy.",
            color=0xb34760,
        )

        # Check the response and edit the message accordingly.
        if response is None:
            embed_schema.fields = [
                {
                    'name': 'Error',
                    'value': 'An error occurred while processing the prompt. Please try again.',
                    'inline': True,
                }
            ]
            return await message.edit(embed=embed)

        embed_schema.fields = [
            {
                'name': 'Prompt',
                'value': self.user_prompt.value,
                'inline': True,
            },
            {
                'name': 'Response',
                'value': response,
                'inline': False,
            }
        ]

        session_schema = SessionSchema(owner_id=interaction.user.id, discord_channel_id=interaction.channel.id)
        await self.sessions.update_session(session_schema)

        embed = await EmbedController().build_embed(embed_schema)
        await message.edit(embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        logger.error(f'An error occurred with a prompt modal: {error}')
        await interaction.response.send_message(f'Oops! Something went wrong: {error}', ephemeral=True)
