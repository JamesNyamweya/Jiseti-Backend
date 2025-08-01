from flask_restful import Resource, reqparse
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.baseModel import db
from models.userModel import User
from models.recordModel import Record
from datetime import datetime, timezone
import cloudinary
import cloudinary.uploader


def is_admin(user_id):
    user = User.query.get(user_id)
    if (user and user.role == "admin"):
        return True
    return False

class RecordResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('type', required=False, help='Type is required')
    parser.add_argument('title', required=False, help='Title is required')
    parser.add_argument('description', required=False, help='Description is required')
    parser.add_argument('latitude', type=float, required=False)
    parser.add_argument('longitude', type=float, required=False)
    parser.add_argument('status', type=str, required=False)
    parser.add_argument('images', type=str, location='json', required=False)

    # GET all records or specific record
    @jwt_required()
    def get(self, record_id=None):
        user_id = get_jwt_identity()
        
        if record_id:
            record = Record.query.get(record_id)
            if not record:
                return {'message': 'Record not found'}, 404
            
            if record.user_id != int(user_id) and not is_admin(user_id):
                return {'message': 'Unauthorized access'}, 403
                
            return self.format_record(record)
        else:
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 10, type=int), 100)
            
        if is_admin(user_id):
            records = Record.query.all()
        else:
            records = Record.query.filter_by(user_id=user_id).all()

            
            return {
                'records': [self.format_record(r) for r in records],
            }
    
    def format_record(self, record):
        return {
            'id': record.id,
            'type': record.type,
            'title': record.title,
            'description': record.description,
            # 'location_address': record.location_address,
            'latitude': record.latitude,
            'longitude': record.longitude,
            'images': record.images or '',
            # 'videos': record.videos or [],
            'status': record.status,
            # 'created_by': record.created_by,
            'created_at': record.created_at.isoformat() if record.created_at else None,
            'updated_at': record.updated_at.isoformat() if record.updated_at else None,
            'user_id': record.user_id
            # 'admin_comment': getattr(record, 'admin_comment', None)
        }


    # CREATE new record
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        try:
            record_type = request.form.get('type')
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            latitude = request.form.get('latitude', type=float)
            longitude = request.form.get('longitude', type=float)

            if record_type not in ['Red-Flag', 'Intervention']:
                return {'message': 'Type must be Red-Flag or Intervention'}, 400

            if latitude is not None and not -90 <= latitude <= 90:
                return {'message': 'Invalid latitude'}, 400

            if longitude is not None and not -180 <= longitude <= 180:
                return {'message': 'Invalid longitude'}, 400


            uploaded_files = request.files.getlist('images')
            image_urls = []
            for file in uploaded_files:
                if file:
                    upload_result = cloudinary.uploader.upload(file)
                    image_urls.append(upload_result['secure_url'])  # fixed typo here
                    
            record = Record(
                type=record_type,
                title=title,
                description=description,
                latitude=latitude,
                longitude=longitude,
                images=image_urls,
                status='pending',
                user_id=int(user_id),
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )

            db.session.add(record)
            db.session.commit()

            return {
                'message': 'Record created successfully',
                'record': self.format_record(record)
            }, 201

        except Exception as e:
            db.session.rollback()
            return {'message': f'Error creating record: {str(e)}'}, 500
    
    # UPDATE record
    @jwt_required()

    def put(self, record_id):
        user_id = get_jwt_identity()
        record = Record.query.get(record_id)
        
        if not record:
            return {'message': 'Record not found'}, 404
            
        if record.user_id != int(user_id):
            return {'message': 'Unauthorized to edit this record'}, 403
        
        if record.status in ['under investigation', 'rejected', 'resolved']:
            return {'message': 'Cannot edit record with current status'}, 400

        try:
            record_type = request.form.get("type")
            if record_type:
                if record_type.lower() not in ['red-flag', 'intervention']:
                    return {'message': 'Invalid record type'}, 400
                record.type = record_type.capitalize() if record_type.lower() == "intervention" else "Red-Flag"

            title = request.form.get('title')
            description = request.form.get('description')
            latitude = request.form.get('latitude', type=float)
            longitude = request.form.get('longitude', type=float)

            if not all([record_type, title, description, latitude, longitude]):
                return {'message': 'All fields (type, title, description, latitude, longitude) are required'}, 400

            if not -90 <= latitude <= 90:
                return {'message': 'Invalid latitude'}, 400
            record.latitude = latitude

            if not -180 <= longitude <= 180:
                return {'message': 'Invalid longitude'}, 400
            record.longitude = longitude

            record.title = title.strip()
            record.description = description.strip()

            # Handle uploaded image files
            uploaded_files = request.files.getlist('images')
            if uploaded_files:
                image_urls = []
                for file in uploaded_files:
                    if file:
                        upload_result = cloudinary.uploader.upload(file)
                        image_urls.append(upload_result['secure_url'])
                record.images = image_urls

            record.updated_at = datetime.now(timezone.utc)
            db.session.commit()

            return {
                'message': 'Record updated successfully',
                'record': self.format_record(record)
            }

        except Exception as e:
            db.session.rollback()
            return {'message': f'Error updating record: {str(e)}'}, 500

    # DELETE record
    @jwt_required()
    def delete(self, record_id):
        user_id = get_jwt_identity()
        record = Record.query.get(record_id)
        
        if not record:
            return {'message': 'Record not found'}, 404
            
        if record.user_id != int(user_id):
            return {'message': 'Unauthorized to delete this record'}, 403
        
        if record.status in ['under investigation', 'rejected', 'resolved']:
            return {'message': 'Cannot delete record with current status'}, 400
        
        try:
            db.session.delete(record)
            db.session.commit()
            return {'message': 'Record deleted successfully'}
            
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error deleting record: {str(e)}'}, 500
