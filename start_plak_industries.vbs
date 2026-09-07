Option Explicit

Dim shell, files, project, python, command
Set shell = CreateObject("WScript.Shell")
Set files = CreateObject("Scripting.FileSystemObject")
project = files.GetParentFolderName(WScript.ScriptFullName)

If files.FileExists(project & "\.venv\Scripts\pythonw.exe") Then
    python = project & "\.venv\Scripts\pythonw.exe"
    command = """" & python & """ """ & project & "\run.py"""
Else
    command = "pyw.exe """ & project & "\run.py"""
End If

shell.Run command, 0, False
WScript.Sleep 4500
shell.Run "http://127.0.0.1:5000/", 1, False
