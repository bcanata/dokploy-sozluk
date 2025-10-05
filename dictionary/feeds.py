from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed

from dictionary.models import Author, Entry


class UserEntriesFeed(Feed):
    """RSS feed for user's published entries."""

    def get_object(self, request, slug):
        return get_object_or_404(Author, slug=slug)

    def title(self, obj):
        return f"{obj.username}'s entries"

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return f"Latest entries from {obj.username}"

    def items(self, obj):
        return (
            Entry.objects_published.filter(author=obj)
            .select_related("topic", "author")
            .order_by("-date_created")[:50]
        )

    def item_title(self, item):
        return item.topic.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.date_created

    def item_updateddate(self, item):
        return item.date_edited if item.date_edited else item.date_created

    def item_author_name(self, item):
        return item.author.username


class UserEntriesAtomFeed(UserEntriesFeed):
    """Atom feed for user's published entries."""

    feed_type = Atom1Feed
    subtitle = UserEntriesFeed.description
