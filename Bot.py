import datetime, requests, discord, roapipy, asyncio, json, os
from discord import app_commands
from discord.ext import commands, tasks
from discord.app_commands import Choice

client = commands.Bot(command_prefix = '!', intents=discord.Intents.all())
client.remove_command('help')
os.chdir("D:\Roblox Businesses\G-Corp\Businesses\Grab a Café\Bot")
tree = client.tree
roclient = roapipy.client()

pointsdir = "points.json"
loadir = "loa.json"
warnsdir = "warns.json"

@tasks.loop(hours=1)
async def loacheck():
    loadict = {}
    loaover = []
    realmembers = []
    with open(loadir, "r+") as f:
        data = json.load(f)
        for el in data:
            loadict[el] = data[el]
    for el in loadict:
        if datetime.datetime.strptime(loadict[el], "%m/%d/%y") < datetime.datetime.now():
            loaover.append(el)
    for el in loaover:
        try:
            client.get_user(el)
            realmembers.append(el)
        except:
            pass
    with open(loadir, "r+") as f:
        data = json.load(f)
        for el in loaover:
            del data[el]
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
    gacserver = client.get_guild(1034238022054592595)
    loarole = gacserver.get_role(1034253861378084935)
    logschannel = client.get_channel(1034247101414125619)
    embed = discord.Embed(
        title="Leave of Absence",
        colour=0x3c8cf5,
        description=""
    )
    for el in realmembers:
        person = gacserver.get_member(int(el))
        embed.description = f"**{person.nick}**\nIs no longer on a Leave of Absence"
        userpfp = roclient.user.info(person.nick)["avatar"]
        embed.set_thumbnail(url=userpfp)
        await logschannel.send(embed=embed)
        try:
            await person.remove_roles(loarole)
        except:
            pass

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Baristas"))
    print(f'Grab a Café Assistant now online with {round(client.latency * 1000)}ms ping.')
    await loacheck.start()

@client.event
async def on_member_join(member):
    welcomechannel = client.get_channel(1034270072715362354)
    await welcomechannel.send(embed=discord.Embed(title="New Member", colour=0xCCB8E1, description=f"Welcome {member.mention}!"))

def notapplied(interaction):
    with open(warnsdir, "r+") as f:
        data = json.load(f)
        return str(interaction.user.id) in data

@tree.command(name="apply", description="Apply to join Grab a Café")
@app_commands.check(notapplied)
async def apply(interaction : discord.Interaction):
    await interaction.response.send_message("Soon...™")

log = app_commands.Group(name="log", description="Logging")
tree.add_command(log)

