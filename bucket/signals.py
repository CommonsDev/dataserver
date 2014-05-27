from __future__ import unicode_literals
from haystack.signals import RealtimeSignalProcessor


class RelatedRealtimeSignalProcessor(RealtimeSignalProcessor):
    """
    Extension to haystack's RealtimeSignalProcessor not only causing the
    search_index to update on saved model, but also for related effected models
    """

    def handle_save(self, sender, instance, **kwargs):
        super(RelatedRealtimeSignalProcessor, self).handle_save(sender, instance, **kwargs)
        self.handle_related(sender, instance)

    def handle_delete(self, sender, instance, **kwargs):
        super(RelatedRealtimeSignalProcessor, self).handle_delete(sender, instance, **kwargs)
        self.handle_related(sender, instance)

    def handle_related(self, sender, instance):
        for related in self.get_related_models(sender, instance):
            super(RelatedRealtimeSignalProcessor, self).handle_save(
                related['sender'],
                related['instance']
        )

    def get_related_models(self, sender, instance):
        from taggit.models import TaggedItem

        related = []
        if sender == TaggedItem:
            related.append({
                'sender': instance.content_object.__class__,
                'instance': instance.content_object
        })
        return related