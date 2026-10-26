from fastapi import FastAPI, HTTPException
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import uuid
import logging

app = FastAPI()
logger = logging.getLogger("resource_reservation")

# Local dicts as psudo resources
resources_db = {}
reservations_db = {}

# Response models
class CreateResourceRequest(BaseModel):
    name: str
    type: str # "desk","equipment"

class CreateReservationRequest(BaseModel):
    resource_id: str
    user_id: str # employee id
    start_time:str
    end_time:str

class ResourceResponse(BaseModel):
    # when a new resource gets succefully created
    resource_id: str
    name: str
    type: str
    status: str

class ReservationResponse(BaseModel):
    reservation_id:str
    resource_id:str
    user_id:str
    start_time:str
    end_time:str
    status:str

# APIs
@app.post("/create_resource", response_model=ResourceResponse)
async def create_resource(request: CreateResourceRequest):
    resource_id = str(uuid.uuid4()) ## create the id server side

    resource = {
        "resource_id":resource_id,
        "name":request.name,
        "type":request.type,
        "status":"available"
    }

    resources_db[resource_id] = resource
    logger.info("Resource created successfully: %s", resource_id)
    return resource

@app.get("/resources/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id:str):

    if resource_id not in resources_db:
        logger.warning("Resource fetch failed: resource_id=%s", resource_id)
        raise HTTPException(404, "resource not found")
    return resources_db[resource_id]

@app.get("/get-all-resources")
def list_all():
    return resources_db

@app.delete("/delete-resource/{resource_id}")
async def delete_resource(resource_id:str):

    if resource_id not in resources_db:
        logger.warning("Resource fetch failed: resource_id=%s", resource_id)
        raise HTTPException(404, "resource not found")

    # check if there are active reservations
    active_reservations = [
        reserv for reserv in reservations_db.values()
        if reserv["resource_id"] == resource_id and reserv["status"] == "active"
    ]

    if active_reservations:
        raise HTTPException(400, "cannot delete active reservation")

    del resources_db[resource_id]
    return {"message":"Successfully deleted the resource"}


@app.post("/create-reservation", response_model=ReservationResponse)
async def create_reservation(request: CreateReservationRequest):

    if request.resource_id not in resources_db:
        raise HTTPException(404, "Resource not found")

    # timings check and overlap check
    if request.end_time <= request.start_time:
        raise HTTPException(400, "End time must be after start time")

    # check resource availability for the selected time
    for reservation in reservations_db.values():
        if reservation["resource_id"] == request.resource_id:
            if reservation["status"] == "cancelled":
                continue
            
            # Check if times actually overlap
            if (request.start_time < reservation["end_time"] and 
                request.end_time > reservation["start_time"]):
                raise HTTPException(400, "Resource already booked for the selected time")

    reservation_id = str(uuid.uuid4())

    reservation_object = {
        "reservation_id":reservation_id,
        "resource_id":request.resource_id,
        "user_id":request.user_id,
        "start_time": request.start_time,
        "end_time": request.end_time,
        "status": "active"
    }

    reservations_db[reservation_id] = reservation_object
    return reservation_object

@app.delete("/cancel-reservations/{reservation_id}")
async def cancel_reservation(reservation_id:str):
    if reservation_id not in reservations_db:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    reservation = reservations_db[reservation_id]
    
    if reservation["status"] == "cancelled":
        raise HTTPException(status_code=400, detail="Reservation is already cancelled")
    
    reservation["status"] = "cancelled"
    logger.info("Reservation cancelled successfully: %s", reservation_id)

    return {"message": "Reservation cancelled successfully", "reservation": reservation}

@app.get("/list-all-reservations")
def get_all_reservations():
    return reservations_db

@app.get("/")
def root():
    return {
        "status": "healthy",
        "service": "Resource Reservation Service",
        "version": "1.0.0"
    }
    