@log.command(name="shift", description="Log your shift")
@app_commands.check(lambda interaction : 1034246149139341434 in [el.id for el in interaction.user.roles])
async def shift(interaction : discord.Interaction, starttime : str, startsc : str, endtime : str, endsc : str):
    nonint = False
    userpfp = roclient.user.info(who.nick)["avatar"]
    try:
        int(starttime)
    except:
        nonint = True
    if nonint == False:
        try:
            int(endtime)
        except:
            nonint = True
    if nonint == False:
        if len(starttime) == 4 or len(endtime) != 4:
            if int(starttime[3]) > 9 or int(endtime[3]) > 9 or int(starttime[2]) > 5 or int(endtime[2]) > 5 or int(starttime[1]) > 9 or int(endtime[1]) > 9 or int(starttime[0]) > 2 or int(endtime[0]) > 2:
                await interaction.response.send_message(embed=discord.Embed(title="Shift Error", colour=0xCCB8E1, description="Ensure that the time you entered is possible").set_thumbnail(url=userpfp))
            elif int(starttime[0]) == 2 and int(starttime[1]) > 4 or int(endtime[0]) == 2 and int(endtime[1]) > 4:
                await interaction.response.send_message(embed=discord.Embed(title="Shift Error", colour=0xCCB8E1, description="Ensure that the time you entered is possible").set_thumbnail(url=userpfp))
            else:
                if int(endtime) < int(starttime):
                    start = datetime.datetime.strptime(starttime, "%H%M")
                    end = datetime.datetime.strptime(endtime, "%H%M")
                    diff = (end - start) + datetime.timedelta(days=1)
                else:
                    start = datetime.datetime.strptime(starttime, "%H%M")
                    end = datetime.datetime.strptime(endtime, "%H%M")
                    diff = end - start
                diff = datetime.datetime.strptime(str(diff), "%H:%M:%S")
                shiftchannel = client.get_channel(1034254579363237949)
                await shiftchannel.send(embed=discord.Embed(title=f"{interaction.user.nick}", colour=0xCCB8E1, description=f"**Start/End**\n{starttime} - {endtime}\n\n**Time**\n{diff.hour} Hour(s) {diff.minute} Minute(s)\n\n**Evidence**\n{startsc}\n{endsc}").set_thumbnail(url=userpfp))
                await interaction.response.send_message(embed=discord.Embed(title="Shift", colour=0xCCB8E1, description="Your shift log has been sent for reviewal.").set_thumbnail(url=userpfp))
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Shift Error", colour=0xCCB8E1, description="Ensure you enter the start and end time in military form.\nE.g; 0900, 1200, 1900").set_thumbnail(url=userpfp))
    else:
        await interaction.response.send_message(embed=discord.Embed(title="Shift Error", colour=0xCCB8E1, description="When entering your start and end times, ensure they're written in military form.\nE.g; 0700, 1200, 1900, etc.\nAvoid the following: 19:00, 07:00 PM, 7PM, etc.").set_thumbnail(url=userpfp))

@shift.error
async def shifterror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message(embed=discord.Embed(title="Command Error", colour=0xCCB8E1, description="You do not have permission to run that command."))
    else:
        raise error

@log.command(name="loa", description="Log your leave of absence")
@app_commands.check(lambda interaction : 1034246149139341434 in [el.id for el in interaction.user.roles])
async def loa(interaction : discord.Interaction, until : str, reason : str):
    already = False
    userpfp = roclient.user.info(who.nick)["avatar"]
    with open(loadir, "r+") as f:
        data = json.load(f)
        if str(interaction.user.id) in data:
            already = True
    if already == False:
        if len(until) == 8:
            if until[2] == "/" and until[5] == "/":
                if int(until[0] + until[1]) > 12 or int(until[3] + until[4]) > 31 or int(until[6] + until[7]) not in [22, 23]:
                    await interaction.response.send_message(embed=discord.Embed(title="LOA Error", colour=0xCCB8E1, description="Ensure that the date you entered exists.").set_thumbnail(url=userpfp))
                elif datetime.datetime.strptime(until, "%m/%d/%y") < datetime.datetime.now():
                    await interaction.response.send_message(embed=discord.Embed(title="LOA Error", colour=0xCCB8E1, description="Ensure that the date you entered is not in the past.").set_thumbnail(url=userpfp))
                else:
                    loarole = interaction.guild.get_role(1034253861378084935)
                    logschannel = client.get_channel(1034247101414125619)
                    await interaction.user.add_roles(loarole)
                    await logschannel.send(embed=discord.Embed(title="Leave of Absence", colour=0xCCB8E1, description=f"**{interaction.user.nick}**\nUntil `{until}`").set_thumbnail(url=userpfp))
                    await interaction.response.send_message(embed=discord.Embed(title="LOA", colour=0xCCB8E1, description="Your LOA has been submitted.").set_thumbnail(url=userpfp))
                    with open(loadir, "r+") as f:
                        data = json.load(f)
                        data[interaction.user.id] = until
                        f.seek(0)
                        f.truncate()
                        json.dump(data, f, indent=4)
            else:
                await interaction.response.send_message(embed=discord.Embed(title="LOA Error", colour=0xCCB8E1, description="Ensure you're using the correct format when request LOA.\nMM/DD/YY").set_thumbnail(url=userpfp))
        else:
            await interaction.response.send_message(embed=discord.Embed(title="LOA Error", colour=0xCCB8E1, description="Ensure you're using the correct format when request LOA.\nMM/DD/YY").set_thumbnail(url=userpfp))
    else:
        await interaction.response.send_message(embed=discord.Embed(title="LOA Error", colour=0xCCB8E1, description="Seems like you've already submitted a LOA.").set_thumbnail(url=userpfp))

