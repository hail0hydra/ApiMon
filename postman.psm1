# ----------------------------------------------
#
# Author:       s1ck
# Description:  Simple POSTMAN emulator
# Date:         11 July 2026
#
# ----------------------------------------------








# ----=={{[[[     HOW TO      ]]]}}==----
#
# USAGE:
#
#
#   1. use "Import-Module ./postman.psm1"  to import all fuctions here into your local powershell session
#
#
#   2. to get a list of all imported function use:
#
#   ```powershell
#       Get-Command -Module postman 
#   ```
#
#   3. To unload just "Remove-Module -Name postman"



# root
function Get-Root {
    curl -s http://localhost:8000/ -X GET | jq
}



# posts
function Get-Posts {
    curl -s http://localhost:8000/posts -X GET -L | jq
}

function Get-PostsById ($id) {
    if ($id -gt 0){

        curl -s http://localhost:8000/posts/$id -X GET | jq

    }
    else {
        Write-Host "pass ID in argv"
    }
}

function Create-Post ($token) {


    $guid = (New-Guid).Guid

        $payload = @{
            title = "powershell script $guid"
                content = "posted by powershell $guid"
        } | ConvertTo-Json -Compress

    if ($null -eq $token) {
        Write-Host "enter access token with: -token"
            return
    } else {

        curl -s http://localhost:8000/posts -X POST -H "Content-Type: application/json" -H "Authorization: bearer $token" -d $payload -L | jq
    }

}

function Delete-Post ($id) {
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
function Get-UserById ($id) {
    if ($id -gt 0){

        curl -s http://localhost:8000/users/$id -X GET | jq

    }
    else {
        Write-Host "pass ID in argv"
    }

}

function Create-User ($user, $passwd) {

# $guid = (New-Guid).Guid
# $payload = @{
#     email = "$guid@powershell.ps1.net"
#         password = "P0w3r==$guid==Sh3ll"
# } | ConvertTo-Json -Compress

    $payload = @{
        email = "$user"
            password = "$passwd"
    } | ConvertTo-Json -Compress


    if ($null -eq $user){
        Write-Host "enter username with:  -user"
            return
    } elseif ($null -eq $passwd) {
        Write-Host "enter password with:  -passwd"
    } else {
        curl -s http://localhost:8000/users -X POST -H "Content-Type: application/json" -d $payload -L | jq
    }

}

# auth

function Login-User ($user, $passwd) {

# $payload = @{
#     email = "$user"
#         password = "$passwd"
# } | ConvertTo-Json -Compress
#
    $payload = "username=$user&password=$passwd"

        if ($null -eq $user){
            Write-Host "enter username with:  -user"
                return
        } elseif ($null -eq $passwd) {
            Write-Host "enter password with:  -passwd"
        } else {

            curl -s http://localhost:8000/login -X POST -H "Content-Type: application/x-www-form-urlencoded" -d $payload -L | jq
        }

}

# Get-Root (was calling this to hit / by default on every load)
