from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from .utils.mongo import get_collection
from .utils.mongo import get_db
from .utils.mongo import get_gridfs_bucket
from datetime import datetime, timedelta



@api_view(['DELETE'])
def delete_batch(request, batch_id):
    fs = get_gridfs_bucket()
    db = get_db("text_to_video_db")

    # Delete all GridFS files
    for file in fs.find({"metadata.batch_id": batch_id}):
        fs.delete(file._id)

    # Delete batch record
    db["batches"].delete_one({"batch_id": batch_id})

    return Response({"status": "deleted", "batch_id": batch_id})


@api_view(['POST'])
def cleanup_inactive_batches(request):
    db = get_db("text_to_video_db")
    fs = get_gridfs_bucket()
    cutoff = datetime.utcnow() - timedelta(hours=1) #minutes=5 #hours=1

    inactive_batches = list(db["batches"].find({"last_active": {"$lt": cutoff}}))
    deleted_batches = []

    for batch in inactive_batches:
        batch_id = batch["batch_id"]

        # Delete all files with this batch_id
        for file in fs.find({"metadata.batch_id": batch_id}):
            fs.delete(file._id)

        # Delete the batch record itself
        db["batches"].delete_one({"batch_id": batch_id})
        deleted_batches.append(batch_id)

    return Response({
        "status": "cleanup complete",
        "deleted_batches": deleted_batches,
        "count": len(deleted_batches)
    })


@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_folder(request):
    image_file = request.FILES.get("image")
    batch_id = request.POST.get("batch_id")

    if not image_file or not batch_id:
        return Response({"error": "Missing required data"}, status=400)

    # Save image to GridFS
    fs = get_gridfs_bucket()
    file_id = fs.put(
        image_file,
        filename=image_file.name,
        content_type=image_file.content_type,
        metadata={
            "batch_id": batch_id,
            "upload_time": datetime.utcnow()
        }
    )

    # ✅ Update or insert batch record
    collection = get_collection("text_to_video_db","batches")
    collection.update_one(
        {"batch_id": batch_id},
        {
            "$set": {"last_active": datetime.utcnow()},
            "$setOnInsert": {"created_at": datetime.utcnow()}
        },
        upsert=True
    )

    return Response({
        "status": "image saved",
        "file_id": str(file_id),
        "filename": image_file.name,
        "batch_id": batch_id
    })

@api_view(['POST'])
def save_script(request):
    script_text = request.data.get("script", "")
    if not script_text:
        return Response({"error": "Missing script"}, status=400)

    collection = get_collection("text_to_video_db", "scripts")
    result = collection.insert_one({"script": script_text})

    return Response({"status": "saved", "id": str(result.inserted_id)})


@api_view(['GET'])
def test_api(request):
    return Response({"message": "API is working ✅"})