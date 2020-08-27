from rest_framework import serializers
from rest_framework import exceptions
from rest_framework.serializers import ListSerializer
from . import models


class UserSerializer(serializers.Serializer):
    f_name = serializers.CharField()
    f_password = serializers.CharField()
    f_phone = serializers.CharField()
    f_sex = serializers.IntegerField()
    f_gender = serializers.SerializerMethodField()
    #  自定义序列化属性
    def get_f_gender(self,obj):
        return obj.get_f_sex_display()


class UserDeserializer(serializers.Serializer):
    f_name = serializers.CharField(
        max_length=10,min_length=2,error_messages={
            'max_length': '名称太长',
            'min_length': '名称太短'
        }
    )
    f_phone = serializers.CharField()
    f_password = serializers.CharField(max_length=32)
    f_sex = serializers.IntegerField()
    #  自定义有校验规则的反序列化字段
    re_f_password = serializers.CharField(max_length=32)

    #  字段级反序列化
    def validate_f_name(self,value):
        if '0' in value.lower():
            raise exceptions.ValidationError('名字错误')
        return value

    def validate_f_password(self, value):
        if '0' in value.lower():
            raise exceptions.ValidationError('密码带0,不行')
        return value

    #   对象级验证
    def validate(self, attrs):
        # 必须pop走,不能留下多余字段
        if attrs.get('f_password') != attrs.pop('re_f_password'):
            raise  exceptions.ValidationError('两次密码不一致')
        return attrs

    def create(self, validated_data):
        return models.t_user.objects.create(**validated_data)

class BookListSerializer(ListSerializer):
    def update(self, instance, validated_data):
        # print(instance)  # 要更新的对象们
        # print(validated_data)  # 更新的对象对应的数据们
        # print(self.child)  # 服务的模型序列化类 - V2BookModelSerializer
        for index, obj in enumerate(instance):
            self.child.update(obj, validated_data[index])
        return instance

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        # 序列化关联的model的类
        model = models.t_book
        list_serializer_class = BookListSerializer
        # 参与序列化的所有字段
        # fields = '__all__'
        # 排除字段
        # exclude = ('f_id',)
        # 指定嵌套序列化,自动深度
        # depth = 1
        fields = ('f_id','f_book_name','f_book_description','f_book_country','f_book_price','f_publish_name','f_author_name','f_book_publish','t_author_set')
        extra_kwargs = {
            "f_book_name" : {
                "required": True,
                "error_messages": {
                    "min_length": 1,
                    "required": "书籍名称必须填写"
                }
            },
            # read_only 只序列化,write_only 只反序列化
            # 'f_id':{'read_only': True},
            # 'f_book_name':{'read_only': True},
            # 'f_book_description':{'read_only': True},
            # 'f_book_price':{'read_only': True},
            # 'f_publish_name':{'read_only': True},
            # 'f_author_name':{'read_only': True},
            # 'f_book_publish':{'write_only': True},

        }
    def validate_f_book_name(self,value):
        if models.t_book.objects.filter(f_book_name=value):
            raise exceptions.ValidationError('书名已经存在')
        return  value

    def validate(self, attrs):
        return attrs

class BookDeserializer(serializers.ModelSerializer):
    class Meta:
        # 序列化关联的model的类
        model = models.t_book
        fields = ('f_book_name', 'f_book_description', 'f_book_country', 'f_book_price', 'f_book_publish')

class PublisherSerializer(serializers.ModelSerializer):
    f_country = serializers.SerializerMethodField()
    class Meta:
        model = models.t_publisher
        fields = ('f_id','f_publisher_name','f_country')
        extra_kwargs = {
            "f_publisher_name": {
                "required": True,
                "error_messages": {
                    "min_length": 1,
                    "required": "出版社名称必须填写"
                }
            },
        }
    def get_f_country(self,obj):
        return '中国'



class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        # 序列化关联的model的类
        model = models.t_school
        fields = ('f_name', 'f_region','f_price')