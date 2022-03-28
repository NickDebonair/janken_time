from django.db import models

class TopicsManager(models.Manager): # 追記箇所(3～6行目)

  def pick_all_topics(self):
    return self.order_by('-id').all()



class Topics(models.Model):

  title = models.CharField(max_length=100)
  user = models.ForeignKey(
    'base.CustomUser', on_delete=models.CASCADE
  )
  objects = TopicsManager() # 追記箇所

  class Meta:
    db_table = 'topics'


class TextsManager(models.Manager): # 追記箇所(20～22行目)
  def pick_by_topic_id(self, topic_id):
    return self.filter(topic_id=topic_id).order_by('id').all()


class Texts(models.Model):

  text = models.CharField(max_length=500)
  user = models.ForeignKey(
    'base.CustomUser', on_delete=models.CASCADE
  )
  topic = models.ForeignKey(
    'Topics', on_delete=models.CASCADE
  )
  objects = TextsManager() # 追記箇所

  class Meta:
    db_table = 'texts'
