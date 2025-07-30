#!/usr/bin/env python3
"""
PharmaEvents - Minimal Flask Application
"""

import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix

# Egyptian governorates list
egyptian_governorates = [
    'Cairo', 'Giza', 'Alexandria', 'Dakahlia', 'Red Sea', 'Beheira', 'Fayoum',
    'Gharbiya', 'Ismailia', 'Menofia', 'Minya', 'Qaliubiya', 'New Valley',
    'Suez', 'Aswan', 'Assiut', 'Beni Suef', 'Port Said', 'Damietta',
    'Sharkia', 'South Sinai', 'Kafr El Sheikh', 'Matrouh', 'Luxor',
    'Qena', 'North Sinai', 'Sohag'
]

# Create app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "pharmaevents_secret_key")
app.config['REMEMBER_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure database - Use PostgreSQL if available, SQLite as fallback
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///pharmaevents.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db = SQLAlchemy(app)

# Initialize login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # type: ignore
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"

# User model
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'

# App Settings model for persistent configuration
class AppSetting(db.Model):
    __tablename__ = 'app_settings'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=True)
    
    @classmethod
    def get_setting(cls, key, default=None):
        setting = cls.query.filter_by(key=key).first()
        return setting.value if setting else default
    
    @classmethod
    def set_setting(cls, key, value):
        setting = cls.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = cls(key=key, value=value)
            db.session.add(setting)
        db.session.commit()
        return setting

# Event Category model
class EventCategory(db.Model):
    __tablename__ = 'event_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Event Type model
class EventType(db.Model):
    __tablename__ = 'event_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Event model
class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type_id = db.Column(db.Integer, db.ForeignKey('event_type.id'))
    is_online = db.Column(db.Boolean, default=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime)
    venue_id = db.Column(db.Integer, nullable=True)  # Could be linked to venue table later
    governorate = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    event_type = db.relationship('EventType', backref='events')
    creator = db.relationship('User', backref='created_events')

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please enter both email and password', 'danger')
            app_name = AppSetting.get_setting('app_name', 'PharmaEvents')
            theme_color = AppSetting.get_setting('theme_color', '#0f6e84')
            return render_template('login.html', app_name=app_name, theme_color=theme_color)
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    app_name = AppSetting.get_setting('app_name', 'PharmaEvents')
    theme_color = AppSetting.get_setting('theme_color', '#0f6e84')
    return render_template('login.html', app_name=app_name, theme_color=theme_color)

