import discord
from discord.ext import commands
import youtube_dl
import logging


# cogs = [music]
bot = commands.Bot(command_prefix='?')

@bot.command()
async def foo(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("You're not in a voice channel!!")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
    
@bot.command()
async def disconnect(ctx):
    await ctx.voice_client.disconnect()


@bot.command()
async def play(ctx, url):
    ctx.voice_client.stop()
    FFMPEG_OPTIONS = {"before_options":"-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options":"-vn"}
    logging.info(FFMPEG_OPTIONS)
    YDL_OPTIONS = {"format":"bestaudio"}
    vc = ctx.voice_client

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        logging.info(info["formats"][0])
        url2 = info["formats"][0]["url"]
        logging.warning('The url is: '+ url2)
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        vc.play(source)

@bot.command()
async def pause(ctx):
    await ctx.voice_client.pause()
    await ctx.send("Paused")

@bot.command()
async def resume(ctx):
    await ctx.voice_client.resume()
    await ctx.send("Resume")


bot.run("OTM5MDYzNzU5NDQyNDM2MTM2.YfzZRw.48CKnHG3-JL3nlqWmnFf3twxpIo")

