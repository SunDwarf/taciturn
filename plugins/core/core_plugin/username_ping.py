from taciturn.registry import nick_ping_registry
from taciturn.locale import Locale

from app import celery, client, __version__
from flask_babel import gettext

loc = Locale.get()


@celery.task
def username_ping(data: list):
    # Get the raw data from the request.
    post, user_misc, user = data
    post_data = post['raw']
    post_lines = post_data.split('\n')
    # Check the lines
    for line in post_lines:
        # Check if it starts with our nickname
        if line.startswith("@{}".format(client.api_username)):
            nline = line.split(" ")
            # Check if there's a command
            if len(nline) <= 1:
                return
            else:
                # Get the command and args
                command = nline[1]
                args = nline[1:]
                if command in nick_ping_registry:
                    # Call function
                    nick_ping_registry[command](data, *args)
                    return

def version_ping(data, *args: list):
    # Get topic ID.
    topic_id = data[0]["topic_id"]
    # Post a new message.
    client.create_post(loc.gettext("core.version").format(ver='.'.join(map(str, __version__))),
        topic_id=topic_id)

