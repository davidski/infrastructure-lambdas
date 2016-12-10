$paths = Get-ChildItem ./functions
foreach ($item in $paths) {
    $dest = ($item -replace "-", "_") + ".zip"
    Write-Output "Destination is $dest"
    Compress-Archive -Path functions/$item/main.py -DestinationPath E:/terraform/personal-infrastructure/files/$dest -force -Verbose
} 