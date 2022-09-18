from django.db.models import Count, Q, QuerySet


class MailingQuerySet(QuerySet):
    def annotate_msg_sent_count(self):
        return self.annotate(
            msg_sent_count=Count("message", filter=Q(message__status=True))
        )

    def annotate_msg_not_sent_count(self):
        return self.annotate(
            msg_not_sent_count=Count("message", filter=Q(message__status=False))
        )

    def annotate_msg_count(self):
        return self.annotate_msg_sent_count().annotate_msg_not_sent_count()
