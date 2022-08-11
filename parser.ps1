$first_page = 200999935 #Начальная страница для интервала опроса
$last_page = 201000000  #Конечная страница для интервала опроса
$pages_interval = $first_page..$last_page 
$export_filename = $pages_interval[0].ToString() + ".csv"
$base_url = "https://kinescope.io/embed/"
$counter = 1
$list = @()

$pages_interval|%{

    Write-Progress -Activity "Scraping site" -Status "Progress:" -PercentComplete (($_-$pages_interval[0])/($pages_interval[-1]-$pages_interval[0])*100)
    $full_url = $base_url + $_.ToString()
    $full_url
    try {
        $responce = Invoke-WebRequest -uri $full_url -ErrorAction SilentlyContinue
        if ($responce.StatusCode -eq 200)
        {
            
            $json = ConvertFrom-Json -InputObject $responce.Scripts[2].innerHTML
            $webinar_date = $json.uploadDate.ToString()
            $webinar_duration = $json.duration
            if ($json.name -match '\d\d\d\d-\d\d-\d\d')
            {
                $provider = "Netology"
                $splited_json = $json.name.Split("_")
                $course = $splited_json[2] + " " + $splited_json[3]
                $webinare_title = $splited_json[5..$splited_json.Length] -join " "
            }
            elseif ($json.name -match '[\w]-\d{1,2}') 
            {   
                $provider = "Netology"
                $splited_json = (($json.name).Replace("&quot;","")).Split(" ")
                $course = $splited_json[0].Replace(".","")
                $webinare_title = $splited_json[1..$splited_json.Length] -join " "
            }
            elseif ($json.name -match '[\w]_\d{1,2}') 
            {   
                $provider = "Netology"
                $splited_json = (($json.name).Replace("&quot;","")).Split("_")
                $course = $splited_json[0].Replace(".","") + "-"+ $splited_json[1]
                $webinare_title = $splited_json[2..$splited_json.Length] -join " "
            }   
            else
            {
                $provider = "Other"
                $course = "???"
                $webinare_title = $json.name
            }

            # $tmp_array = @($counter, $json.embedUrl, $provider, $webinar_date, $course, $webinare_title, $webinar_duration)
            # $tmp_array -join "`t" 

            $webinars =[pscustomobject]@{
                'counter' = $counter
                'URL' = $json.embedUrl
                'provider' = $provider
                'webinar_date' = $webinar_date
                'course' = $course
                'webinare_title' = $webinare_title
                'webinar_duration' = $webinar_duration
            }


            $webinars| Export-Csv 1.csv -Append  -NoTypeInformation -Encoding UTF8
            # $tmp_array | Export-Csv -Path .\1.csv -Append 
            #$tmp_array -join "`t" >> .\$export_filename
            # $list += ,@($tmp_array)
            $counter +=1
        }  
    }
    catch {}    
}