$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host "Fetching all issues..."
$issues = gh issue list --limit 100 --json number,title | ConvertFrom-Json

$mustHave = @("Create Tasks", "View Tasks", "Update Tasks", "Delete Tasks", "User Authentication", "Basic UI")
$shouldHave = @("Mark Tasks Complete", "Task Due Dates", "Task Categories", "Search/Filter Tasks", "Task Priority Levels")
$couldHave = @("Task Notes", "Recurring Tasks", "Task Sharing", "Dark Mode", "Email Notifications")

$projectNumber = 7
Write-Host "Adding issues to Kanban board..."

foreach ($issue in $issues) {
    $title = $issue.title
    Write-Host "Processing: $title"
    
    if ($mustHave -contains $title) {
        $label = "must-have"
    }
    elseif ($shouldHave -contains $title) {
        $label = "should-have"
    }
    else {
        $label = "could-have"
    }
    
    gh issue edit $issue.number --add-label $label 2>&1 | Out-Null
    gh project item-add $projectNumber --owner DarylMurphyCoder --url "https://github.com/DarylMurphyCoder/planit/issues/$($issue.number)" 2>&1 | Out-Null
    
    Write-Host "  OK with label: $label"
}

Write-Host "Kanban setup complete!"
Write-Host "Board: https://github.com/users/DarylMurphyCoder/projects/7"