@loa.error
async def loaerror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message(embed=discord.Embed(title="Command Error", colour=0xCCB8E1, description="You do not have permission to run that command."))
    else:
        raise error

action = app_commands.Group(name="action", description="Log administrative actions", parent=log)

@action.command(name="hire", description="Log a hiring")
@app_commands.check(lambda interaction : 1034246167653011507 in [el.id for el in interaction.user.roles])
async def hire(interaction : discord.Interaction, who : discord.Member):
    logschannel = client.get_channel(1034247101414125619)
    employeerole = interaction.guild.get_role(1034246149139341434)
    juniorbaristarole = interaction.guild.get_role(1034245751825510450)
    userpfp = roclient.user.info(who.nick)["avatar"]
    await interaction.response.send_message(embed=discord.Embed(title="Done", colour=0xCCB8E1, description="This action has been logged").set_thumbnail(url=userpfp))
    await logschannel.send(embed=discord.Embed(title="Hired", colour=0x3cf55e, description=f"**{who.nick}** has been hired").set_thumbnail(url=userpfp))
    await who.add_roles(employeerole, juniorbaristarole)

@hire.error
async def hireerror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message(embed=discord.Embed(title="Command Error", colour=0xCCB8E1, description="You do not have permission to run that command."))
    else:
        raise error

@action.command(name="term", description="Log a termination")
@app_commands.check(lambda interaction : 1034246167653011507 in [el.id for el in interaction.user.roles])
async def term(interaction : discord.Interaction, who : discord.Member):
    logschannel = client.get_channel(1034247101414125619)
    roleslist = [1034253861378084935, 1034246149139341434, 1034245751825510450, 1034245738659594260, 1034245691343650877, 1034246167653011507, 1034245672293113866, 1034245653611679777]
    userpfp = roclient.user.info(who.nick)["avatar"]
    await interaction.response.send_message(embed=discord.Embed(title="Done", colour=0xCCB8E1, description="This action has been logged").set_thumbnail(url=userpfp))
    await logschannel.send(embed=discord.Embed(title="Terminated", colour=0xf53c3c, description=f"**{who.nick}** has been terminated").set_thumbnail(url=userpfp))
    for el in roleslist:
        try:
            role = interaction.guild.get_role(el)
            await who.remove_roles(role)
        except:
            pass

@term.error
async def termerror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message(embed=discord.Embed(title="Command Error", colour=0xCCB8E1, description="You do not have permission to run that command."))
    else:
        raise error

