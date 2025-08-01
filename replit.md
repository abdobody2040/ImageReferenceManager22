# PharmaEvents - Event Management System

## Current Status: Application Successfully Migrated and Enhanced

**Resolution**: Application successfully migrated from Replit Agent to standard Replit environment with full functionality restored and significant improvements implemented.

**Progress Made**: 
- ✅ Resolved SQLAlchemy "Class already has a primary mapper defined" error
- ✅ Consolidated working code back to standard app.py architecture
- ✅ Successfully started application server on port 5000 (updated for standard Replit environment)
- ✅ Fixed template routing issues and missing route endpoints
- ✅ Login page loading correctly with all static assets
- ✅ Application running with PostgreSQL/SQLite database support
- ✅ Implemented persistent theme color storage with AppSetting model
- ✅ Fixed JavaScript API authentication for settings functionality
- ✅ Fixed JavaScript syntax errors causing console warnings
- ✅ Added optional image upload functionality to event creation
- ✅ Improved button layout in events page with proper grouping
- ✅ Added comprehensive event details page with full information display
- ✅ Fixed event editing and viewing functionality
- ✅ Enhanced dashboard charts initialization and error handling

## Overview

PharmaEvents is a web-based event management application designed specifically for pharmaceutical companies to manage events while maintaining regulatory compliance. The system provides role-based access control with admin, event manager, and medical representative roles, along with comprehensive event creation, management, and reporting capabilities.

## System Architecture

### Frontend Architecture
- **Templates**: Jinja2-based HTML templates with Bootstrap 5.3.3 for responsive UI
- **CSS Framework**: Bootstrap with custom CSS variables for theming and dark mode support
- **JavaScript**: Vanilla JavaScript with jQuery for enhanced functionality
- **Component Libraries**:
  - Font Awesome 6.5.2 for icons
  - Select2 for enhanced select dropdowns
  - Chart.js 4.4.2 for dashboard analytics
  - Flatpickr for date/time pickers
- **Theme Support**: Light/dark mode toggle with CSS custom properties

### Backend Architecture
- **Framework**: Flask 3.1.1 with SQLAlchemy 2.0.40 ORM
- **Authentication**: Flask-Login for session management with role-based access control
- **Database**: PostgreSQL (production) with SQLite fallback (development)
- **File Handling**: Werkzeug for secure file uploads with 2MB limit
- **Deployment**: Gunicorn WSGI server with autoscale deployment target

### Database Schema
- **Users**: Email-based authentication with role hierarchy (admin > event_manager > medical_rep)
- **Events**: Comprehensive event model with online/offline support, categories, and venue management
- **Configuration**: AppSetting table for dynamic application configuration
- **Relationships**: Many-to-many associations between events and categories

## Key Components

### Authentication System
- Role-based access control with three user types
- Password hashing using Werkzeug security utilities
- Session-based authentication with Flask-Login
- Admin-only routes protected with custom decorators

### Event Management
- Full CRUD operations for events with rich metadata
- Support for both online and offline events
- Image upload with file validation and storage
- Multi-category tagging system
- Venue management with governorate-based filtering

### Dashboard & Analytics
- Real-time statistics with Chart.js visualizations
- Event filtering by date, category, and type
- Export functionality for compliance reporting
- Role-specific dashboard views

### File Management
- Secure file upload handling with extension validation
- Image storage in static/uploads directory
- 2MB file size limit enforcement
- Support for PNG, JPG, JPEG formats

## Data Flow

1. **User Authentication**: Login → Session Creation → Role Verification → Dashboard Redirect
2. **Event Creation**: Form Validation → File Upload Processing → Database Storage → Success Confirmation
3. **Event Management**: List View → Filter Application → CRUD Operations → Database Updates
4. **Analytics**: Data Aggregation → Chart Generation → Dashboard Display

## External Dependencies

### Python Packages
- **Flask Stack**: flask, flask-sqlalchemy, flask-login
- **Database**: psycopg2-binary for PostgreSQL connectivity
- **Validation**: email-validator for form validation
- **Deployment**: gunicorn for production serving

### Frontend Libraries
- **Bootstrap 5.3.3**: UI framework and components
- **Font Awesome 6.5.2**: Icon library
- **Chart.js 4.4.2**: Data visualization
- **Select2**: Enhanced select dropdowns
- **Flatpickr**: Date/time picker widgets

## Deployment Strategy

### Development Environment
- SQLite database for local development
- Flask development server with debug mode
- File-based session storage

### Production Environment
- PostgreSQL database with connection pooling
- Gunicorn WSGI server with 4 workers
- ProxyFix middleware for reverse proxy compatibility
- Environment-based configuration management

### Hosting Configuration
- **Modules**: python-3.11, postgresql-16
- **Port Mapping**: Internal 4000 → External 80
- **Process Management**: Parallel workflow execution
- **File Storage**: Static file serving for uploads

## Role-Based Access Control

### User Roles
- **Admin**: Full system access, can approve/decline all events, see all events and dashboard data
- **Event Manager**: Can approve/decline events, see all events and dashboard data, cannot manage users
- **Medical Rep**: Can create events (start in pending status), only see their own events and dashboard data

### Event Status Flow
- **Medical Reps**: Events created in "pending" status, require approval
- **Admin/Event Managers**: Events created directly in "active" status
- **Approval Process**: Admin and Event Managers can approve (active) or decline events
- **Event Visibility**: Medical reps see only their own events, Admin/Event Managers see all events

## Changelog

