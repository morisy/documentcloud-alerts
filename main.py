"""
A test of a DocumentCloud alert Add-On.
"""

from documentcloud.addon import AddOn
from documentcloud.constants import BULK_LIMIT
from documentcloud.toolbox import grouper, requests_retry_session


class Alert(AddOn):
    def main(self):
        if not self.client.documents:
            self.set_message("No documents matching query found.")
            return
        numDocs = str(len(self.client.documents.list(id__in=self.documents)))
        message = f"{numDocs} documents found matching your alert\n"
        self.set_message(message)
        for document in self.client.documents.list(id__in=self.documents):
            self.set_message(f"Working on setting up an alert for {document.title}.")
            message += f"{document.title} - {document.canonical_url}\n"
        self.send_mail("New documents found!", message)
        if self.data.get("slack_webhook"):
            SLACK_WEBHOOK = self.data.get("slack_webhook")
            requests_retry_session().post(
            SLACK_WEBHOOK, json={"text": message}
            )


if __name__ == "__main__":
    Alert().main()
