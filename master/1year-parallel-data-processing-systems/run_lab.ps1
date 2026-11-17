param (
    [Parameter(Mandatory=$true, Position=0)]
    [int]$Lab,
    [int]$Cores = 4
)

$exePath = ".\.build\lab-$Lab\Release\mpi_app_$Lab.exe"

if (-not (Test-Path -Path $exePath -PathType Leaf)) {
    Write-Host "Исполняемый файл не найден! Выполните сборку соответствующей работы перед запуском." -ForegroundColor Red
    exit 1
}

Write-Host "Исполняемый файл: $exePath" -ForegroundColor Cyan
Write-Host "Запуск лабораторной работы №$Lab на $Cores процессах..." -ForegroundColor Cyan

mpiexec -n $Cores $exePath

if ($LASTEXITCODE -eq 0) {
    Write-Host "Программа завершилась успешно." -ForegroundColor Green
} else {
    Write-Host "Программа завершилась с ошибкой (код: $LASTEXITCODE)" -ForegroundColor Red
}
