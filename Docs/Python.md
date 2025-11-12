
# PowerShell (recomendado no Windows — copia, concatena e zipa):
$source = "C:\Users\nicol\source\repos\roncato\Controle-Roncatin"
$dest   = "C:\Users\nicol\source\repos\roncato"
Remove-Item -Path $dest -Recurse -Force -ErrorAction SilentlyContinue
New-Item -Path $dest -ItemType Directory | Out-Null
Copy-Item -Path (Join-Path $source "Layout") -Recurse -Destination $dest -Force -ErrorAction SilentlyContinue
Copy-Item -Path (Join-Path $source "Pages")  -Recurse -Destination $dest -Force -ErrorAction SilentlyContinue
Copy-Item -Path (Join-Path $source "Imports.razor") -Destination $dest -Force -ErrorAction SilentlyContinue
Copy-Item -Path (Join-Path $source "Routes.razor")  -Destination $dest -Force -ErrorAction SilentlyContinue
$combined = Join-Path $dest "all_files_combined.txt"
Get-ChildItem -Path $dest -Recurse -File | Sort-Object FullName | ForEach-Object {
    "`n---- $($_.FullName) ----`n" | Out-File -FilePath $combined -Encoding utf8 -Append
    Get-Content -Raw -Path $_.FullName | Out-File -FilePath $combined -Encoding utf8 -Append
}

$zip = Join-Path $env:USERPROFILE "Desktop\project_extract.zip"
Compress-Archive -Path (Join-Path $dest "*") -DestinationPath $zip -Force
Write-Output "Extraído em: $dest`nZip: $zip`nArquivo combinado: $combined"

# Python (cross-platform, cria pasta de saída e zip):


import os, shutil, zipfile

SOURCE = r"C:\Users\nicol\source\repos\roncato\Controle-Roncatin"
DEST   = r"C:\Users\nicol\source\repos\roncato"

#limpaerecria
if os.path.exists(DEST):
    shutil.rmtree(DEST)
os.makedirs(DEST, exist_ok=True)
items = ["Layout", "Pages", "Imports.razor", "Routes.razor"]
for it in items:
    src = os.path.join(SOURCE, it)
    if os.path.isdir(src):
        shutil.copytree(src, os.path.join(DEST, it))
    elif os.path.isfile(src):
        shutil.copy2(src, DEST)


combined = os.path.join(DEST, "all_files_combined.txt")
with open(combined, "w", encoding="utf-8") as out:
    for root, _, files in os.walk(DEST):
        for f in sorted(files):
            path = os.path.join(root, f)
            out.write(f"\n---- {path} ----\n")
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as fh:
                    out.write(fh.read())
            except Exception as e:
                out.write(f"[erro lendo {path}: {e}]\n")
    
zip_path = os.path.join(os.path.expanduser("~"), "Desktop", "project_extract")
shutil.make_archive(zip_path, 'zip', DEST)
print("Extraído em:", DEST)
print("Combined:", combined)
print("Zip:", zip_path + ".zip")