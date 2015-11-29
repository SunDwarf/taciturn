from pydiscourse import client

from taciturn import locale

loc = locale.Locale.get()

class Client(client.DiscourseClient):
    def close(self, topic_id, **kwargs):
        """
        Close a topic.
        """
        return self._put("/t/{0}/status".format(topic_id), status="closed", enabled="true")

    def create_post(self, content, **kwargs):
        footer = loc.gettext("core.footer")
        content = content + footer
        super().create_post(content, **kwargs)
