from django.db import models
from django.contrib.auth.models import User, AbstractUser


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        sum_post = 0
        sum_com = 0
        sum_post_com = 0
        auth = self.author
        for i in range(len(Post.objects.filter(author=Author.objects.get(author=User.objects.get(username=auth))))):
            sum_post += Post.objects.filter(author=Author.objects.get(author=User.objects.get(username=auth)))[
                i].article_rating

        for i in range(len(Comment.objects.filter(user=User.objects.get(username=auth)))):
            sum_com += Comment.objects.filter(user=User.objects.get(username=auth))[i].comment_rating

        for post in Post.objects.filter(author=Author.objects.get(author=User.objects.get(username=auth))):
            for comment in Comment.objects.filter(post=Post.objects.filter(text_title=post.text_title)[0]):
                sum_post_com += comment.comment_rating
        self.author_rating = sum_post * 3 + sum_com + sum_post_com
        self.save()

    def __str__(self):
        return self.author.username


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    news = 'news'
    article = 'article'

    Post_1 = [(news, 'News'), (article, 'article')]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    _category = models.ManyToManyField(Category, through='PostCategory', null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=10, choices=Post_1, default=news)
    text_news = models.TextField()
    text_title = models.CharField(max_length=50)
    article_rating = models.IntegerField(default=0)

    def like(self):
        self.article_rating += 1
        self.save()

    def dislike(self):
        self.article_rating -= 1
        self.save()

    def preview(self):
        preview = self.text_news[0:124]
        return preview + '...'

    def __str__(self):
        return f'??????????: {self.author.author.username} , ???????????? :{self.title}, ?????????????????? {self.text_title},reting: {self.article_rating}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.post + ';' + self.category


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    datetime = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return f'{self.post}, {self.user}, {self.comment_rating}'