@action.command(name="rank", description="Log a ranking")
@app_commands.check(lambda interaction : 1034246167653011507 in [el.id for el in interaction.user.roles])
@app_commands.choices(rank=[Choice(name="Shift Supervisor", value="1034245653611679777"), Choice(name="Head Barista", value="1034245672293113866"), Choice(name="Senior Barista", value="1034245691343650877"), Choice(name="Barista", value="1034245738659594260"), Choice(name="Junior Barista", value="1034245751825510450")])
async def rank(interaction : discord.Interaction, who : discord.Member, rank : Choice[str]):
    userpfp = roclient.user.info(who.nick)["avatar"]
    if who.id != interaction.user.id:
        rank = interaction.guild.get_role(int(rank.value))
        logschannel = client.get_channel(1034247101414125619)
        hrrole = interaction.guild.get_role(1034246167653011507)
        roleslist = [1034245751825510450, 1034245738659594260, 1034245691343650877, 1034245672293113866, 1034245653611679777]
        userroleid = None
        for el in interaction.user.roles:
            if el.id in roleslist:
                userroleid = el.id
        if interaction.user.id == 301014178703998987 or roleslist.index(rank.id) < roleslist.index(userroleid):
            hrlist = [1034245672293113866, 1034245653611679777]
            oldroleid = None
            for el in who.roles:
                if el.id in roleslist:
                    oldroleid = el.id
            oldrole = interaction.guild.get_role(oldroleid)
            await who.remove_roles(oldrole)
            await who.add_roles(rank)
            if roleslist.index(oldroleid) < roleslist.index(rank.id):
                if rank.id in hrlist and oldroleid not in hrlist:
                    await who.add_roles(hrrole)
                await logschannel.send(embed=discord.Embed(title="Promotion", colour=0x3cf55e, description=f"**{who.nick}** has been promoted from `{oldrole.name}` to `{rank.name}`").set_thumbnail(url=userpfp))
                await interaction.response.send_message(embed=discord.Embed(title="Done", colour=0xCCB8E1, description="This action has been logged").set_thumbnail(url=userpfp))
            elif roleslist.index(oldroleid) > roleslist.index(rank.id):
                if oldroleid in hrlist and rank.id not in hrlist:
                    await who.remove_roles(hrrole)
                await logschannel.send(embed=discord.Embed(title="Demotion", colour=0xf5953c, description=f"**{who.nick}** has been demoted from `{oldrole.name}` to `{rank.name}`").set_thumbnail(url=userpfp))
                await interaction.response.send_message(embed=discord.Embed(title="Done", colour=0xCCB8E1, description="This action has been logged").set_thumbnail(url=userpfp))
            else:
                await interaction.response.send_message(embed=discord.Embed(title="Rank Error", colour=0xCCB8E1, description="You can't set someone's rank to their current rank.").set_thumbnail(url=userpfp))
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Rank Error", colour=0xCCB8E1, description="You can't rank someone higher than yourself.").set_thumbnail(url=userpfp))
    else:
        await interaction.response.send_message(embed=discord.Embed(title="Rank Error", colour=0xCCB8E1, description="You can't set your own rank.").set_thumbnail(url=userpfp))

@rank.error
async def rankerror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message(embed=discord.Embed(title="Command Error", colour=0xCCB8E1, description="You do not have permission to run that command."))
    else:
        raise error

check = app_commands.Group(name="check", description="Checking")
tree.add_command(check)

@check.command(name="points", description="Check someone's points")
@app_commands.check(lambda interaction : 1034246167653011507 in [el.id for el in interaction.user.roles])
async def checkpoints(interaction : discord.Interaction, who : discord.Member):
    userpfp = roclient.user.info(who.nick)["avatar"]
    with open(pointsdir, "r+") as f:
        data = json.load(f)
        if str(who.id) in data:
            await interaction.response.send_message(embed=discord.Embed(title=f"{who.nick}'s Points", colour=0xCCB8E1, description=f"{who.mention} has `{data[str(who.id)]}` point(s)").set_thumbnail(url=userpfp))
        elif 1034246149139341434 in [el.id for el in who.roles]:
            data[who.id] = 0
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
            await interaction.response.send_message(embed=discord.Embed(title=f"{who.nick}'s Points", colour=0xCCB8E1, description=f"{who.mention} has `0` point(s)").set_thumbnail(url=userpfp))
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Points Error", colour=0xCCB8E1, description="We couldn't find that user\nAre they an employee for Grab a Café?").set_thumbnail(url=userpfp))

@checkpoints.error
async def checkpointserror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message(embed=discord.Embed(title="Command Error", colour=0xCCB8E1, description="You do not have permission to run that command."))
    else:
        raise error

@check.command(name="loa", description="Check someone's loa")
@app_commands.check(lambda interaction : 1034246167653011507 in [el.id for el in interaction.user.roles])
async def checkloa(interaction : discord.Interaction, who : discord.Member):
    userpfp = roclient.user.info(who.nick)["avatar"]
    with open(loadir, "r+") as f:
        data = json.load(f)
        if str(who.id) in data:
            await interaction.response.send_message(embed=discord.Embed(title=f"{who.nick}'s LOA", colour=0xCCB8E1, description=f"{who.mention} has a LOA Until {data[str(who.id)]}").set_thumbnail(url=userpfp))
        else:
            await interaction.response.send_message(embed=discord.Embed(title="LOA Error", colour=0xCCB8E1, description="We couldn't find that user/they don't have a LOA").set_thumbnail(url=userpfp))

