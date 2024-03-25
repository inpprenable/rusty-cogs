from .chacall import Chacall


async def setup(bot):
    await bot.add_cog(Chacall(bot))
