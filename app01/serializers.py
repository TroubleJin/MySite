from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    f_name = serializers.CharField()
    f_password = serializers.CharField()
    f_phone = serializers.CharField()
    f_sex = serializers.IntegerField()
    #  自定义序列化属性
    f_gender = serializers.SerializerMethodField()
    def get_gender(self,obj):
        return obj.get_f_sex_display()