@checkloa.error
async def checkloaerror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message(embed=discord.Embed(title="Command Error", colour=0xCCB8E1, description="You do not have permission to run that command."))
    else:
        raise error

@check.command(name="warns", description="Check someone's warnings")
@app_commands.check(lambda interaction : 1034246167653011507 in [el.id for el in interaction.user.roles])
async def checkwarns(interaction : discord.Interaction, who : discord.Member):
    userpfp = roclient.user.info(who.nick)["avatar"]
    with open(warnsdir, "r+") as f:
        data = json.load(f)
        if str(who.id) in data:
            embed = discord.Embed(
                title=f"{who.nick}'s Warnings",
                colour=0xCCB8E1,
                description=f"{len(data[str(who.id)])} total warning(s)```\n"
            )
            embed.set_thumbnail(url=userpfp)
            for el in data[str(who.id)]:
                embed.description = f"{embed.description}{el}\n"
            embed.description = f"{embed.description}```"
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Warnings Error", colour=0xCCB8E1, description="We couldn't find that user/they don't have any warnings").set_thumbnail(url=userpfp))

@checkwarns.error
async def checkwarnserror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message(embed=discord.Embed(title="Command Error", colour=0xCCB8E1, description="You do not have permission to run that command."))
    else:
        raise error

points = app_commands.Group(name="points", description="Points")
tree.add_command(points)

@points.command(name="self", description="Check your points")
@app_commands.check(lambda interaction : 1034246149139341434 in [el.id for el in interaction.user.roles])
async def self(interaction : discord.Interaction):
    userpfp = roclient.user.info(interaction.user.nick)["avatar"]
    with open(pointsdir, "r+") as f:
        data = json.load(f)
        if str(interaction.user.id) not in data:
            data[str(interaction.user.id)] = 0
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
        await interaction.response.send_message(embed=discord.Embed(title=f"{interaction.user.nick}'s Points", colour=0xCCB8E1, description=f"You have `{data[str(interaction.user.id)]}` point(s)").set_thumbnail(url=userpfp))

@self.error
async def selferror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message(embed=discord.Embed(title="Command Error", colour=0xCCB8E1, description="You do not have permission to run that command."))
    else:
        raise error

@points.command(name="add", description="Add to someone's points")
@app_commands.check(lambda interaction : 1034246167653011507 in [el.id for el in interaction.user.roles])
async def add(interaction : discord.Interaction, who : discord.Member, amount : int):
    error = False
    userpfp = roclient.user.info(who.nick)["avatar"]
    with open(pointsdir, "r+") as f:
        data = json.load(f)
        if str(who.id) not in data:
            if 1034246149139341434 in [el.id for el in interaction.user.roles]:
                data[str(who.id)] = amount
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4)
            else:
                error = True
        else:
            data[str(who.id)] = data[str(who.id)] + amount
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
    if error == False:
        await interaction.response.send_message(embed=discord.Embed(title=f"{who.nick}'s Points", colour=0xCCB8E1, description=f"{who.mention} now has `{data[str(who.id)]}` point(s)").set_thumbnail(url=userpfp))
    else:
        await interaction.response.send_message(embed=discord.Embed(title="Points Error", colour=0xCCB8E1, description="We couldn't find that user\nAre they an employee for Grab a Café").set_thumbnail(url=userpfp))

@add.error
async def adderror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message(embed=discord.Embed(title="Command Error", colour=0xCCB8E1, description="You do not have permission to run that command."))
    else:
        raise error

