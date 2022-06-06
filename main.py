import discord
from discord.ext import commands
import youtube_dl
import logging
import os
from dotenv import load_dotenv
load_dotenv()
# print(os.getenv('WEB_HOOK_KEY'))
key = os.getenv('WEB_HOOK_KEY')
# cogs = [music]
bot = commands.Bot(command_prefix='?')
songQueue = []
YDL_OPTIONS = {"format":"bestaudio"}
FFMPEG_OPTIONS = {"before_options":"-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options":"-vn"}
playFlag = False
commandDic = {
    'play': 'Paste youtube url after the play command',
    'stop': 'Stop playing',
    'skip': 'Skip current song',
    'fuck': 'Kick bot out',
    'pause': 'Pause it',
    'list': 'List the song queue'
}


@bot.command()
async def foo(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("You're not in a voice channel!!")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        msg = ''
        index = 1
        for key, value in commandDic.items():

            msg = msg + str(index) +'. '+ key+' : '+value + '\n'
            index = index + 1
        await voice_channel.connect()
        await ctx.send(msg)
    else:
        await ctx.voice_client.move_to(voice_channel)
    
@bot.command()
async def fuck(ctx):
    await ctx.voice_client.disconnect()

#stop playing music
@bot.command()
async def stop(ctx):
    ctx.voice_client.stop()

@bot.command()
async def play(ctx, url=''):
    if url:
        songQueue.append(url)
    # ctx.voice_client.stop()
    
    logging.info(FFMPEG_OPTIONS)
    
    # vc = ctx.voice_client
    print(songQueue)
    if not ctx.voice_client.is_playing():
        for song in songQueue:
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(song, download=False)
                logging.info(info["formats"][0])
                url2 = info["formats"][0]["url"]
                logging.warning('The url is: '+ url2)
                source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                ctx.voice_client.play(source)
        
                
@bot.command()
async def pause(ctx):
    await ctx.voice_client.pause()
    await ctx.send("Paused")

@bot.command()
async def resume(ctx):
    await ctx.voice_client.resume()
    await ctx.send("Resume")

@bot.command()
async def clear():
    songQueue.clear()
    print(songQueue)

@bot.command(name='list')
async def list(ctx):
    if len(songQueue):
        await ctx.send(songQueue)
    else:
        await ctx.send('Oh yeah~~ come fuel me with your giant URL!!!')

@bot.command()
async def skip(ctx):
    ctx.voice_client.stop()
    songQueue.pop(0)
    await play(ctx)
    


bot.run(key)

