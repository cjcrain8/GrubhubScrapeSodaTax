for /f %%x in ('wmic path win32_localtime get /format:list ^| findstr "="') do set %%x
set today=%Month%.%Day%.%Year%

echo %today%


schtasks /create /sc once /ri 5 /tn "GrubhubSodaTax"  /st 12:00 /tr "D:\Grubhub_SodaTax_Grubhub_Scrapes\start_direct.cmd co_plus %today%
