
import discord

from asgiref.sync import sync_to_async
from discord import app_commands

from trips.services.trip_service import create_trip


trip_group = app_commands.Group(
    name="trip",
    description="Manage trips",
)


@trip_group.command(name="create")
async def trip_create(
    interaction: discord.Interaction,
    name: str,
):
    trip = await sync_to_async(create_trip)(
        name,
        interaction.user.id,
    )

    await interaction.response.send_message(
        f"Utworzono podróż: {trip.name}"
    )
