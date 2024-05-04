import uuid
from typing import Any, Optional

from sqlalchemy_file import File
from sqlalchemy_file.storage import StorageManager
from sqlalchemy_file.stored_file import StoredFile


class NamedFile(File):
    def store_content(
        self,
        content: Any,
        upload_storage: Optional[str] = None,
        name: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
        extra: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
        content_path: Optional[str] = None,
    ) -> StoredFile:
        """Store content into provided `upload_storage`
        with additional `metadata`. Can be used by processors
        to store additional files.
        """
        name = name or self.filename or str(uuid.uuid4())
        stored_file = StorageManager.save_file(
            name=name,
            content=content,
            upload_storage=upload_storage,
            metadata=metadata,
            extra=extra,
            headers=headers,
            content_path=content_path,
        )
        self["files"].append(f"{upload_storage}/{name}")
        return stored_file
