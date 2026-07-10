param (
        [string]$Test,
        [int]$id
      )

# root
    function Get-Root {
        curl -s http://localhost:8000/ -X GET | jq
    }



# posts
function Get-Posts {
    curl -s http://localhost:8000/posts -X GET | jq
}

function Get-PostsById {
    if ($id -gt 0){

        curl -s http://localhost:8000/posts/$id -X GET | jq

    }
    else {
        Write-Host "pass ID in argv"
    }
}

function Create-Post {

    $guid = (New-Guid).Guid

        $payload = @{
            title = "powershell script $guid"
                content = "posted by powershell $guid"
        } | ConvertTo-Json -Compress

    curl -s http://localhost:8000/posts -X POST -H "Content-Type: application/json" -d $payload | jq
}

function Delete-Post {
    if ($id -gt 0){

        curl -s http://localhost:8000/posts/$id -X DELETE -i

    }
    else {
        Write-Host "pass ID in argv"
    }
}

function Update-Post {

    $guid = (New-Guid).Guid

    $payload = @{
        title = "powershell script $guid"
            content = "posted by powershell $guid"
    } | ConvertTo-Json -Compress

    curl -s http://localhost:8000/posts/20 -X PUT -H "Content-Type: application/json" -d $payload | jq

}


# users
function Get-UserById {
    if ($id -gt 0){

        curl -s http://localhost:8000/users/$id -X GET | jq

    }
    else {
        Write-Host "pass ID in argv"
    }

}

function Create-User {
    $guid = (New-Guid).Guid

        $payload = @{
            email = "$guid@powershell.ps1.net"
                password = "P0w3r==$guid==Sh3ll"
        } | ConvertTo-Json -Compress

    curl -s http://localhost:8000/users -X POST -H "Content-Type: application/json" -d $payload | jq

}


switch ($Test) {
    "gp" { Get-Posts }
    "gpi" { Get-PostsById }
    "gui" { Get-UserById }
    "cp" { Create-Post }
    "cu" { Create-User }
    "dp" { Delete-Post }
    "up" { Update-Post }
    default { Get-Root }
}