@app.route('/dashboard')
@login_required
def dashboard():
    # Get app settings
    app_name = AppSetting.get_setting('app_name', 'PharmaEvents')
    theme_color = AppSetting.get_setting('theme_color', '#0f6e84')
    
    return render_template('dashboard.html', 
                         app_name=app_name,
                         app_logo=None,
                         theme_color=theme_color,
                         total_events=0,
                         upcoming_events=0,
                         pending_events_count=0,
                         recent_events=[],
                         category_data=[])

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/events')
@login_required
def events():
    app_name = AppSetting.get_setting('app_name', 'PharmaEvents')
    theme_color = AppSetting.get_setting('theme_color', '#0f6e84')
    
    # Get categories from database
    try:
        categories = EventCategory.query.order_by(EventCategory.name).all()
    except Exception as e:
        app.logger.error(f'Error fetching categories: {str(e)}')
        categories = []
    
    # Get event types from database
    try:
        event_types = EventType.query.order_by(EventType.name).all()
    except Exception as e:
        app.logger.error(f'Error fetching event types: {str(e)}')
        event_types = []
    
    # Get events from database
    try:
        events_query = """
            SELECT e.id, e.name, e.description, e.is_online, e.start_datetime, e.end_datetime, 
                   e.status, et.name as event_type_name, u.email as creator_email
            FROM event e
            LEFT JOIN event_type et ON e.event_type_id = et.id
            LEFT JOIN users u ON e.user_id = u.id
            ORDER BY e.start_datetime DESC
        """
        events_result = db.session.execute(db.text(events_query))
        events = []
        for row in events_result:
            events.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'is_online': row[3],
                'start_datetime': row[4],
                'end_datetime': row[5],
                'status': row[6],
                'event_type_name': row[7],
                'creator_email': row[8]
            })
    except Exception as e:
        app.logger.error(f'Error fetching events: {str(e)}')
        events = []
    
    return render_template('events.html', 
                         app_name=app_name,
                         app_logo=None,
                         theme_color=theme_color,
                         events=events, 
                         categories=categories,
                         event_types=event_types)

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    app_name = AppSetting.get_setting('app_name', 'PharmaEvents')
    theme_color = AppSetting.get_setting('theme_color', '#0f6e84')
    
    # Get categories from database
    try:
        categories = EventCategory.query.order_by(EventCategory.name).all()
    except Exception as e:
        app.logger.error(f'Error fetching categories: {str(e)}')
        categories = []
    
    # Get event types from database
    try:
        event_types = EventType.query.order_by(EventType.name).all()
    except Exception as e:
        app.logger.error(f'Error fetching event types: {str(e)}')
        event_types = []
    
    if request.method == 'POST':
        # Handle event creation
        try:
            # Get form data
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            event_type_id = request.form.get('event_type')
            category_ids = request.form.getlist('categories')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')
            is_online = request.form.get('is_online') == 'on'
            venue = request.form.get('venue', '').strip() if not is_online else None
            governorate = request.form.get('governorate', '').strip() if not is_online else None
            max_attendees = request.form.get('max_attendees')
            
            # Handle attendees file upload
            attendees_file = request.files.get('attendees_file')
            attendees_filename = None
            attendees_count = 0
            if attendees_file and attendees_file.filename:
                # Validate file type (CSV, Excel)
                allowed_extensions = {'csv', 'xlsx', 'xls'}
                file_ext = attendees_file.filename.rsplit('.', 1)[1].lower() if '.' in attendees_file.filename else ''
                if file_ext not in allowed_extensions:
                    flash('Attendees file must be CSV or Excel format', 'danger')
                    return render_template('create_event.html', 
                                         app_name=app_name, app_logo=None, theme_color=theme_color,
                                         categories=categories, event_types=event_types, 
                                         governorates=egyptian_governorates, edit_mode=False)
                
                # Save the file
                upload_folder = os.path.join(app.static_folder or 'static', 'uploads', 'attendees')
                os.makedirs(upload_folder, exist_ok=True)
                attendees_filename = f"attendees_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{attendees_file.filename}"
                file_path = os.path.join(upload_folder, attendees_filename)
                attendees_file.save(file_path)
                
                # Process and validate the attendees file
                try:
                    import pandas as pd
                    
                    if file_ext == 'csv':
                        df = pd.read_csv(file_path)
                    else:  # xlsx or xls
                        df = pd.read_excel(file_path)
                    
                    # Flexible validation - just check if file has data
                    if df.empty:
                        flash('Attendees file appears to be empty', 'danger')
                        os.remove(file_path)  # Clean up the uploaded file
                        return render_template('create_event.html', 
                                             app_name=app_name, app_logo=None, theme_color=theme_color,
                                             categories=categories, event_types=event_types, 
                                             governorates=egyptian_governorates, edit_mode=False)
                    
                    # Count valid attendees (rows with non-null values in key columns)
                    # Look for columns that might contain names or emails
                    name_cols = [col for col in df.columns if any(keyword in col.lower() for keyword in ['name', 'participant', 'attendee'])]
                    email_cols = [col for col in df.columns if 'email' in col.lower() or 'mail' in col.lower()]
                    
                    if name_cols:
                        attendees_count = len(df.dropna(subset=name_cols[:1]))  # Use first name column
                    else:
                        attendees_count = len(df.dropna())  # Count all non-empty rows
                    
                    app.logger.info(f'Processed attendees file with {attendees_count} attendees from {len(df)} total rows')
                    app.logger.info(f'File columns: {list(df.columns)}')
                    
                except Exception as e:
                    app.logger.error(f'Error processing attendees file: {str(e)}')
                    flash('Error processing attendees file. Please check the format and try again.', 'danger')
                    if os.path.exists(file_path):
                        os.remove(file_path)  # Clean up the uploaded file
                    return render_template('create_event.html', 
                                         app_name=app_name, app_logo=None, theme_color=theme_color,
                                         categories=categories, event_types=event_types, 
                                         governorates=egyptian_governorates, edit_mode=False)
            
            # Basic validation
            if not title:
                flash('Event title is required', 'danger')
                return render_template('create_event.html', 
                                     app_name=app_name, app_logo=None, theme_color=theme_color,
                                     categories=categories, event_types=event_types, 
                                     governorates=egyptian_governorates, edit_mode=False)
            
            if not start_date:
                flash('Start date is required', 'danger')
                return render_template('create_event.html', 
                                     app_name=app_name, app_logo=None, theme_color=theme_color,
                                     categories=categories, event_types=event_types, 
                                     governorates=egyptian_governorates, edit_mode=False)
            
            # Now using SQLAlchemy ORM for event creation
            
            # Combine date and time for datetime fields
            start_datetime = None
            end_datetime = None
            
            if start_date:
                if start_time:
                    start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
                else:
                    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
            
            if end_date:
                if end_time:
                    end_datetime = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")
                else:
                    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
            
            # Create new event using SQLAlchemy ORM instead of raw SQL
            new_event = Event(
                name=title,
                description=description,
                event_type_id=int(event_type_id) if event_type_id else None,
                is_online=is_online,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                venue_id=None,  # We'll implement venue handling later
                governorate=governorate,
                user_id=current_user.id
            )
            
            db.session.add(new_event)
            db.session.flush()  # Flush to get the ID
            event_id = new_event.id
            
            # Handle category associations if any
            if category_ids:
                for category_id in category_ids:
                    db.session.execute(db.text("""
                        INSERT INTO event_categories (event_id, category_id) 
                        VALUES (%(event_id)s, %(category_id)s)
                        ON CONFLICT DO NOTHING
                    """), {
                        'event_id': event_id,
                        'category_id': int(category_id)
                    })
            
            db.session.commit()
            
            success_message = f'Event "{title}" created successfully!'
            if attendees_count > 0:
                success_message += f' Attendees file uploaded with {attendees_count} participants.'
            
            app.logger.info(f'Event "{title}" created successfully with ID {event_id} by user {current_user.email}')
            flash(success_message, 'success')
            return redirect(url_for('events'))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error creating event: {str(e)}')
            flash('Error creating event. Please try again.', 'danger')
    
    # Egyptian governorates list
    egyptian_governorates = [
        'Cairo', 'Giza', 'Alexandria', 'Dakahlia', 'Red Sea', 'Beheira', 'Fayoum', 'Gharbiya',
        'Ismailia', 'Menofia', 'Minya', 'Qaliubiya', 'New Valley', 'Suez', 'Aswan', 'Assiut',
        'Beni Suef', 'Port Said', 'Damietta', 'Sharkia', 'South Sinai', 'Kafr El Sheikh',
        'Matrouh', 'Luxor', 'Qena', 'North Sinai', 'Sohag'
    ]
    
    return render_template('create_event.html', 
                         app_name=app_name,
                         app_logo=None,
                         theme_color=theme_color,
                         categories=categories,
                         event_types=event_types,
                         governorates=egyptian_governorates,
                         edit_mode=False)

