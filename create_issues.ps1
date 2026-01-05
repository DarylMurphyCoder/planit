$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

$issues = @(
    @{Title="Create Tasks"; Label="must-have"; Body=@"
As a user, I want to create a new to-do item with a title so that I can add tasks to my list.

Acceptance Criteria:
- [ ] User can fill out a form with a task title
- [ ] User can submit the form to create a new task
- [ ] The task is saved to the database
- [ ] A success message appears after creation
- [ ] The new task appears in the task list immediately
"@},
    @{Title="View Tasks"; Label="must-have"; Body=@"
As a user, I want to see all my to-do items so that I can track what needs to be done.

Acceptance Criteria:
- [ ] User dashboard displays all tasks for the logged-in user
- [ ] Tasks are displayed in a clear, readable list format
- [ ] Each task shows its title and key information
- [ ] The list updates without requiring a page refresh
- [ ] Empty state message appears when there are no tasks
"@},
    @{Title="Update Tasks"; Label="must-have"; Body=@"
As a user, I want to edit task titles and descriptions so that I can modify tasks if needed.

Acceptance Criteria:
- [ ] User can click an edit button on any task
- [ ] An edit form appears with the current task information
- [ ] User can modify the title and/or description
- [ ] Changes are saved to the database
- [ ] The updated task is reflected in the task list immediately
- [ ] A confirmation message appears after update
"@},
    @{Title="Delete Tasks"; Label="must-have"; Body=@"
As a user, I want to remove completed or unwanted tasks so that I can keep my list clean.

Acceptance Criteria:
- [ ] User can click a delete button on any task
- [ ] A confirmation dialog appears before deletion
- [ ] User can confirm or cancel the deletion
- [ ] Task is removed from the database upon confirmation
- [ ] Task disappears from the list immediately
- [ ] A confirmation message appears after deletion
"@},
    @{Title="User Authentication"; Label="must-have"; Body=@"
As a user, I want to create an account and log in so that my tasks are private and persistent.

Acceptance Criteria:
- [ ] User can access a registration/signup page
- [ ] User can create an account with username and password
- [ ] Password is securely hashed and stored
- [ ] User receives validation feedback for form fields
- [ ] User can log in with correct credentials
- [ ] Login fails with invalid credentials
- [ ] User session persists across page refreshes
- [ ] User can log out successfully
- [ ] Only authenticated users can access the task dashboard
"@},
    @{Title="Basic UI"; Label="must-have"; Body=@"
As a user, I want a simple, intuitive interface so that I can easily manage my tasks.

Acceptance Criteria:
- [ ] The interface uses a clean, uncluttered design
- [ ] Navigation is intuitive and easy to understand
- [ ] All action buttons are clearly labeled
- [ ] The layout is responsive and works on different screen sizes
- [ ] Color scheme is consistent throughout the app
- [ ] Typography is readable with appropriate font sizes
- [ ] No confusing or duplicate functionality exists
"@},
    @{Title="Mark Tasks Complete"; Label="should-have"; Body=@"
As a user, I want to mark tasks as complete/incomplete so that I can track progress.

Acceptance Criteria:
- [ ] User can click a checkbox to mark a task as complete
- [ ] Complete tasks are visually distinguished (strikethrough or different styling)
- [ ] User can uncheck the box to mark a task as incomplete
- [ ] Status changes are saved to the database immediately
- [ ] Completed tasks remain in the list unless filtered out
"@},
    @{Title="Task Due Dates"; Label="should-have"; Body=@"
As a user, I want to set due dates on tasks so that I know deadlines.

Acceptance Criteria:
- [ ] User can add a due date when creating a task
- [ ] User can edit a task's due date
- [ ] A date picker is provided for easy selection
- [ ] Due dates are displayed on tasks in the list
- [ ] Tasks overdue are highlighted or visually flagged
- [ ] Due date is stored and persisted in the database
"@},
    @{Title="Task Categories"; Label="should-have"; Body=@"
As a user, I want to organize tasks into categories so that I can group related items.

Acceptance Criteria:
- [ ] User can create new categories
- [ ] User can assign a category when creating a task
- [ ] User can assign/change a category for existing tasks
- [ ] Tasks are grouped by category in the list view
- [ ] Categories are displayed with tasks
- [ ] User can delete unused categories
- [ ] Categories are stored in the database
"@},
    @{Title="Search/Filter Tasks"; Label="should-have"; Body=@"
As a user, I want to search or filter tasks by status or category so that I can find specific items quickly.

Acceptance Criteria:
- [ ] User can type in a search box to find tasks by title
- [ ] Search results filter in real-time as user types
- [ ] User can filter tasks by completion status (complete/incomplete)
- [ ] User can filter tasks by category
- [ ] Multiple filters can be applied simultaneously
- [ ] A clear filters button returns to the full task list
- [ ] Results are displayed without page reload
"@},
    @{Title="Task Priority Levels"; Label="should-have"; Body=@"
As a user, I want to set priority levels (high, medium, low) so that I focus on important tasks first.

Acceptance Criteria:
- [ ] User can select a priority level (High, Medium, Low) when creating a task
- [ ] User can change priority for existing tasks
- [ ] Priority is displayed on each task in the list
- [ ] Tasks can be sorted by priority
- [ ] High priority tasks are visually highlighted
- [ ] Priority is stored in the database
- [ ] A default priority (Medium) is assigned if not specified
"@},
    @{Title="Task Notes"; Label="could-have"; Body=@"
As a user, I want to add detailed notes to tasks so that I can include additional context.

Acceptance Criteria:
- [ ] User can add notes when creating a task
- [ ] User can edit task notes for existing tasks
- [ ] A text editor is provided for note entry
- [ ] Notes are displayed in a task detail view
- [ ] Notes support basic formatting (bold, italic, lists)
- [ ] Notes are stored in the database
- [ ] Notes are optional (tasks can exist without notes)
"@},
    @{Title="Recurring Tasks"; Label="could-have"; Body=@"
As a user, I want to set tasks to repeat daily/weekly/monthly so that I don't have to recreate them.

Acceptance Criteria:
- [ ] User can select a recurrence option (Daily, Weekly, Monthly, Yearly)
- [ ] User can set an end date for recurring tasks
- [ ] Recurring tasks automatically create new instances at the specified interval
- [ ] User can edit all instances or just one instance of a recurring task
- [ ] Completed instances don't prevent new instances from being created
- [ ] Recurrence settings are stored in the database
"@},
    @{Title="Task Sharing"; Label="could-have"; Body=@"
As a user, I want to share task lists with others so that we can collaborate.

Acceptance Criteria:
- [ ] User can invite other users to view/edit their task lists
- [ ] Shared lists can be set to view-only or editable
- [ ] Shared users receive notifications of invitations
- [ ] User can revoke access to shared lists at any time
- [ ] Shared changes are reflected in real-time for all users
- [ ] A list of shared users is displayed for each list
- [ ] Original owner retains full control over shared lists
"@},
    @{Title="Dark Mode"; Label="could-have"; Body=@"
As a user, I want a dark theme option so that I can reduce eye strain.

Acceptance Criteria:
- [ ] User can toggle dark mode on/off in settings
- [ ] Dark mode applies to all pages and components
- [ ] Color contrast meets accessibility standards (WCAG AA)
- [ ] User's theme preference is saved and persists across sessions
- [ ] Theme preference syncs across user's devices
- [ ] System theme preference is detected and auto-applied on first visit
- [ ] Both light and dark themes are fully functional
"@},
    @{Title="Email Notifications"; Label="could-have"; Body=@"
As a user, I want to receive email reminders about tasks so that I don't miss deadlines.

Acceptance Criteria:
- [ ] User can enable/disable email notifications
- [ ] User can set reminder timing (e.g., 1 day before due)
- [ ] Emails include task title and due date
- [ ] Emails send reliably and only once per reminder
- [ ] Notifications respect user time zone
- [ ] Email delivery is logged for troubleshooting
"@}
)

foreach ($issue in $issues) {
    Write-Host "Creating issue: $($issue.Title)"
    gh issue create --title $issue.Title --label $issue.Label --body $issue.Body
}

Write-Host "All issues created successfully!"
