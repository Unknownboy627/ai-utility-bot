import discord
from discord.ext import commands
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Utility AI | /help | Tech support"
        )
    )

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if channel:
        embed = discord.Embed(
            title="👋 Welcome!",
            description=f"Welcome {member.mention} to **{member.guild.name}**!",
            color=0x57F287
        )
        await channel.send(embed=embed)

@bot.command()
async def ping(ctx):
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latency: `{round(bot.latency * 1000)}ms`",
        color=0x5865F2
    )
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    g = ctx.guild
    embed = discord.Embed(
        title="📊 Server Info",
        color=0x3498DB
    )
    embed.add_field(name="Name", value=g.name, inline=True)
    embed.add_field(name="Members", value=g.member_count, inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(
        title="👤 User Info",
        color=0x95A5A6
    )
    embed.add_field(name="User", value=member.name)
    embed.add_field(name="ID", value=member.id)
    await ctx.send(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
