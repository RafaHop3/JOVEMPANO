import magic
from fastapi import HTTPException, UploadFile

# Limite de 2MB para evitar DoS por exaustão de disco
MAX_FILE_SIZE = 2 * 1024 * 1024 
ALLOWED_MIMES = ["image/jpeg", "image/png", "image/webp"]

async def validate_image_upload(file: UploadFile):
    # 1. Checagem de Tamanho
    content = await file.read(MAX_FILE_SIZE + 1)
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Arquivo muito grande. Máximo 2MB.")
    
    # 2. MIME Sniffing Real (Magic Numbers)
    mime = magic.from_buffer(content, mime=True)
    if mime not in ALLOWED_MIMES:
        raise HTTPException(status_code=400, detail=f"Tipo de arquivo inválido detectado pelo magic number: {mime}")
    
    # Reposiciona o ponteiro para o início para que o arquivo possa ser salvo
    await file.seek(0)
    return True
