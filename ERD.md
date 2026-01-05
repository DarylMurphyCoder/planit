ment# PlanIt! Entity Relationship Diagram (ERD)

## Database Schema Overview

```
┌──────────────────────┐
│       USER           │
├──────────────────────┤
│ id (PK)              │
│ username             │
│ email                │
│ password             │
│ created_at           │
│ updated_at           │
└──────────────────────┘
         │
         ├─────────────────────────────────────────┐
         │                                         │
         │ 1:1                                     │ 1:N
         │                                         │
         ↓                                         ↓
┌──────────────────────┐              ┌──────────────────────┐
│    USER PROFILE      │              │      CATEGORY        │
├──────────────────────┤              ├──────────────────────┤
│ id (PK)              │              │ id (PK)              │
│ user_id (FK)         │              │ user_id (FK)         │
│ email_notifications  │              │ name                 │
│ theme_preference     │              │ created_at           │
│ created_at           │              │ updated_at           │
│ updated_at           │              └──────────────────────┘
└──────────────────────┘                       ▲
                                               │ 1:N
         ┌────────────────────────────────────┤
         │                                    │
         │ 1:N                                │
         ↓                                    │
┌──────────────────────┐                      │
│       TASK           │                      │
├──────────────────────┤                      │
│ id (PK)              │                      │
│ user_id (FK)         │                      │
│ title                │                      │
│ description          │◄──────────────────────┘
│ is_completed         │
│ priority             │
│ due_date             │
│ category_id (FK)     │
│ created_at           │
│ updated_at           │
└──────────────────────┘
         │
    ┌────┼──────────────────────────┐
    │    │                          │
    │    │ 1:N                      │ 1:1
    │    │                          │
    ↓    ↓                          ↓
 ┌──────────────────┐    ┌──────────────────────┐
 │   TASK_NOTE      │    │ RECURRING_TASK       │
 ├──────────────────┤    ├──────────────────────┤
 │ id (PK)          │    │ id (PK)              │
 │ task_id (FK)     │    │ task_id (FK)         │
 │ content          │    │ frequency            │
 │ created_at       │    │ end_date             │
 │ updated_at       │    │ created_at           │
 └──────────────────┘    │ updated_at           │
                         └──────────────────────┘

┌──────────────────────────────────┐
│   SHARED_TASK_LIST               │
├──────────────────────────────────┤
│ id (PK)                          │
│ task_id (FK) ──────────┐         │
│ shared_with_user (FK)  │         │
│ permission_level       │         │
│ created_at             │         │
└──────────────────────────────────┘
         ▲                  ▲
         │                  │
         └──────────────────┘
         Both reference User
```

---

## Django Models Structure

### 1. **User Model** (Django Built-in)
| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | AutoField | Primary Key | Django auto-generated |
| username | CharField | Unique, Max 150 | For login |
| email | EmailField | Unique | For notifications |
| password | CharField | Hashed | Django handles hashing |
| is_active | BooleanField | Default=True | Account status |
| is_staff | BooleanField | Default=False | Admin status |
| date_joined | DateTimeField | auto_now_add | Registration timestamp |

---

### 2. **UserProfile Model** (Extended User)
| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | AutoField | Primary Key | Django auto-generated |
| user | OneToOneField | User, on_delete=CASCADE | User extension |
| email_notifications_enabled | BooleanField | Default=True | Notification preference |
| theme_preference | CharField | Choices (light/dark), Default=light | UI theme |
| created_at | DateTimeField | auto_now_add | Timestamp on creation |
| updated_at | DateTimeField | auto_now | Timestamp on update |

---

### 3. **Category Model**
| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | AutoField | Primary Key | Django auto-generated |
| user | ForeignKey | User, on_delete=CASCADE | Links to task owner |
| name | CharField | Max 100 | Category name (Work, Personal, etc.) |
| created_at | DateTimeField | auto_now_add | Timestamp on creation |
| updated_at | DateTimeField | auto_now | Timestamp on update |

---

