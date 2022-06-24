"""
A test of a DocumentCloud alert Add-On.
"""

from documentcloud.addon import AddOn
from documentcloud.constants import BULK_LIMIT
from documentcloud.toolbox import grouper, requests_retry_session


class Alert(AddOn):
    def main(self):
        searchString = self.data.get("search") + "+created_at:[NOW-1HOUR TO *]"
        doc_list = self.client.documents.search(searchString)
        if not doc_list:
            self.set_message("No documents matching query found.")
            return
        self.set_message("Some documents matched this alert setting!")
        for document in doc_list:
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