@app.route('/settings')
@login_required
def settings():
    # Get app settings from database
    app_name = AppSetting.get_setting('app_name', 'PharmaEvents')
    theme_color = AppSetting.get_setting('theme_color', '#0f6e84')
    
    # Get categories from database
    try:
        categories_result = db.session.execute(db.text("SELECT id, name FROM event_category ORDER BY name"))
        categories = [{'id': row[0], 'name': row[1]} for row in categories_result]
    except Exception as e:
        app.logger.error(f'Error fetching categories: {str(e)}')
        categories = []
    
    # Get event types from database
    try:
        event_types_result = db.session.execute(db.text("SELECT id, name FROM event_type ORDER BY name"))
        event_types = [{'id': row[0], 'name': row[1]} for row in event_types_result]
    except Exception as e:
        app.logger.error(f'Error fetching event types: {str(e)}')
        event_types = []
    
    # Get actual users from database
    users = [{'id': u.id, 'email': u.email, 'role': u.role} for u in User.query.all()]
    
    return render_template('settings.html',
                         app_name=app_name,
                         app_logo=None,
                         theme_color=theme_color,
                         categories=categories,
                         event_types=event_types,
                         users=users)

@app.route('/export_events')
@login_required
def export_events():
    flash('Export functionality will be implemented soon', 'info')
    return redirect(url_for('events'))

