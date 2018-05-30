from django.db import models


class Userinfo(models.Model):
    """
    用户表
    """
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=64, verbose_name="密码")
    email = models.EmailField(max_length=16, verbose_name="邮箱")


class NewsType(models.Model):
    """
    新闻类型表
    """
    caption = models.CharField(max_length=16, verbose_name="标题")


class News(models.Model):
    """
    新闻表
    """
    title = models.CharField(max_length=32, verbose_name="标题")
    url = models.URLField(max_length=255, verbose_name="url")
    avatar = models.CharField(max_length=255, verbose_name="头像")
    summary = models.CharField(max_length=255, verbose_name="简介")
    new_type = models.ForeignKey(to="NewsType", verbose_name="新闻类型")
    user = models.ForeignKey(to="Userinfo", verbose_name="发布者")
    ctime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    like_count = models.IntegerField(default=0, verbose_name="点赞数")
    comment_count = models.IntegerField(default=0, verbose_name="评论数")
    like = models.ManyToManyField(to="Userinfo", through="News2Like", through_fields=("new", "user"),
                                  related_name="likem2m", verbose_name="点赞m2m关系")
    comment = models.ManyToManyField(to="Userinfo", through="News2Comment", through_fields=("new", "user"),
                                     related_name="commentm2m", verbose_name="评论m2m关系表", )


class News2Like(models.Model):
    """
    点赞表
    """
    new = models.ForeignKey(to="News", verbose_name="点赞的新闻ID")
    user = models.ForeignKey(to="Userinfo", verbose_name="点赞者")
    ctime = models.DateTimeField(auto_now_add=True, verbose_name="点赞的时间")

    class Meta:
        unique_together = [
            ('new', 'user')
        ]


class News2Comment(models.Model):
    """
    评论表
    """
    new = models.ForeignKey(to="News", verbose_name="评论的新闻ID")
    user = models.ForeignKey(to="Userinfo", verbose_name="评论者")
    content = models.CharField(max_length=255, verbose_name="评论的内容")
    ctime = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    parent = models.ForeignKey(to="News2Comment", null=True, blank=True)

# News.objects.create(title="索禁令下的校园贷：有大学生半年贷了38家", url="http://news.sina.com.cn/s/qw/2017-09-19/doc-ifykyfwq8513368.shtml",
#                     avatar="user.png",
#                     summary="“第一次接触校园贷是因为学费丢了，不敢给家里说。怕家里知道又要挨骂。”今年大四的河南大学生高峰（化名）告诉新京报记者，当时正好在学校里看到有各种小广告，想着就试一下，写的利息也不高可以分期还，觉得自己可以还得起。但后来才发现还有各种管理费。", new_type_id=4,
#                     user_id=1, like_count=10, comment_count=20)
