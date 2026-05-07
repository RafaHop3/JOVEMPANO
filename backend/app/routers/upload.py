from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
import cloudinary
import cloudinary.uploader
import logging
from app.core.config import settings
from app.utils.security import validate_image_upload
from app.core.security import get_current_user

# O SDK do Cloudinary já configura automaticamente se a env CLOUDINARY_URL existir
cloudinary.config(secure=True)

router = APIRouter()

@router.post("/")
async def upload_image(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    # 1. Inspeção de Binário (Cyber Safety)
    await validate_image_upload(file)
    
    try:
        # 2. Leitura em Memória
        file_content = await file.read()
        
        # 3. Upload Direto para o Cloudinary
        # O uso de public_id auto-gerado pelo Cloudinary previne Path Traversal
        upload_result = cloudinary.uploader.upload(
            file_content,
            folder="jovempano_uploads", 
            resource_type="image"
        )
        
        # Retorna a URL segura (HTTPS) pronta para o banco de dados
        return {"secure_url": upload_result.get("secure_url")}
        
    except Exception as e:
        # Log da exceção real para o sistema de monitoramento
        logging.error(f"Erro no upload para Cloudinary: {str(e)}")
        raise HTTPException(status_code=500, detail="Falha ao processar o upload no servidor externo.")
