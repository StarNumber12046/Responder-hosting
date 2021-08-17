import discord, io, functools, random, requests, os
from discord.ext import commands  
from PIL import Image, ImageFont, ImageDraw  
from urllib.request import urlopen

class AmongUs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_user_image(self, username):
        impostor = random.choice(["true", "false"])
        color = random.choice(["black", "blue", "brown", "cyan", "darkgreen", "lime", "orange", "pink", "purple", "red"], "white", "yellow")
        return(f"https://vacefron.nl/api/ejected?name={username}&impostor={impostor}&crewmate={color}")
        
        
        

    
    def has_transparency(self, img):
        if img.mode == "P":
            transparent = img.info.get("transparency", -1)
            for _, index in img.getcolors():
                if index == transparent:
                    return True

        elif img.mode == "RGBA":
            extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

        return False
    
    def eject_sync(self, username, image):
        
        impostor = random.choice(["true", "false"])
        color = random.choice(["black", "blue", "brown", "cyan", "darkgreen",
                               "lime", "orange", "pink", "purple", "red", "white", "yellow"])
        imgbytes = requests.get(f"https://vacefron.nl/api/ejected?name={username}&impostor={impostor}&crewmate={color}")
        base = Image.open(io.BytesIO(imgbytes.content)).convert("RGBA")


        font = ImageFont.truetype("assets/amongus.ttf", 35)

        
        img = Image.open(io.BytesIO(image)).resize((120, 120)).convert("RGBA")
        mask = Image.open(
            "assets/circle-mask.jpg").resize((25, 25)).convert("L")
        
        transparency = self.has_transparency(img)



        if transparency:
            base.paste(img, (2145, 650), img)

        else:
            base.paste(img, (2145, 650), img)
        
        b = io.BytesIO()
        base.save(b, "png")
        b.seek(0)
        return b



    def face_sync(self, image):

        imgbytes = "assets/sus/" + random.choice(os.listdir("assets/sus"))
        base = Image.open(imgbytes).convert("RGBA")

        font = ImageFont.truetype("assets/amongus.ttf", 35)

        img = Image.open(io.BytesIO(image)).resize((250, 250)).convert("RGBA")
        mask = Image.open(
            "assets/circle-mask.jpg").resize((25, 25)).convert("L")

        transparency = self.has_transparency(img)


        base.paste(img, (200, 200), img)

        b = io.BytesIO()
        base.save(b, "png")
        b.seek(0)
        return b
    
    async def ejector(self, username, image):
    
        function = functools.partial(self.eject_sync, username, image)
        img = await self.bot.loop.run_in_executor(None, function)
        return img

    async def facer(self, image):

        function = functools.partial(self.face_sync, image)
        img = await self.bot.loop.run_in_executor(None, function)
        return img
    
    @commands.command()
    async def eject(self, ctx, user:discord.User):
        async with ctx.typing():
            
            member = user or ctx.author
            bytes = await ctx.author.avatar_url_as(format="png").read()

            
            bytes = await self.ejector(str(ctx.author)[:-5], bytes)
            file = discord.File(fp = bytes, filename = "eject.png")
        await ctx.send(file=file)
    @commands.command()
    async def susface(self, ctx, user:discord.User):

        member = user or ctx.author
        bytes = await ctx.author.avatar_url_as(format="png").read()

        bytes = await self.facer(bytes)
        file = discord.File(fp=bytes, filename="face.png")
        await ctx.send(file=file)

def setup(bot):
    bot.add_cog(AmongUs(bot))
