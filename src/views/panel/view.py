import discord

class PanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def not_implemented(self, interaction: discord.Interaction):
        return await interaction.response.send_message("Sorry! This option is **not** yet implemented.", ephemeral=True)

    @discord.ui.button(label='➕ Create Room', style=discord.ButtonStyle.green, custom_id='panel:create_menu')
    async def create_room_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        raise NotImplementedError("Create Room button is not implemented yet.")