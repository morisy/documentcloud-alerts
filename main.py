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
            documentCount = documents.len()
            message = f"{documentCount} documents found matching your alert\n"
            self.set_message(message)
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
