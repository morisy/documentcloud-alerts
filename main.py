"""
A test of a DocumentCloud alert Add-On.
"""

from documentcloud.addon import AddOn
from documentcloud.constants import BULK_LIMIT
from documentcloud.toolbox import grouper, requests_retry_session


class Alert(AddOn):
    def main(self):
        documents = self.client.documents.list(id__in=self.documents)
        self.set_message("The alert has started and gotten a list of documents.")
        if documents:
            message = "New Documents Found Matching Your Alert\n"
            self.set_message("New Documents Found Matching Your Alert")
            for d in documents:
                message += f"{d.title} - {d.canonical_url}\n"
            self.send_mail("New documents found!", message)
            if self.data.get("slack_webhook"):
                SLACK_WEBHOOK = self.data.get("slack_webhook")
                requests_retry_session().post(
                SLACK_WEBHOOK, json={"text": message}
            )


if __name__ == "__main__":
    Alert().main()
