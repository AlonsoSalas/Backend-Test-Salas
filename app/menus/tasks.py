
from __future__ import absolute_import, unicode_literals
import os
from celery import shared_task
from slack import WebClient
from slack.errors import SlackApiError
from time import time
import asyncio

slack_token = os.environ.get('SLACK_TOKEN')
slackClient = WebClient(slack_token)


@shared_task
def sendMenuToSlack():
    # print('holaaa')
    asyncio.run(sendMessage())


async def sendMessage():
    # print('llegue aqui ')
    users = await getUsers()
    channels = await getChannels(users)

    await asyncio.gather(slackClient.chat_postMessage(channel=channel,
                                                      text="que paso prueba") for channel in channels if channel)


async def getChannels(users):
    channels = []
    for user in users:
        conversation = await getConversation(user)
        channels.append(conversation['channel']['id'])

    return channels


async def getConversation(user):
    try:
        conversation = await slackClient.conversations_open(
            users=[user])
        return conversation
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")
        pass


async def getUsers():
    try:
        response = await slackClient.users_list()
        users = response["members"]
        print('users')
        print(users)
        userlist = list(user['id']
                        for user in users if not user['is_bot'])
        print(userlist)
        return userlist
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")
        return []
