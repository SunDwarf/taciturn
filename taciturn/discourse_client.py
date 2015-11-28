from pydiscourse import client

from flask.ext.babel import gettext, ngettext

footer = gettext("\n\n------\n*I am a bot, this message was sent automatically.*\nPowered by [taciturn.]("
                 "https://github.com/SunDwarf/taciturn)")

class Client(client.DiscourseClient):
    def close(self, topic_id, **kwargs):
        """
        Close a topic.
        """
        return self._put("/t/{0}/status".format(topic_id), status="closed", enabled="true")

    def create_post(self, content, **kwargs):
        content = content + footer
        super().create_post(content, **kwargs)