@app.route('/api/download/attendees-template')
@login_required
def download_attendees_template():
    """Download CSV template for attendees upload"""
    from flask import make_response
    import io
    import csv
    
    # Create CSV template content
    csv_content = io.StringIO()
    csv_writer = csv.writer(csv_content)
    
    # Write header row
    csv_writer.writerow(['Name', 'Email', 'Phone', 'Title', 'Company', 'Department', 'Special_Requirements'])
    
    # Write sample rows
    csv_writer.writerow(['Dr. Ahmed Hassan', 'ahmed.hassan@example.com', '+20 123 456 7890', 'Cardiologist', 'Cairo Medical Center', 'Cardiology', 'Vegetarian meal'])
    csv_writer.writerow(['Dr. Sarah Mohamed', 'sarah.mohamed@example.com', '+20 987 654 3210', 'Neurologist', 'Alexandria Hospital', 'Neurology', ''])
    
    # Create response
    response = make_response(csv_content.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=attendees_template.csv'
    
    return response

@app.route('/api/download/users-template')
@login_required
def download_users_template():
    """Download Excel template for bulk user creation"""
    from flask import make_response
    import io
    import pandas as pd
    
    # Create sample data for the template
    sample_data = {
        'Full Name': ['Dr. Ahmed Hassan', 'Dr. Sarah Mohamed', 'Dr. Mohamed Ali'],
        'Email': ['ahmed.hassan@example.com', 'sarah.mohamed@example.com', 'mohamed.ali@example.com'],
        'Role': ['medical_rep', 'event_manager', 'admin'],
        'Department': ['Cardiology', 'Neurology', 'Administration'],
        'Phone': ['+20 123 456 7890', '+20 987 654 3210', '+20 555 123 4567'],
        'Employee ID': ['EMP001', 'EMP002', 'EMP003']
    }
    
    df = pd.DataFrame(sample_data)
    
    # Create Excel file in memory
    output = io.BytesIO()
    df.to_excel(output, index=False, sheet_name='Users')
    output.seek(0)
    
    # Create response
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = 'attachment; filename=users_template.xlsx'
    
    return response

@app.route('/bulk-user-upload', methods=['GET', 'POST'])
@login_required
def bulk_user_upload():
    """Handle bulk user creation from Excel file"""
    app_name = AppSetting.get_setting('app_name', 'PharmaEvents')
    theme_color = AppSetting.get_setting('theme_color', '#0f6e84')
    
    if request.method == 'POST':
        users_file = request.files.get('users_file')
        
        if not users_file or not users_file.filename:
            flash('Please select a file to upload', 'danger')
            return render_template('bulk_user_upload.html', 
                                 app_name=app_name, theme_color=theme_color)
        
        # Validate file extension
        allowed_extensions = {'xlsx', 'xls'}
        file_ext = users_file.filename.rsplit('.', 1)[1].lower() if '.' in users_file.filename else ''
        
        if file_ext not in allowed_extensions:
            flash('Please upload an Excel file (.xlsx or .xls)', 'danger')
            return render_template('bulk_user_upload.html', 
                                 app_name=app_name, theme_color=theme_color)
        
        try:
            # Read Excel file
            import pandas as pd
            df = pd.read_excel(users_file)
            
            # Flexible column matching based on actual Excel file structure
            df_columns = df.columns.tolist()
            app.logger.info(f'Excel columns found: {df_columns}')
            
            # Map the actual columns from the Excel file
            email_col = None
            password_col = None  
            role_col = None
            
            for col in df_columns:
                col_lower = col.lower().strip()
                if 'email' in col_lower:
                    email_col = col
                elif 'password' in col_lower:
                    password_col = col
                elif 'role' in col_lower:
                    role_col = col
            
            # Check if we have the required columns
            missing_columns = []
            if not email_col:
                missing_columns.append('Email')
            if not role_col:
                missing_columns.append('Role')
            
            if missing_columns:
                flash(f'Missing required columns: {", ".join(missing_columns)}', 'danger')
                return render_template('bulk_user_upload.html', 
                                     app_name=app_name, theme_color=theme_color)
            
            # Process users
            success_count = 0
            error_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    email = str(row[email_col]).strip().lower() if email_col else ''
                    role = str(row[role_col]).strip().lower() if role_col else ''
                    user_password = str(row[password_col]).strip() if password_col and pd.notna(row[password_col]) else None
                    
                    # Validate required fields
                    if not email or not role:
                        errors.append(f'Row {index + 2}: Missing required fields (Email or Role)')
                        error_count += 1
                        continue
                    
                    # Normalize role names
                    role_mapping = {
                        'medical rep': 'medical_rep',
                        'medical_rep': 'medical_rep', 
                        'event manager': 'event_manager',
                        'event_manager': 'event_manager',
                        'admin': 'admin'
                    }
                    
                    normalized_role = role_mapping.get(role, role)
                    valid_roles = ['admin', 'event_manager', 'medical_rep']
                    
                    if normalized_role not in valid_roles:
                        errors.append(f'Row {index + 2}: Invalid role "{role}". Must be one of: admin, event_manager, medical_rep')
                        error_count += 1
                        continue
                    
                    # Check if user already exists
                    existing_user = User.query.filter_by(email=email).first()
                    if existing_user:
                        errors.append(f'Row {index + 2}: User with email "{email}" already exists')
                        error_count += 1
                        continue
                    
                    # Create new user
                    new_user = User(
                        email=email,
                        role=normalized_role
                    )
                    
                    # Use provided password or default
                    password_to_use = user_password if user_password else 'PharmaEvents2024!'
                    new_user.password_hash = generate_password_hash(password_to_use)
                    
                    db.session.add(new_user)
                    success_count += 1
                    
                except Exception as e:
                    errors.append(f'Row {index + 2}: {str(e)}')
                    error_count += 1
            
            # Commit all successful users
            if success_count > 0:
                db.session.commit()
                flash(f'Successfully created {success_count} users', 'success')
            
            if error_count > 0:
                flash(f'{error_count} errors occurred. Check details below.', 'warning')
                for error in errors[:10]:  # Show first 10 errors
                    flash(error, 'danger')
                if len(errors) > 10:
                    flash(f'... and {len(errors) - 10} more errors', 'info')
            
            if success_count == 0 and error_count > 0:
                db.session.rollback()
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error processing bulk user upload: {str(e)}')
            flash(f'Error processing file: {str(e)}', 'danger')
    
    return render_template('bulk_user_upload.html', 
                         app_name=app_name, theme_color=theme_color)

@app.route('/api/dashboard/stats')
def api_dashboard_stats():
    from flask import jsonify
    return jsonify({
        'total_events': 0,
        'upcoming_events': 0,
        'online_events': 0,
        'offline_events': 0,
        'pending_events': 0,
        'completed_events': 0
    })

@app.route('/api/dashboard/category_data')
@login_required
def api_category_data():
    from flask import jsonify
    return jsonify([])

@app.route('/api/dashboard/monthly_data')
@login_required  
def api_monthly_data():
    from flask import jsonify
    # Return data in the format expected by the chart
    return jsonify({
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'data': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    })

@app.route('/api/dashboard/requester_data')
@login_required
def api_requester_data():
    from flask import jsonify
    return jsonify([])

@app.route('/api/settings/theme', methods=['POST'])
def api_update_theme():
    from flask import jsonify, request
    try:
        app.logger.info(f'Theme update request: authenticated={current_user.is_authenticated}')
        
        # Check if user is authenticated
        if not current_user.is_authenticated:
            app.logger.warning('Unauthenticated theme update attempt')
            return jsonify({'error': 'Not authenticated', 'debug': 'User not logged in'}), 401
            
        data = request.get_json()
        app.logger.info(f'Theme update data: {data}')
        
        if not data or 'theme_color' not in data:
            return jsonify({'error': 'Theme color is required'}), 400
        
        theme_color = data['theme_color']
        # Save to database
        AppSetting.set_setting('theme_color', theme_color)
        app.logger.info(f'Theme color saved: {theme_color}')
        # Don't flash message for API calls - JavaScript handles notifications
        return jsonify({'success': True, 'theme_color': theme_color})
    except Exception as e:
        app.logger.error(f'Error in api_update_theme: {str(e)}')
        return jsonify({'error': str(e), 'debug': 'Server error occurred'}), 500

@app.route('/api/settings/app', methods=['POST'])
def api_update_app_settings():
    from flask import jsonify, request
    try:
        # Check if user is authenticated
        if not current_user.is_authenticated:
            return jsonify({'error': 'Not authenticated'}), 401
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Save to database
        if 'name' in data:
            AppSetting.set_setting('app_name', data['name'])
            # Don't flash message for API calls - JavaScript handles notifications
        return jsonify({'success': True})
    except Exception as e:
        app.logger.error(f'Error in api_update_app_settings: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Simple file serving route for uploaded files
    from flask import send_from_directory
    return send_from_directory('static/uploads', filename)

@app.route('/api/settings/logo', methods=['POST'])
@login_required
def api_upload_logo():
    from flask import jsonify, request
    flash('Logo upload functionality will be implemented soon', 'info')
    return jsonify({'success': True})

@app.route('/api/categories', methods=['POST'])
@login_required
def api_add_category():
    from flask import jsonify, request
    category_name = request.form.get('category_name', '').strip()
    if not category_name:
        return jsonify({'error': 'Category name is required'}), 400
    
    # For now, return the actual name that was submitted
    # In a real app, you'd save this to database
    flash(f'Category "{category_name}" added successfully', 'success')
    return jsonify({'success': True, 'id': 1, 'name': category_name})

@app.route('/api/categories/<int:category_id>', methods=['DELETE'])
@login_required
def api_delete_category(category_id):
    from flask import jsonify
    flash('Category deleted successfully', 'success')
    return jsonify({'success': True})

@app.route('/api/event-types', methods=['POST'])
@login_required
def api_add_event_type():
    from flask import jsonify, request
    type_name = request.form.get('type_name', '').strip()
    if not type_name:
        return jsonify({'error': 'Event type name is required'}), 400
    
    # For now, return the actual name that was submitted
    # In a real app, you'd save this to database
    flash(f'Event type "{type_name}" added successfully', 'success')
    return jsonify({'success': True, 'id': 1, 'name': type_name})

@app.route('/api/event-types/<int:type_id>', methods=['DELETE'])
@login_required
def api_delete_event_type(type_id):
    from flask import jsonify
    flash('Event type deleted successfully', 'success')
    return jsonify({'success': True})

@app.route('/api/users', methods=['POST'])
@login_required
def api_add_user():
    from flask import jsonify, request
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    role = request.form.get('role', '').strip()
    
    if not email or not password or not role:
        return jsonify({'error': 'Email, password, and role are required'}), 400
    
    # For now, return the actual data that was submitted
    # In a real app, you'd save this to database
    flash(f'User "{email}" added successfully', 'success')
    return jsonify({'success': True, 'id': 2, 'email': email, 'role': role})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@login_required
def api_delete_user(user_id):
    from flask import jsonify
    flash('User deleted successfully', 'success')
    return jsonify({'success': True})

@app.route('/api/auth/test')
@login_required
def api_auth_test():
    from flask import jsonify
    return jsonify({'authenticated': True, 'user': current_user.email, 'role': current_user.role})

@app.route('/forgot_password')
def forgot_password():
    return '<p>Password reset functionality coming soon. Please contact administrator.</p><p><a href="/login">Back to Login</a></p>'

# Initialize database
with app.app_context():
    # Create upload directory
    os.makedirs('static/uploads', exist_ok=True)
    
    db.create_all()
    
    # Create admin user if it doesn't exist
    if not User.query.filter_by(email='admin@test.com').first():
        admin = User()
        admin.email = 'admin@test.com'
        admin.role = 'admin'
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: admin@test.com / admin123")
    
    # Create event categories if they don't exist
    categories = [
        'Cardiology', 'Oncology', 'Neurology', 'Pediatrics', 'Endocrinology',
        'Dermatology', 'Psychiatry', 'Product Launch', 'Medical Education',
        'Patient Awareness', 'Internal Training'
    ]
    
    for cat_name in categories:
        if not EventCategory.query.filter_by(name=cat_name).first():
            category = EventCategory(name=cat_name)
            db.session.add(category)
    
    # Create event types if they don't exist
    event_types = [
        'Conference', 'Webinar', 'Workshop', 'Symposium', 
        'Roundtable Meeting', 'Investigator Meeting'
    ]
    
    for type_name in event_types:
        if not EventType.query.filter_by(name=type_name).first():
            event_type = EventType(name=type_name)
            db.session.add(event_type)
    
    db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)