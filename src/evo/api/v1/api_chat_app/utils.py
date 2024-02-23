from PIL import Image

def check_image(image) -> bool:
    """
    Проверяет содержимое изображения и тип изображения

    :attr image -> изображение

    :return bool -> результат пройденной проверки
    """
    allowed_image_formats = ['JPEG', 'PNG', 'WEBP', 'SVG']
    
    try:
        image = Image.open(image)
        image.verify()

        if image.format not in allowed_image_formats:
            return False
        
        return True
    except:
        return False

    