from django.db.models import QuerySet, Count, Q


class MailingQuerySet(QuerySet):
    """
    Менеджер рассылки
    """

    def annotate_msg_status_true_count(self):
        return self.annotate(msg_status_true_count=Count("message", filter=Q(message__status=True)))

    def annotate_msg_status_false_count(self):
        return self.annotate(
            msg_status_false_count=Count("message", filter=Q(message__status=False))
        )

    def annotate_msg_count(self):
        return self.annotate_msg_status_false_count().annotate_msg_status_true_count()