@points.command(name="remove", description="Remove from someone's points")
@app_commands.check(lambda interaction : 1034246167653011507 in [el.id for el in interaction.user.roles])
async def remove(interaction : discord.Interaction, who : discord.Member, amount : int):
    userpfp = roclient.user.info(who.nick)["avatar"]
    error, neg = False, False
    with open(pointsdir, "r+") as f:
        data = json.load(f)
        if str(who.id) not in data:
            if 1034246149139341434 in [el.id for el in interaction.user.roles]:
                data[str(who.id)] = 0
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4)
                neg = True
            else:
                error = True
        else:
            if (data[str(who.id)] - amount) < 0:
                error = True
            else:
                data[str(who.id)] = data[str(who.id)] - amount
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4)
    if error == False:
        if neg == False:
            await interaction.response.send_message(embed=discord.Embed(title=f"{who.nick}'s Points", colour=0xCCB8E1, description=f"{who.mention} now has `{data[str(who.id)]}` point(s)").set_thumbnail(url=userpfp))
        else:
            await interaction.response.send_message(embed=discord.Embed(title=f"Points Error", colour=0xCCB8E1, description="A user cannot have negative points").set_thumbnail(url=userpfp))
    else:
        await interaction.response.send_message(embed=discord.Embed(title="Points Error", colour=0xCCB8E1, description="We couldn't find that user\nAre they an employee for Grab a Café").set_thumbnail(url=userpfp))

@remove.error
async def removeerror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message(embed=discord.Embed(title="Command Error", colour=0xCCB8E1, description="You do not have permission to run that command."))
    else:
        raise error

@points.command(name="set", description="Set someone's points")
@app_commands.check(lambda interaction : 1034246167653011507 in [el.id for el in interaction.user.roles])
async def setpoints(interaction : discord.Interaction, who : discord.Member, amount : int):
    userpfp = roclient.user.info(who.nick)["avatar"]
    if amount > 0:
        error = False
        with open(pointsdir, "r+") as f:
            data = json.load(f)
            if str(who.id) in data:
                data[str(who.id)] = amount
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4)
            else:
                if 1034246149139341434 in [el.id for el in interaction.user.roles]:
                    data[str(who.id)] = amount
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f, indent=4)
                else:
                    error = True
        if error == False:
            await interaction.response.send_message(embed=discord.Embed(title=f"{who.nick}'s Points", colour=0xCCB8E1, description=f"{who.mention} now has `{data[str(who.id)]}` point(s)").set_thumbnail(url=userpfp))
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Points Error", colour=0xCCB8E1, description="We couldn't find that user\nAre they an employee for Grab a Café").set_thumbnail(url=userpfp))
    else:
        await interaction.response.send_message(embed=discord.Embed(title=f"Points Error", colour=0xCCB8E1, description="A user cannot have negative points").set_thumbnail(url=userpfp))

@setpoints.error
async def setpointserror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message(embed=discord.Embed(title="Command Error", colour=0xCCB8E1, description="You do not have permission to run that command."))
    else:
        raise error

infractions = app_commands.Group(name="infractions", description="Infractions")
tree.add_command(infractions)

@infractions.command(name="add", description="Warn a user")
@app_commands.check(lambda interaction : 1034246167653011507 in [el.id for el in interaction.user.roles])
async def infracsadd(interaction : discord.Interaction, who : discord.Member, reason : str):
    totalwarns = 0
    userpfp = roclient.user.info(who.nick)["avatar"]
    with open(warnsdir, "r+") as f:
        data = json.load(f)
        totalwarns = len(data[str(who.id)])+1
        if str(who.id) in data:
            if len(data[str(who.id)]) == 2:
                notifchannel = client.get_channel(1034276863935254588)
                await notifchannel.send(embed=discord.Embed(title="3 Warnings", colour=0xf5e63c, description=f"{who.mention} is now at 3 warnings.").set_thumbnail(url=userpfp))
            data[str(who.id)].append(reason)
            await interaction.response.send_message(embed=discord.Embed(title="Warning", colour=0xCCB8E1, description=f"{who.mention} has been warned for;```\n{reason}\n```").set_thumbnail(url=userpfp))
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
        elif 1034246149139341434 in [el.id for el in who.roles]:
            data[str(who.id)] = [
                data[str(who.id)].append(reason)
            ]
            await interaction.response.send_message(embed=discord.Embed(title="Warning", colour=0xCCB8E1, description=f"{who.mention} has been warned for;```\n{reason}\n```").set_thumbnail(url=userpfp))
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Warning Error", colour=0xCCB8E1, description="We couldn't find that user\nAre they an employee for Grab a Café").set_thumbnail(url=userpfp))
    logschannel = client.get_channel(1034247101414125619)
    await logschannel.send(embed=discord.Embed(title="Warning", colour=0xf5e63c, description=f"**{who.nick}** has been given a record warning.\nThey are now at `{totalwarns}` warning(s)").set_thumbnail(url=userpfp))

