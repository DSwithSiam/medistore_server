from rest_framework import serializers
from .models import Product, AdditionalInformation


class AdditionalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInformation
        fields = ["id", "key", "value"]


class ProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source="id", read_only=True)
    discounted_price = serializers.SerializerMethodField()
    additional_info = AdditionalInformationSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "product_id",
            "name",
            "product_image",
            "category",
            "used_for",
            "description",
            "price",
            "discount",
            "sku",
            "stock_quantity",
            "product_ref",
            "created_at",
            "discounted_price",
            "additional_info",
        ]

    def get_discounted_price(self, obj):
        return obj.get_discounted_price()


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    additional_info = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "product_image",
            "category",
            "used_for",
            "description",
            "price",
            "discount",
            "sku",
            "stock_quantity",
            "additional_info",
        ]

    def create(self, validated_data):
        additional_info_data = validated_data.pop("additional_info", [])
        product = Product.objects.create(**validated_data)

        for info in additional_info_data:
            product.additional_info.create(**info)

        return product

    def update(self, instance, validated_data):
        additional_info_data = validated_data.pop("additional_info", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if additional_info_data:
            instance.additional_info.all().delete()
            for info in additional_info_data:
                instance.additional_info.create(**info)

        return instance
