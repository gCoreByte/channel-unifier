import json
from urllib.parse import urlencode
import aiohttp

from integrations.campuswire.campuswire_api import *
from integrations.campuswire.campuswire_models import *
from utils.loop_handler import LoopHandler
from dacite import from_dict


def name_helper(first_name, last_name):
    return " ".join([first_name, last_name])


class Campuswire:
    """Async Campuswire wrapper"""

    def __init__(self, loop: LoopHandler, email: str, password: str) -> None:
        self.loop = loop
        self.email = email
        self.password = password
        self.session = aiohttp.ClientSession()
        self.token = None

    async def authorize(self):
        login_obj = {"email": self.email, "password": self.password}
        async with self.session.post(LOGIN_ENDPOINT, json=login_obj) as res:
            if res.status != 200:
                # TODO: create separate error classes
                raise ValueError('Invalid login details')
            login_obj: LoginResponseSmall = from_dict(LoginResponseSmall, await res.json())
            self.token = login_obj.token

    async def connect_to_websocket(self):
        encoded_url = WS_ENDPOINT + "?" + urlencode({'access_token': self.token, 'v': 14})
        async with self.session.ws_connect(encoded_url) as ws:
            async for received_event in ws:
                if received_event.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                    break
                await self.websocket_event_helper(received_event.json(), ws)

    async def websocket_event_helper(self, event, ws):
      if event['event'] == EventType.Message.value:
          messageEvent = from_dict(MessageEvent, event['data'])
          message = messageEvent.message
          await self.loop.send_to_all(
              message.body, "Campuswire", name_helper(
                  message.author.firstName, message.author.lastName
              ), message.author.photo
          )
          return
      elif event['event'] == EventType.Hello.value:
        helloEvent = from_dict(Hello, event)
        await ws.send_json({'event':'world', 'replyTo':event.id})
        return
      elif event['event'] == EventType.WallPostCreated.value:
        if event['data'].has_key('anonymous'):
            await self.loop.send_to_all(
            event['data']['body'], "Campuswire", "Anonymous"
            )
        else:
            author = from_dict(Author, event['data']['author'])
            await self.loop.send_to_all(
            event['data']['body'], "Campuswire", name_helper(author.firstName, author.lastName), author.photo
            )


    async def run(self):
        await self.authorize()
        while True:
          await self.connect_to_websocket()
