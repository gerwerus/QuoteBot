from pydantic import BaseModel, Field, HttpUrl


class ImageModel(BaseModel):
    link: HttpUrl
    
    def __init__(self, width: int, **data):
        super().__init__(link=f"{data["raw"]}?q=75&fm=jpg&w={width}&fit=max", **data)


class UnsplashModel(BaseModel):
    result: ImageModel

    def __init__(self, **data):
        super().__init__(result=ImageModel(width=data['width'], **data['urls']), **data)
