from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from s3direct.fields import S3DirectField


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('Category', null=True, blank=True, related_name='cat_child')
    order = models.IntegerField(null=True, blank=True)
    hidden = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    @property
    def products(self):
        return self.categories.filter(status='Active').order_by('-id')[:8]

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(User)
    categories = models.ManyToManyField(Category, blank=True, related_name='categories')
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    short_description = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    STATUS_CHOICES = (
        ('Active','Active'),
        ('Inactive','Inactive'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Inactive")

    @property
    def questions_no_answer(self):
        return self.productquestion_set.filter(status='Active', productanswer__isnull=True)

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            super(Product, self).save()
            self.slug = '%s-%i' % (slugify(self.name), self.id)
        super(Product, self).save(*args, **kwargs)




class ProductQuestion(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey('Product')
    question = models.TextField()
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Active")

    class Meta:
        verbose_name_plural = "Product Questions"

    @property
    def get_answers(self):
        return self.productanswer_set.filter()

    def __str__(self):
        return self.question


class ProductAnswer(models.Model):
    user = models.ForeignKey(User)
    product_question = models.ForeignKey(ProductQuestion)
    answer = models.TextField()
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Active")

    class Meta:
        verbose_name_plural = "Answers"

    def __str__(self):
        return self.answer


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    cpf = models.CharField(max_length=35, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=20, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=15, null=True, blank=True)
    zipcode = models.CharField(max_length=15, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    remote_customer_id = models.CharField(max_length=255, null=True, blank=True, default='')
    remote_receiver_id = models.CharField(max_length=255, null=True, blank=True, default='')


class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name='prod_images')
    images = S3DirectField(dest='product_images')

    class Meta:
        verbose_name_plural = "Images"