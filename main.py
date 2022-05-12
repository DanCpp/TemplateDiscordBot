import discord
from discord.ext import commands
import json
import requests
import os, random as r
import codecs
import math
import youtube_dl
import asyncio

settings = {
    'token': '',
    'bot': 'Pichupido',
    'id':,
    'prefix': '.'
}
intents = discord.Intents.all()
discord.member = True
bot = commands.Bot(command_prefix = settings['prefix'], intents = intents)

@bot.command(help="Prints details of Server")
async def where_am_i(ctx):
    owner = str(ctx.guild.owner)
    region = str(ctx.guild.region)
    guild_id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    desc = ctx.guild.description

    embed = discord.Embed(
        title=ctx.guild.name + " Server Information",
        description=desc,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=guild_id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)
    await ctx.send(embed=embed)
    members = []
    async for member in ctx.guild.fetch_members(limit=20):
        await ctx.send('Name : {}\t Status : {}\n Joined at {}'.format(member.display_name, str(member.status),
                                                                       str(member.joined_at)))

@bot.command() # Не передаём аргумент pass_context, так как он был нужен в старых версиях.
async def hello(ctx): # Создаём функцию и передаём аргумент ctx.
    author = ctx.message.author # Объявляем переменную author и записываем туда информацию об авторе.
    await ctx.send(f'Привет, {author.mention}!') # Выводим сообщение с упоминанием автора, обращаясь к переменной author.

@bot.command()
async def stix(ctx):
    files = os.listdir(path="stixi")
    random_stix = r.randint(1, len(files))
    file = codecs.open(f"stixi/{random_stix}.txt", encoding="utf-8")
    stih = file.readlines()
    stih = ''.join(stih)
    await ctx.send(stih)

@bot.command()
async def cat(ctx):
    response = requests.get('https://some-random-api.ml/img/cat')  # Get-запрос
    json_data = json.loads(response.text)  # Извлекаем JSON

    embed = discord.Embed(color=0xff9900, title='Random Cat')  # Создание Embed'a
    embed.set_image(url=json_data['link'])  # Устанавливаем картинку Embed'a
    await ctx.send(embed=embed)  # Отправляем Embed

@bot.command()
async def fox(ctx):
    response = requests.get('https://some-random-api.ml/img/fox') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff9900, title = 'Random Fox') # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed

@bot.event
async def on_member_join(member):
    print(f'{member.mention} has joined the server.')
    channel = None
    for i in member.guild.text_channels:
        if str(i) == "general":
            channel = i
    join = discord.Embed(description=f"{member.mention} Ку, порося", color=discord.Colour.random())
    join.set_image(url="https://www.volyn24.com/img/modules/news/5/9e/b9255584e2791c1ddfd4ae1b938699e5/gallery-photo.jpg")
    await channel.send(embed=join)

@bot.command()
async def quadraticequation(ctx):
    equa = ctx.message.content[19:].split(' ')
    a = int(equa[0][:len(equa[0]) - 3])
    b = int(equa[1] + equa[2][:len(equa[2]) - 1])
    c = int(equa[3] + equa[4])
    D = (b**2) - 4 * a * c
    if D < 0:
        await ctx.send("Нет корней")
        return
    if D == 0:
        x1 = (-b)/(2*a)
        await ctx.send(f"Единственный корень: {x1}")
        return
    x1 = (-b - math.sqrt(D)) / (2 * a)
    x2 = (-b + math.sqrt(D)) / (2 * a)
    await ctx.send(f"Два корня: {x1}; {x2}; D = {D}")



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    try:
        pass
    finally:
        await bot.process_commands(message)

youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

curr_file = ''

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        global curr_file
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        curr_file = filename
        return filename

@bot.command()
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command()
async def from_begin(ctx):
    global curr_file
    try:
        voice_client = ctx.message.guild.voice_client
        voice_client.stop()
        voice_client.play(discord.FFmpegPCMAudio(executable='voice/ffmpeg.exe', source=curr_file))
        await ctx.send('**again playing:** {}'.format(curr_file))
    except:
        await ctx.send("something went wrong")

@bot.command(help='To play song')
async def play(ctx, url):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="voice/ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")


@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


bot.run(settings['token']) # Обращаемся к словарю settings с ключом token, для получения токена


