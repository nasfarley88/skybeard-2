# from multiprocessing import Process
import logging

from skybeard.beards import BeardChatHandler
from skybeard.decorators import onerror, debugonly

from . import server
from . import database


logger = logging.getLogger(__name__)


class APIBeard(BeardChatHandler):

    __userhelp__ = "A simple api beard that runs a flask server"
    __commands__ = [
        ('restartserver', 'restart_server', 'Restarts flask server.'),
        ('whoami', 'who_am_i', 'Returns the chat id for current chat.'),
        ('allkeys', 'all_keys', 'Gets all the keys if in debug mode.'),
        ('getkey', 'get_key', 'TODO'),
    ]

    async def who_am_i(self, msg):
        await self.sender.sendMessage("Current chat_id: "+str(self.chat_id))

    sanic_proc = server.start()

    @classmethod
    def _restart_server(cls):
        server.stop()
        server.start()

    @onerror
    async def restart_server(self, msg):
        await self.logger.debug("Server: "+str(APIBeard.sanic_proc))
        return self._restart_server()

    @debugonly
    async def all_keys(self, msg):
        return await self.sender.sendMessage("All keys are:\n{}".format(
            "\n".join((
                "{}:{}".format(
                    x["chat_id"], x["key"]) for x in database.get_all_keys()))))

    async def get_key(self, msg):
        entry = database.get_key(self.chat_id)
        return await self.sender.sendMessage("Your key: {}".format(entry["key"]))
