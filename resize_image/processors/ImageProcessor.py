
#from PIL.Image import Image


from PIL import Image, ImageOps

#*Logger
import logging
logger = logging.getLogger(__name__)






class ImageProcessor:
    def __init__(self,thumbnail_size:int ) -> None:
        self._thumbnail_size = thumbnail_size
        
        

    def createThumbnail(self,image: Image.Image) -> Image.Image:
        target_size = (self.createThumbnail, self._thumbnail_size)

        thumbnail = ImageOps.fit(
            image=image,
            size=(
                self._thumbnail_size,
                self._thumbnail_size,
            ),
            method=Image.Resampling.LANCZOS,
        )
        
        logger.debug(
                "Thumbnail created",
                extra={
                    "original_size": image.size,       # (width, height) — ממדים, לא בתים
                    "thumbnail_size": thumbnail.size,
                    "mode": image.mode,                # RGB / RGBA / P / L ...
                },
            )
        
        return thumbnail
        
        
