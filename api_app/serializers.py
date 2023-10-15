from rest_framework import serializers

def validate_hex_color(value):
    """
    Check that the color field is a valid hex color.
    """
    if len(value) != 7:
        raise serializers.ValidationError("Color must be a valid hex color.")
    if value[0] != "#":
        raise serializers.ValidationError("Color must be a valid hex color.")
    for char in value[1:]:
        if char not in "0123456789abcdefABCDEF":
            raise serializers.ValidationError("Color must be a valid hex color.")
    
    return value

class QrCodeSerializer(serializers.Serializer):
    url = serializers.CharField(required=True)
    color = serializers.CharField(required=False, validators=[validate_hex_color])
    company_name = serializers.CharField(required=False)