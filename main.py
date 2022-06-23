"""
This is a hello world add-on for DocumentCloud.

It demonstrates how to write a add-on which can be activated from the
DocumentCloud add-on system and run using Github Actions.  It receives data
from DocumentCloud via the request dispatch and writes data back to
DocumentCloud using the standard API
"""

from documentcloud.addon import AddOn


class Alert(AddOn):
    def main(self):
        documents = self.client.documents.list(id__in=self.documents):
        if documents:
            message = [f"New Documents Found Matching Your Alert\n"]
            self.set_message(message)
            message.extend([f"{d.title} - {d.canonical_url}\n" for d in documents])
            self.send_mail(f"New documents found!", "\n".join(message))
            if SLACK_WEBHOOK:
                requests_retry_session().post(
                SLACK_WEBHOOK, json={"text": f"{subject}\n\n{message}"}
            )


if __name__ == "__main__":
    Alert().main()
