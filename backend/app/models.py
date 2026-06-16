import enum
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum, func
)
from sqlalchemy.orm import relationship
from app.database import Base

# ==============================================================================
# 0. SCHEMA ENUM DEFINITIONS
# ==============================================================================

class TicketPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class TicketStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    on_hold = "on_hold"
    resolved = "resolved"
    closed = "closed"

class CommentAuthor(str, enum.Enum):
    department = "department"
    it_admin = "it_admin"

class NotificationRecipient(str, enum.Enum):
    department = "department"
    it_admin = "it_admin"

class NotificationType(str, enum.Enum):
    ticket_received = "ticket_received"
    status_updated = "status_updated"
    ticket_resolved = "ticket_resolved"
    overdue_alert = "overdue_alert"

class NotificationChannel(str, enum.Enum):
    sms = "sms"
    in_app = "in_app"

class DeliveryStatus(str, enum.Enum):
    pending = "pending"
    sent = "sent"
    failed = "failed"


# ==============================================================================
# 1. CORE APPLICATION MODELS
# ==============================================================================

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    dept_code = Column(String(20), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    tickets = relationship("Ticket", back_populates="department")
    comments = relationship("TicketComment", back_populates="department")
    notifications = relationship("Notification", back_populates="department")
    kb_search_logs = relationship("KbSearchLog", back_populates="department")


class ItAdmin(Base):
    __tablename__ = "it_admin"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # Relationships
    tickets = relationship("Ticket", back_populates="category")
    kb_articles = relationship("KbArticle", back_populates="category")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_number = Column(String(20), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    
    priority = Column(Enum(TicketPriority, name="ticket_priority"), nullable=False, default=TicketPriority.medium)
    status = Column(Enum(TicketStatus, name="ticket_status"), nullable=False, default=TicketStatus.open)
    
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    due_date = Column(DateTime, nullable=True)
    is_overdue = Column(Boolean, nullable=False, default=False)
    resolved_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    department = relationship("Department", back_populates="tickets")
    category = relationship("Category", back_populates="tickets")
    attachments = relationship("TicketAttachment", back_populates="ticket", cascade="all, delete-orphan")
    comments = relationship("TicketComment", back_populates="ticket", cascade="all, delete-orphan")
    status_history = relationship("TicketStatusHistory", back_populates="ticket", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="ticket", cascade="all, delete-orphan")


class TicketAttachment(Base):
    __tablename__ = "ticket_attachments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    file_url = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=True)
    file_type = Column(String(50), nullable=True)
    uploaded_at = Column(DateTime, nullable=False, server_default=func.now())

    # Relationships
    ticket = relationship("Ticket", back_populates="attachments")


class TicketComment(Base):
    __tablename__ = "ticket_comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    author = Column(Enum(CommentAuthor, name="comment_author"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    comment = Column(Text, nullable=False)
    is_internal = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # Relationships
    ticket = relationship("Ticket", back_populates="comments")
    department = relationship("Department", back_populates="comments")


class TicketStatusHistory(Base):
    __tablename__ = "ticket_status_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    old_status = Column(Enum(TicketStatus, name="ticket_status", inherit_schema=True), nullable=True)
    new_status = Column(Enum(TicketStatus, name="ticket_status", inherit_schema=True), nullable=False)
    note = Column(Text, nullable=True)
    changed_at = Column(DateTime, nullable=False, server_default=func.now())

    # Relationships
    ticket = relationship("Ticket", back_populates="status_history")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    recipient = Column(Enum(NotificationRecipient, name="notification_recipient"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    type = Column(Enum(NotificationType, name="notification_type"), nullable=False)
    channel = Column(Enum(NotificationChannel, name="notification_channel"), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(Enum(DeliveryStatus, name="delivery_status"), nullable=False, default=DeliveryStatus.pending)
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # Relationships
    ticket = relationship("Ticket", back_populates="notifications")
    department = relationship("Department", back_populates="notifications")


class KbArticle(Base):
    __tablename__ = "kb_articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    is_published = Column(Boolean, nullable=False, default=False)
    view_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    category = relationship("Category", back_populates="kb_articles")


class KbSearchLog(Base):
    __tablename__ = "kb_search_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    search_query = Column(String(500), nullable=False)
    results_found = Column(Integer, nullable=False, default=0)
    led_to_ticket = Column(Boolean, nullable=False, default=False)
    searched_at = Column(DateTime, nullable=False, server_default=func.now())

    # Relationships
    department = relationship("Department", back_populates="kb_search_logs")


class SlaPolicy(Base):
    __tablename__ = "sla_policies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    priority = Column(Enum(TicketPriority, name="ticket_priority", inherit_schema=True), unique=True, nullable=False)
    response_time_hours = Column(Integer, nullable=False)
    resolution_time_hours = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
