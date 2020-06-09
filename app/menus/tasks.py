
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
def send_menu_to_slack():
    """
    Start the broadcast of the message
    """
    menu = Menu.objects.get_today_menu()
    if menu:
        url = os.environ.get('TODAY_MENU_URL').format(menu.id)
        message = f'Hello Here is the link for todays Menu!.\n\n{url}'
    else:
        message = f'Hello There is no menu for today, Sorry'
    slackClient = WebClient(slack_token, run_async=True)
    asyncio.run(send_message(slackClient, message))


async def send_message(slackClient, message):
    """
    Recollect all users and channels, and send the messages
    """
    users = await get_users(slackClient)
    channels = await get_channels(slackClient, users)
    promises = [slackClient.chat_postMessage(channel=channel,
                                             text=message) for channel in channels]
    await asyncio.gather(*promises)


async def get_channels(slackClient, users):
    """
    Obtain the channels of all users
    """
    channels = []
    for user in users:
        conversation = await get_conversation(slackClient, user)
        channels.append(conversation['channel']['id'])

    return channels


async def get_conversation(slackClient, user):
    """
    Obtain the conversation to take the channel id from it
    """
    try:
        conversation = await slackClient.conversations_open(
            users=[user])
        return conversation
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")
        pass


async def get_users(slackClient):
    """
    Obtain all the users from the slack and filter the bots
    """
    try:
        response = await slackClient.users_list()
        users = response["members"]
        userlist = list(user['id']
                        for user in users if not user['is_bot'])
        return userlist
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")
        return []
