class SessionSchema:
    def __init__(self, owner_id: int, discord_channel_id: int) -> None:
        self.owner_id = owner_id
        self.discord_channel_id = discord_channel_id

    def serialize(self) -> dict:
        return {
            'owner_id': self.owner_id,
            'discord_channel_id': self.discord_channel_id
        }

    @staticmethod
    def deserialize(data) -> 'SessionSchema':
        return SessionSchema(
            owner_id=data['owner_id'],
            discord_channel_id=data['discord_channel_id'],
            last_used=data['last_used']
        )