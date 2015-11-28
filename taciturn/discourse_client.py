from pydiscourse import client

class Client(client.DiscourseClient):
    def close(self, topic_id, **kwargs):
        """
        Close a topic.
        """
        return self._put("/t/{0}/status".format(topic_id), status="closed", enabled="true")
