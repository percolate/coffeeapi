from google.appengine.ext import ndb


class Coffee(ndb.Model):
    name = ndb.StringProperty(required=True)
    desc = ndb.StringProperty(required=True)
    image_url = ndb.StringProperty(required=True)
    created_at = ndb.DateTimeProperty(auto_now_add=True, required=True)
    last_updated_at = ndb.DateTimeProperty(auto_now=True, required=True)

    def to_json_full_dict(self):
        return {
            "id": self.key.id(),
            "name": self.name,
            "desc": self.desc,
            "image_url": self.image_url,
            "last_updated_at": str(self.last_updated_at),
        }

    def to_json_summary_dict(self):
        if len(self.desc) > 100:
            desc = self.desc[:100] + "..."
        else:
            desc = self.desc

        return {
            "id": self.key.id(),
            "name": self.name,
            "desc": desc,
            "image_url": self.image_url,
        }
