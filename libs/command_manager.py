import functools

import libs.config as config
from libs.embed  import officialEmbed
from discord.ext import commands

"""
Any and all checks common to more than one command should be performed here
"""

def custom_check(allowed_channels=[]):

    """Decorator for any checks.

    Wrap around a bot command to check appropriate permission and channel context of the executed command from
    the Context object provided by the bot's event listener method, and errors out if checks do not pass.

    Example Usage:
        @commands.command...
        @custom_check(channel=['channel-name1', channel-name2'])
        def echo...

    Args:
        None yet

    Returns:
        Original method call that the method wraps around, and continues executing the command/method.
        If any checks fail, then will stop execution of the method and returns False after raising an exception.
    """

    def guild_check(cmd):

        @functools.wraps(cmd)
        async def wrapper(*args, **kwargs):
            ctx = args[1]
            if type(ctx) is not commands.Context:
                print("ERROR: Missing ctx variable in @check() call in", cmd.__name__, " command!")
                raise commands.MissingRequiredArgument(ctx)

            if len(allowed_channels) > 0:
                if not ctx.channel.name in allowed_channels + ['glug-bot-test']:
                    print(f"Command used in {ctx.channel.name} channel while allowed channels were {str(allowed_channels)}")
                    return False


            return await cmd(*args, **kwargs)

        return wrapper

    return guild_check

"""
Function to get Member object from user_id

Args:
    ctx: The context passed to the command function
    role_id: The mentioned role_id

Returns:
    role: Role if found otherwise None
"""

def get_member(ctx, user_id):
    try:
        if '<@!' in user_id:
            user = ctx.author.guild.get_member(int(user_id[3:-1]))
        elif '<@' in user_id:
            user = ctx.author.guild.get_member(int(user_id[2:-1]))
        else:
            user = ctx.author.guild.get_member(int(user_id))
    except ValueError:
        user = None
    
    return user

"""
Function to get Role object from role_id

Args:
    ctx: The context passed to the command function
    role_id: The mentioned role_id

Returns:
    role: Role if found otherwise None
"""

def get_role(ctx, role_id):
    try:
        if '<@&' in role_id:
            role = ctx.author.guild.get_role(int(role_id[3:-1]))
        elif '<@' in role_id:
            role = ctx.author.guild.get_role(int(role_id[2:-1]))
        else:
            role = ctx.author.guild.get_role(int(role_id))
    except ValueError:
        role = None
    
    return role


"""
Function to send contribution embed as reply

Args:
    ctx: context variable which is passed to a command function

Returns:
    None
"""

async def contribute(ctx):
    embed = officialEmbed("Contribute", "Contribute to this project, help create more cool features", url=config.get_config("info")["url"])
    embed.set_thumbnail(url=config.get_string("logos")["github"])
    await ctx.send(embed=embed)
