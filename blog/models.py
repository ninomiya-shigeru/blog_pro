from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Messageクラス
class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,\
                              related_name='message_owner')
    # group = models.ForeignKey('Group', on_delete=models.CASCADE)
    content = models.TextField(max_length=2000)
    aianswer = models.TextField(max_length=2000,blank=True, null=True)
    photo1 = models.ImageField(verbose_name='写真1', blank=True, null=True)
    # photo2 = models.ImageField(verbose_name='写真2', blank=True, null=True)
    # video_title = models.CharField(max_length=125, blank=True, null=True)
    # video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    # share_id = models.IntegerField(default=-1)
    # good_count = models.IntegerField(default=0)
    # share_count = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)

    class Meta:
        ordering = ('-pub_date',)




class Comment(models.Model):
    # id = models.BigAutoField(primary_key=True)  # ここで主キーを指定
    text = models.TextField("本文", blank=False)
    commented_at = models.DateTimeField("投稿日", auto_now_add=True)
    commented_to = models.ForeignKey(Message, verbose_name ='message',on_delete=models.CASCADE)
    commented_by = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="投稿者",
                                     on_delete=models.CASCADE)

    class Meta:
        db_table = 'comment'

    def __str__(self):
        return self.text


