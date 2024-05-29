import requests
from PIL import Image
from io import BytesIO
from urllib.parse import unquote
from pathlib import Path
import os


def get_image_from_url(url: str, save: bool = False, timeout: int = 1) -> Image:

    try:
        # Download Image from Url
        res = requests.get(url, timeout=timeout)
        img = Image.open(BytesIO(res.content))

        if save:

            # Set Default Filename
            default_filename = "download"
            path = Path(os.getcwd())
            num = len(list(path.glob(f'{default_filename}_*.jpg')))

            default_filename = f'{default_filename}_{num}'

            content_disposition = res.headers.get('Content-Disposition')

            if content_disposition:
                _, params = content_disposition.split(';')
                filename = next((s.strip() for s in params.split(
                    ',') if s.startswith('filename=')), None)

                filename = unquote(filename.split(
                    '=')[1]) if filename else default_filename

            else:
                filename = default_filename

            img.save(f'./{filename}.jpg', quality=100)

        return img
    except Exception as e:
        print(e)
        return None