```
Changelog:
- July 31, 2025. Role-Based Event Approval System Implementation
  - ✅ Implemented role-based access control with admin, event_manager, and medical_rep roles
  - ✅ Medical rep events start in "pending" status and require approval from admin/event manager
  - ✅ Admin and event managers can approve/decline events with proper form handling
  - ✅ Medical reps only see their own events in events page and dashboard
  - ✅ Admin and event managers see all events from all users
  - ✅ Updated dashboard statistics to respect user role visibility
  - ✅ Updated all chart data (categories, monthly, requesters) to show role-appropriate data
  - ✅ Enhanced events template with approval/decline buttons for authorized users
  - ✅ Updated event status badges (pending, active, declined) with proper styling
  - ✅ Added role-based filtering in events page with status filter for admins/managers
- July 31, 2025. Migration and Enhancement Completion
  - ✅ Successfully migrated application from Replit Agent to standard Replit environment
  - ✅ Fixed JavaScript syntax errors in dashboard.js causing browser console warnings
  - ✅ Made Full Name field optional in bulk user upload functionality
  - ✅ Updated bulk user upload template to show only required columns: Email, Role, Password
  - ✅ Added optional image upload feature to event creation with proper validation
  - ✅ Enhanced events page button layout with grouped Edit/Delete actions
  - ✅ Added comprehensive event details page with complete event information display
  - ✅ Fixed event viewing and editing functionality with proper route handling and POST method support
  - ✅ Fixed dashboard API endpoints to show real data instead of hardcoded zeros
  - ✅ Enhanced dashboard chart initialization with better error handling
  - ✅ Fixed dashboard charts to fetch real data from API endpoints instead of hardcoded fallback data
  - ✅ Updated application to run on port 5000 for standard Replit environment
  - ✅ Implemented proper PostgreSQL database integration with fallback support
  - ✅ Fixed all LSP diagnostics for improved code quality and performance
- July 30, 2025. Event Creation System Fixed & UI Enhanced
  - ✅ Fixed database schema issues causing event creation failures
  - ✅ Added missing venue_name column to Event model for proper form handling
  - ✅ Styled event creation form to match attendees list design with enhanced UI
  - ✅ Removed description field below event title per user request
  - ✅ Made attendees list upload prominently featured with professional styling
  - ✅ Fixed all LSP diagnostics errors for improved code quality
  - ✅ Consolidated event creation form layout for better user experience
  - ✅ Enhanced file upload sections with clear validation and templates

- July 30, 2025. Comprehensive Code Review & Critical Fixes
  - ✅ Created missing event_categories table in PostgreSQL database
  - ✅ Fixed SQL parameter binding syntax (changed %% to : for PostgreSQL compatibility)
  - ✅ Added Password column to bulk user upload Excel template with validation
  - ✅ Optimized bulk user processing to handle 1000+ users efficiently:
    → Implemented batch processing (50 users per batch) to prevent timeouts
    → Pre-validates all data before database operations
    → Eliminates individual queries for existing email checks
    → Uses proper transaction management with batch commits
  - ✅ Fixed all LSP diagnostics including pandas data type issues
  - ✅ Changed category selection from multiple checkboxes to single dropdown
  - ✅ Improved database connection stability with proper pool settings
  - ✅ Created default admin user (admin@test.com / admin123) for testing
  - ✅ Auto-populated event categories and types during initialization
  - ✅ Fixed Egyptian governorates reference errors throughout codebase
  - ✅ Enhanced Excel file generation with proper pandas ExcelWriter usage
  - ✅ Implemented comprehensive error handling and logging

- July 29, 2025. Event Creation & Management Implementation
  - Fixed "Method Not Allowed" error by adding POST method support to create_event route
  - Implemented complete event creation functionality with database persistence
  - Added proper form validation and error handling for event creation
  - Integrated event creation with existing event table schema (name, description, type, categories, dates, online/offline)
  - Enhanced events page to display real events from database instead of empty placeholder
  - Added support for event-category associations and proper datetime handling
  - Added all 27 Egyptian governorates to venue selection dropdown
  - Implemented attendees file upload functionality with CSV/Excel support
  - Added downloadable CSV template for attendees with proper medical professional format

- July 29, 2025. Medical Event Categories & Types Implementation
  - Added 11 medical speciality and pharmaceutical event categories to database
  - Categories include: Cardiology, Oncology, Neurology, Pediatrics, Endocrinology, Dermatology, Psychiatry, Product Launch, Medical Education, Patient Awareness, Internal Training
  - Added 6 professional event types: Conference, Webinar, Workshop, Symposium, Roundtable Meeting, Investigator Meeting
  - Updated all relevant routes to fetch real categories and event types from database instead of placeholder data
  - Enhanced events, create_event, and settings pages with authentic data

- July 29, 2025. JavaScript API Integration & Settings Functionality Implementation
  - Fixed all API endpoint mismatches between frontend JavaScript and backend routes
  - Added proper session authentication with credentials: 'same-origin' to all fetch requests
  - Implemented real form data processing instead of hardcoded placeholder responses
  - Enhanced error handling in JavaScript to properly parse server responses
  - Added comprehensive API endpoints for settings, categories, event types, and user management
  - Resolved settings persistence issues by providing proper template data
  - Added authentication debugging and better error messages for API calls

- July 29, 2025. SQLAlchemy Registry Issue Investigation & Resolution Attempt
  - Identified critical "Class already has a primary mapper defined" error
  - Traced root cause to SQLAlchemy registry persistence beyond circular imports
  - Successfully resolved by creating simplified single-file application structure
  - Application now running stably with SQLite database
  
- June 30, 2025. Fixed application startup issues
  - Removed dotenv dependency causing import errors
  - Fixed Chart.js loading timing issues on dashboard
  - Fixed create_event template missing edit_mode variable
  - Enhanced user dropdown menu positioning and responsiveness
  - Added viewport boundary constraints for dropdown menus
  - Improved mobile device compatibility for navigation
  
- June 14, 2025. Initial setup
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```