$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Create GitHub Project (v2)
Write-Host "Creating GitHub Project: PlanIt Kanban..."
$output = gh project create --owner DarylMurphyCoder --title "PlanIt Kanban" --format json
$project = $output | ConvertFrom-Json
$projectNumber = $project.number
Write-Host "Project created with number: $projectNumber"

# Get all issues
Write-Host "Fetching all issues..."
$issues = gh issue list --limit 100 --json number,title | ConvertFrom-Json

# Add issues to project
Write-Host "Adding issues to project..."
foreach ($issue in $issues) {
    Write-Host "Adding issue #$($issue.number): $($issue.title)"
    gh project item-add $projectNumber --owner DarylMurphyCoder --url "https://github.com/DarylMurphyCoder/planit/issues/$($issue.number)" 2>&1 | Out-Null
}

Write-Host "Kanban board created successfully!"
Write-Host "Visit: https://github.com/users/DarylMurphyCoder/projects/$projectNumber"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Go to the project link above"
Write-Host "2. Click Configure table or Add view to create a board view"
Write-Host "3. Add status field with columns: To Do, In Progress, Done"
Write-Host "4. Drag issues between columns as you work"
