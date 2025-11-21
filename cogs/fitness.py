import discord
from discord.ext import commands
from discord import app_commands
import os
import json
from datetime import datetime

DATA_FOLDER = "data/"
os.makedirs(DATA_FOLDER, exist_ok=True)


def user_data_file(user_id):
    return os.path.join(DATA_FOLDER, f"{user_id}.json")


def load(user_id):
    try:
        with open(user_data_file(user_id), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"workouts": [], "mental": []}


def save(user_id, data):
    with open(user_data_file(user_id), "w") as f:
        json.dump(data, f, indent=4)


class Fitness(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="workout", description="Log a workout session")
    async def workout(
        self,
        interaction: discord.Interaction,
        workout_type: str = "Strength Training",
        duration_in_min: int = 30,
        notes: str = "",
    ):
        """Log a workout session."""
        user_id = str(interaction.user.id)
        data = load(user_id)

        workout_entry = {
            "type": workout_type,
            "duration_in_min": duration_in_min,
            "notes": notes,
            "timestamp": datetime.utcnow().isoformat(),
        }

        data["workouts"].append(workout_entry)
        save(user_id, data)

        await interaction.response.send_message(
            f"Workout logged: {workout_type} for {duration_in_min} minutes."
        )

    @app_commands.command(
        name="mental",
        description="Log a mental health activity, like a hobby or meditation",
    )
    async def mental(
        self,
        interaction: discord.Interaction,
        activity_type: str = "meditation",
        duration_in_min: int = 30,
        notes: str = "",
    ):
        """Log a mental health activity."""
        user_id = str(interaction.user.id)
        data = load(user_id)

        mental_entry = {
            "type": activity_type,
            "duration_in_min": duration_in_min,
            "notes": notes,
            "timestamp": datetime.utcnow().isoformat(),
        }

        data["mental"].append(mental_entry)
        save(user_id, data)

        await interaction.response.send_message(
            f"Mental health activity logged: {activity_type} for {duration_in_min} minutes."
        )

    @app_commands.command(
        name="summary",
        description="View your logged fitness and mental health activities",
    )
    async def summary(self, interaction: discord.Interaction):
        """View logged fitness and mental health activities."""
        user_id = str(interaction.user.id)
        data = load(user_id)

        workouts = data["workouts"]
        mental = data["mental"]

        embed = discord.Embed(
            title=f"{interaction.user.name}'s FitBunny Summary 🐰",
            color=discord.Color.pink(),
        )

        embed.add_field(
            name="🏋️ Workouts",
            value=str(len(workouts)),
        )
        embed.add_field(
            name="🧘 Mental Activities",
            value=str(len(mental)),
        )

        total_workout = sum(w["duration_in_min"] for w in workouts)
        total_mental = sum(m["duration_in_min"] for m in mental)

        embed.add_field(
            name="⏱ Total Workout Minutes",
            value=str(total_workout),
            inline=False,
        )
        embed.add_field(
            name="💭 Total Mental Minutes",
            value=str(total_mental),
            inline=False,
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Fitness(bot))
