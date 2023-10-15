# Let's begin by importing the tools we'll need on our journey!
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
import qrcode  # Our magic wand to make QR codes
from django.http import HttpResponse
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from PIL import Image, ImageDraw, ImageFont  # Our artistic tools for image crafting
from .serializers import QrCodeSerializer  # This will help us understand incoming data
from rest_framework import status  # To talk back in HTTP language

# Some custom tools we've built for our special journey
from .permissions import IsAuthenticatedOrFromRapidAPI
from .authentications import RapidAPIAuthentication

# Welcome to the heart of our journey, the QR code forest!
class ApiQrCode(APIView):
    # Here we decide which languages we're comfortable speaking with our visitors.
    parser_classes = (JSONParser, FormParser, MultiPartParser)
    
    # Our friendly forest guards who check the visitor's passes.
    authentication_classes = [TokenAuthentication, RapidAPIAuthentication]
    
    # Rules of the forest! Who's allowed and who's not.
    permission_classes = [IsAuthenticatedOrFromRapidAPI]

    # When someone sends a postcard (POST request) to the forest...
    def post(self, request):
        # We try to understand their message using the QrCodeSerializer.
        serializer = QrCodeSerializer(data=request.data)
        
        # If we can understand their message...
        if serializer.is_valid():
            # We extract the important bits from their message.
            url = serializer.validated_data['url']
            color = serializer.validated_data.get('color', None)
            company_name = serializer.validated_data.get('company_name', None)
            
            # If they didn't mention a favorite color, we choose classic black.
            if color is None:
                color = '#000000'
            
            # Using our QR wand, we start crafting the magical QR code.
            qr = qrcode.QRCode(version=5, box_size=10, border=4)
            qr.add_data(url)  # We pour the URL essence into the mix.
            qr.make(fit=True)  # We make sure it's a perfect fit!
            img = qr.make_image(fill_color=color, back_color='white')  # The QR code comes to life!
            
            # We use some artistic tools to refine our creation.
            pil_img = img.convert('RGBA')
            draw = ImageDraw.Draw(pil_img)
            width, height = pil_img.size  # Checking the canvas size
            
            # If they whispered a company name, we inscribe it onto the QR code.
            if company_name is not None:
                # Adjusting the font size to make it look perfect!
                font_size = int(min(width, height) / 30)
                font = ImageFont.truetype('api_app/Lato-Bold.ttf', font_size)
                text_width, text_height = draw.textsize(company_name, font=font)
                
                # Finding the perfect spot for the name.
                text_x = int((width - text_width) / 2)
                text_y = int((height - text_height) / 2)
                
                # We add a small glowing rectangle behind the name to make it stand out.
                padding = 10
                rect_x1 = text_x - padding
                rect_y1 = text_y - padding
                rect_x2 = text_x + text_width + padding
                rect_y2 = text_y + text_height + padding
                draw.rectangle((rect_x1, rect_y1, rect_x2, rect_y2), fill='white')
                
                # With a steady hand, we write the company name onto the QR code.
                draw.text((text_x, text_y), company_name, font=font, fill='black')
            
            # Our QR code artwork is ready!
            img = pil_img
            
            # We lovingly place it on a digital canvas and present it to our visitor.
            response = HttpResponse(content_type='image/png')
            img.save(response, 'PNG')
            return response
        
        # If we couldn't understand their message...
        else:
            # We kindly ask them to check their postcard for mistakes.
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
