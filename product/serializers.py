from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from product.models import Product, Category, Review, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "id name parent".split()


class ProductSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = " id title description price category tags".split()

    def get_tags(self, product):
        l = []
        for i in product.tags.all():
            l.append((i.name))
        return [tag.name for tag in product.tags.all()]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ReviewsSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = " id title description price category tags".split()

    def get_tags(self, product):
        l = []
        for i in product.tags.all():
            l.append((i.name))
        return [tag.name for tag in product.tags.all()]


class ProductCreateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=3, max_length=100)
    description = serializers.CharField(max_length=1000)
    price = serializers.FloatField()
    category_id = serializers.IntegerField()
    tags = serializers.ListField(child=serializers.IntegerField())


def validate_title(self, title):
    products = Product.objects.filter(title=title)
    if products.count() > 0:
        raise ValidationError("Такой товар уже существует")
    return title


def validate_category_id(self, category_id):
    try:
        Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise ValidationError("Данной категории не существует")
    return category_id


def validate_tags(self, tags):
    count_tags = len(tags)
    tag_list = Tag.objects.filter(id__in=tags)
    if count_tags != tag_list.count():
        raise ValidationError("Некоторых тегов не сущесвует!!!")
    else:
        return tags


class ProductUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=3, max_length=100)
    description = serializers.CharField(max_length=1000)
    price = serializers.FloatField()
    category_id = serializers.IntegerField()
    tags = serializers.ListField(child=serializers.IntegerField())

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError("Данной категории не существует")
        return category_id

    def validate_tags(self, tags):
        t = list(dict.fromkeys(tags))
        print(t)
        count_tags = len(t)
        tag_list = Tag.objects.filter(id__in=t)
        if count_tags != tag_list.count():
            raise ValidationError("Некоторых тегов не сущесвует!!!")
        else:
            return tags


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
