
from __future__ import absolute_import, unicode_literals
import os
import asyncio
from celery import shared_task
from slack import WebClient
from slack.errors import SlackApiError
from time import time
from menus.models import Menu

slack_token = os.environ.get('SLACK_TOKEN')


@shared_task
def sendMenuToSlack():
    menu = Menu.objects.getTodayMenu()
    if menu:
        message = f'Hello Here is the link for todays Menu!.\n\nhttps://nora.cornershop.io/menu/{menu.id}'
    else:
        message = f'Hello There is no menu for today, Sorry'
    slackClient = WebClient(slack_token, run_async=True)
    asyncio.run(sendMessage(slackClient, message))


async def sendMessage(slackClient, message) -> None:
    users = await getUsers(slackClient)
    channels = await getChannels(slackClient, users)
    promises = [slackClient.chat_postMessage(channel=channel,
                                             text=message) for channel in channels]
    await asyncio.gather(*promises)


async def getChannels(slackClient, users):
    channels = []
    for user in users:
        conversation = await getConversation(slackClient, user)
        channels.append(conversation['channel']['id'])

    return channels


async def getConversation(slackClient, user):
    try:
        conversation = await slackClient.conversations_open(
            users=[user])
        return conversation
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")
        pass


async def getUsers(slackClient):
    try:
        response = await slackClient.users_list()
        users = response["members"]
        userlist = list(user['id']
                        for user in users if not user['is_bot'])
        return userlist
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")
        return []