@infracsadd.error
async def infracsadderror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message(embed=discord.Embed(title="Command Error", colour=0xCCB8E1, description="You do not have permission to run that command."))
    else:
        raise error

@infractions.command(name="clear", description="Clears a users' warnings")
@app_commands.check(lambda interaction : 1034246167653011507 in [el.id for el in interaction.user.roles])
async def infracsclear(interaction : discord.Interaction, who : discord.Member, reason : str):
    anywarns, error = None, None
    with open(warnsdir, "r+") as f:
        data = json.load(f)
        if str(who.id) in data and len(data[str(who.id)]) > 0:
            anywarns = True
            del data[str(who.id)]
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
        else:
            error = True
    userpfp = roclient.user.info(who.nick)["avatar"]
    if error:
        await interaction.response.send_message(embed=discord.Embed(title="Warning Error", colour=0xCCB8E1, description="We couldn't find that user\nAre they an employee for Grab a Café").set_thumbnail(url=userpfp))
    elif anywarns:
        await interaction.response.send_message(embed=discord.Embed(title="Warning", colour=0xCCB8E1, description=f"{who.mention} has had their warnings cleared.").set_thumbnail(url=userpfp))
    else:
        await interaction.response.send_message(embed=discord.Embed(title="Warning", colour=0xCCB8E1, description=f"{who.mention} doesn't have any warnings to clear.").set_thumbnail(url=userpfp))

@infracsclear.error
async def infracsclearerror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message(embed=discord.Embed(title="Command Error", colour=0xCCB8E1, description="You do not have permission to run that command."))
    else:
        raise error

@infractions.command(name="self", description="Check your warnings")
@app_commands.check(lambda interaction : 1034246149139341434 in [el.id for el in interaction.user.roles])
async def infracsself(interaction : discord.Interaction, who : discord.Member, reason : str):
    anywarns = None
    with open(warnsdir, "r+") as f:
        data = json.load(f)
        if str(who.id) in data and len(data[str(who.id)]) > 0:
            anywarns = True
            allwarns = "```\n"
            for el in data[str(who.id)]:
                allwarns = f"{allwarns}{el}\n"
            allwarns = f"{allwarns}```"
    userpfp = roclient.user.info(interaction.user.nick)["avatar"]
    if anywarns:
        await interaction.response.send_message(embed=discord.Embed(title="Warnings", colour=0xCCB8E1, description=allwarns).set_thumbnail(url=userpfp))
    else:
        await interaction.response.send_message(embed=discord.Embed(title="Warnings", colour=0xCCB8E1, description="You don't have any warnings.").set_thumbnail(url=userpfp))

@infracsself.error
async def infracsselferror(interaction, error):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        await interaction.response.send_message(embed=discord.Embed(title="Command Error", colour=0xCCB8E1, description="You do not have permission to run that command."))
    else:
        raise error

@client.command()
@commands.check(lambda ctx : ctx.author.id == 301014178703998987)
async def connect(ctx):
    await tree.sync()

client.run('MTAzNDI1MDYwMTE2MjM0NjUwNg.Gz75yP.XeebGBMBvtdxQR4iiYmkEJ4jb5pCKykPkkfUL0')

#https://discord.com/api/oauth2/authorize?client_id=1034250601162346506&permissions=8&scope=bot

#General Hex (Light Purple) - 0xCCB8E1
#Hired/Promoted - 0x3cf55e
#Demoted - 0xf5953c
#Termination - 0xf53c3c
#Warning - 0xf5e63c
#LOA - 0x3c8cf5

"""
f.seek(0)
f.truncate()
json.dump(data, f, indent=4)
"""