param([string]$BaseUrl = "http://localhost:8000")
Invoke-RestMethod -Method Post -Uri "$BaseUrl/knowledge/reindex" | ConvertTo-Json