### 4. **Task Model** (Core Entity)
| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | AutoField | Primary Key | Django auto-generated |
| user | ForeignKey | User, on_delete=CASCADE | Task owner |
| title | CharField | Max 255 | Task title (required) |
| description | TextField | Blank=True, Null=True | Detailed description |
| is_completed | BooleanField | Default=False | Completion status |
| priority | CharField | Choices (low/medium/high), Default=medium | Task priority |
| due_date | DateField | Blank=True, Null=True | Optional deadline |
| category | ForeignKey | Category, Blank=True, Null=True, on_delete=SET_NULL | Task organization |
| created_at | DateTimeField | auto_now_add | Timestamp on creation |
| updated_at | DateTimeField | auto_now | Timestamp on update |

---

### 5. **TaskNote Model**
| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | AutoField | Primary Key | Django auto-generated |
| task | ForeignKey | Task, on_delete=CASCADE | Parent task |
| content | TextField | | Detailed notes/context |
| created_at | DateTimeField | auto_now_add | Timestamp on creation |
| updated_at | DateTimeField | auto_now | Timestamp on update |

---

### 6. **RecurringTask Model**
| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | AutoField | Primary Key | Django auto-generated |
| task | OneToOneField | Task, on_delete=CASCADE | Parent task |
| frequency | CharField | Choices (daily/weekly/monthly/yearly) | Recurrence pattern |
| end_date | DateField | Blank=True, Null=True | Optional end date |
| created_at | DateTimeField | auto_now_add | Timestamp on creation |
| updated_at | DateTimeField | auto_now | Timestamp on update |

---

### 7. **SharedTaskList Model** (For Collaboration)
| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | AutoField | Primary Key | Django auto-generated |
| task | ForeignKey | Task, on_delete=CASCADE | Task being shared |
| shared_with_user | ForeignKey | User, on_delete=CASCADE | User receiving access |
| permission_level | CharField | Choices (view_only/editable), Default=view_only | Access level |
| created_at | DateTimeField | auto_now_add | Timestamp on creation |
| task | ForeignKey | Task, on_delete=CASCADE | Related task |
| notification_type | CharField | Choices (due_soon/overdue/shared) | Notification reason |
| sent_at | DateTimeField | | When notification was sent |
| created_at | DateTimeField | auto_now_add | Record creation time |

---

## Relationships Summary

| From | To | Cardinality | Type | Notes |
|------|----|----|------|-------|
| User | Task | 1:N | One-to-Many | A user has many tasks |
| User | Category | 1:N | One-to-Many | A user has many categories |
| User | Notification | 1:N | One-to-Many | A user receives many notifications |
| Category | Task | 1:N | One-to-Many | A category has many tasks |
| Task | TaskNote | 1:N | One-to-Many | A task has many notes |
| Task | RecurringTask | 1:1 | One-to-One | A task can have one recurrence pattern |
| Task | SharedTaskList | 1:N | One-to-Many | A task can be shared with many users |
| User | SharedTaskList | 1:N | One-to-Many | A user can have many shared tasks |
| Task | Notification | 1:N | One-to-Many | A task can generate many notifications |

---

## Key Design Decisions

1. **User Model**: Using Django's built-in User model for authentication and authorization
2. **Cascade Delete**: Most ForeignKeys use CASCADE to maintain data integrity
3. **Soft Delete Not Needed**: Simple deletion is sufficient for MVP
4. **Timestamps**: All models include created_at and updated_at for tracking
5. **Nullable Fields**: Optional fields (notes, due_date, category) allow flexibility
6. **Permission Model**: Simple view_only vs editable for shared tasks
7. **Notification Tracking**: Separate model to track sent notifications and avoid duplicates

---

## Future Considerations

- Add `is_deleted` soft-delete flag for archived tasks
- Add `reminder_settings` model for granular notification preferences
- Add `task_history` model for audit trail of changes
- Add `tag` model for more flexible task organization (many-to-many with Task)
- Add `team` model for group-level task sharing
