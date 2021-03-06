from os import environ
from discord.ext import commands
from discord import DMChannel
import yaml
import difflib
import re


class Kevin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.command_list = self._get_command_list()
        self.aliases = {'ex': 'example',
                        'do': 'doc',
                        'tu': 'tutorial',
                        'ma': 'macro',
                        'to': 'tool'}

    @staticmethod
    def _get_command_list():
        with open('command_list.yaml') as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    def _get_options(self, parent_command):
        option_list = []
        for key in self.command_list.get(parent_command):
            option_list.append(key)
        return option_list

    def _get_response(self, command, option):
        response = self.command_list.get(command).get(option)
        if not response:
            best_match = difflib.get_close_matches(option, self.command_list.get(command))
            print(f'best_match: {best_match}')
            if not best_match:
                return f'Could not anything like option: {option}'
            else:
                return f'<{self.command_list.get(command).get(best_match[0])}>'
        else:
            return f'<{response}>'

    def get_command(self, command):
        if len(command) == 2:
            return self.aliases.get(command)
        else:
            return command

    def get_related_links(self, node, option):
        if isinstance(node, list):
            for item in node:
                for value in self.get_related_links(item, option):
                    yield value
        elif isinstance(node, dict):
            if option in node:
                yield node.get(option)
            for value in node.values():
                for val in self.get_related_links(value, option):
                    yield val

    async def _help_option_wrapper(self, ctx):
        msg = ctx.message.content
        option = msg[len(ctx.prefix) + len(ctx.invoked_with) + 1:]

        if option == '':
            await ctx.send(f"```{ctx.invoked_with} options:\n" +
                           "\n".join(self._get_options(self.get_command(ctx.invoked_with))) + "```")
        else:
            await ctx.send(self._get_response(self.get_command(ctx.invoked_with), option))

    async def _dm_user_wrapper(self, ctx):
        sep = '<'
        message = ctx.message.content[len(ctx.prefix) + len(ctx.invoked_with) + 1:]
        option = message.split(sep, 1)[0]
        print(f'option: {option}')
        if ctx.message.mentions:
            user = ctx.guild.get_member(ctx.message.mentions[0].id)
        else:
            user = ctx.message.author
        if option == '':

            await DMChannel.send(user, f"```{ctx.invoked_with} options:\n" +
                           "\n".join(self._get_options(self.get_command(ctx.invoked_with))) + "```")
        else:
            await DMChannel.send(user, self._get_response(self.get_command(ctx.invoked_with), option))


    # @commands.command(help='!all option\n Will fetch all occurrences of option from all commands.  ')
    # @commands.has_permissions(embed_links=True)
    # async def all(self, ctx):
    #     msg = ctx.message.content
    #     option = msg[len(ctx.prefix) + len(ctx.invoked_with) + 1:]
    #     user = ctx.message.author
    #     response = (list(self.get_related_links(self.command_list, option)))
    #     escaped_response = ["<" + resp + ">" for resp in response]
    #     await DMChannel.send(user, f"\n\n".join(escaped_response))

    @commands.command(aliases=['ex'], help='!example option\nWithout an option will list options')
    @commands.has_permissions(embed_links=True)
    async def example(self, ctx):
        await self._dm_user_wrapper(ctx)

    @commands.command(aliases=['do'], help='!doc option\nWithout an option will list options')
    @commands.has_permissions(embed_links=True)
    async def doc(self, ctx):
        await self._dm_user_wrapper(ctx)

    @commands.command(aliases=['tu'], help='!tutorial option\nWithout an option will list options')
    @commands.has_permissions(embed_links=True)
    async def tutorial(self, ctx):
        await self._dm_user_wrapper(ctx)

    @commands.command(aliases=['ma'], help='!macro option\nWithout an option will list options')
    @commands.has_permissions(embed_links=True)
    async def macro(self, ctx):
        await self._dm_user_wrapper(ctx)

    @commands.command(aliases=['to'], help='!tool option\nWithout an option will list options')
    @commands.has_permissions(embed_links=True)
    async def tool(self, ctx):
        await self._dm_user_wrapper(ctx)
