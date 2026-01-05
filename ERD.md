# PlanIt! Entity Relationship Diagram (ERD)

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
         │ 1:N
         │
    ┌────┴─────────────────────────────────────────┐
    │                                              │
    │                                              │
    ↓                                              ↓
┌──────────────────────┐                  ┌──────────────────────┐
│      CATEGORY        │                  │       TASK           │
├──────────────────────┤                  ├──────────────────────┤
│ id (PK)              │◄──────1:N────────│ id (PK)              │
│ user_id (FK)         │                  │ user_id (FK)         │
│ name                 │                  │ title                │
│ created_at           │                  │ description          │
│ updated_at           │                  │ is_completed         │
└──────────────────────┘                  │ priority             │
                                          │ due_date             │
                                          │ category_id (FK)     │
                                          │ created_at           │
                                          │ updated_at           │
                                          └──────────────────────┘
                                                   │
                                  ┌────────────────┼─────────────────┐
                                  │                │                 │
                                  ↓                ↓                 ↓
                          ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
                          │    TASK_NOTE     │ │ RECURRING_TASK   │ │ SHARED_TASK_LIST │
                          ├──────────────────┤ ├──────────────────┤ ├──────────────────┤
                          │ id (PK)          │ │ id (PK)          │ │ id (PK)          │
                          │ task_id (FK)     │ │ task_id (FK)     │ │ task_id (FK)     │
                          │ content          │ │ frequency        │ │ shared_with_user │
                          │ created_at       │ │ end_date         │ │ permission_level │
                          │ updated_at       │ │ created_at       │ │ created_at       │
                          └──────────────────┘ │ updated_at       │ └──────────────────┘
                                              └──────────────────┘         │
                                                                           │ FK
                                                                           ↓
                                                                    ┌──────────────────┐
                                                                    │   USER (shared)  │
                                                                    └──────────────────┘

┌──────────────────────┐
│   NOTIFICATION       │
├──────────────────────┤
│ id (PK)              │
│ user_id (FK)         │
│ task_id (FK)         │
│ notification_type    │
│ sent_at              │
│ created_at           │
└──────────────────────┘
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
| created_at | DateTimeField | auto_now_add | Timestamp on creation |
| updated_at | DateTimeField | auto_now | Timestamp on update |

---

### 2. **Category Model**
| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | AutoField | Primary Key | Django auto-generated |
| user | ForeignKey | User, on_delete=CASCADE | Links to task owner |
| name | CharField | Max 100 | Category name (Work, Personal, etc.) |
| created_at | DateTimeField | auto_now_add | Timestamp on creation |
| updated_at | DateTimeField | auto_now | Timestamp on update |

---

### 3. **Task Model** (Core Entity)
| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | AutoField | Primary Key | Django auto-generated |
| user | ForeignKey | User, on_delete=CASCADE | Task owner |
| title | CharField | Max 255 | Task title (required) |
| description | TextField | Blank=True, Null=True | Detailed description |
| is_completed | BooleanField | Default=False | Completion status |
| priority | CharField | Choices (High/Medium/Low), Default=Medium | Task priority |
| due_date | DateField | Blank=True, Null=True | Optional deadline |
| category | ForeignKey | Category, Blank=True, Null=True, on_delete=SET_NULL | Task organization |
| created_at | DateTimeField | auto_now_add | Timestamp on creation |
| updated_at | DateTimeField | auto_now | Timestamp on update |

---

### 4. **TaskNote Model**
| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | AutoField | Primary Key | Django auto-generated |
| task | ForeignKey | Task, on_delete=CASCADE | Parent task |
| content | TextField | | Detailed notes/context |
| created_at | DateTimeField | auto_now_add | Timestamp on creation |
| updated_at | DateTimeField | auto_now | Timestamp on update |

---

### 5. **RecurringTask Model**
| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | AutoField | Primary Key | Django auto-generated |
| task | ForeignKey | Task, on_delete=CASCADE | Parent task |
| frequency | CharField | Choices (Daily/Weekly/Monthly/Yearly) | Recurrence pattern |
| end_date | DateField | Blank=True, Null=True | Optional end date |
| created_at | DateTimeField | auto_now_add | Timestamp on creation |
| updated_at | DateTimeField | auto_now | Timestamp on update |

---

### 6. **SharedTaskList Model** (For Collaboration)
| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | AutoField | Primary Key | Django auto-generated |
| task | ForeignKey | Task, on_delete=CASCADE | Task being shared |
| shared_with_user | ForeignKey | User, on_delete=CASCADE | User receiving access |
| permission_level | CharField | Choices (view_only/editable), Default=view_only | Access level |
| created_at | DateTimeField | auto_now_add | Timestamp on creation |

---

### 7. **Notification Model** (For Email Reminders)
| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | AutoField | Primary Key | Django auto-generated |
| user | ForeignKey | User, on_delete=CASCADE | Notification recipient |
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
