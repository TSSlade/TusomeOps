Option Explicit
'Copied from https://www.extendoffice.com/documents/outlook/1166-outlook-save-all-attachments.html
'Be certain to consult comments
'   https://www.extendoffice.com/documents/outlook/1166-outlook-save-all-attachments.html#comment-2308
'   https://www.extendoffice.com/documents/outlook/1166-outlook-save-all-attachments.html#comment-2572
'   and
'   https://www.extendoffice.com/documents/outlook/1166-outlook-save-all-attachments.html#comment-1709

Public Sub SaveAttachments()
'Update 20170731
    Dim objOL As Outlook.Application
    Dim objMsg As Outlook.MailItem
    Dim objAttachments As Outlook.Attachments
    Dim objSelection As Outlook.Selection
    Dim i As Long
    Dim lngCount As Long
    Dim strFile As String
    Dim strFolderpath As String
    Dim strDeletedFiles As String
    'strFolderpath = CreateObject("WScript.Shell").SpecialFolders(16)
    Set objOL = CreateObject("Outlook.Application")
    Set objSelection = objOL.ActiveExplorer.Selection
    'Update the next line to reflect the path where the documents are going to be staged
    strFolderpath = "C:\Dropbox\Kenya Tusome\Technical\tool development\CLO Consolidation Tool\Observations\"
    For Each objMsg In objSelection
        Set objAttachments = objMsg.Attachments
        lngCount = objAttachments.Count
        strDeletedFiles = ""
'        Use next line to test 
'        MsgBox "Subject = " & objMsg.Subject & " lngCount = " & objAttachments. Count
        If lngCount > 0 Then
            For i = lngCount To 1 Step -1
                strFile = objAttachments.Item(i).FileName
                strFile = strFolderpath & strFile
                objAttachments.Item(i).SaveAsFile strFile
'objAttachments.Item(i).Delete()
'               If objMsg.BodyFormat <> olFormatHTML Then
'                   strDeletedFiles = strDeletedFiles & vbCrLf & "<Error! Hyperlink reference not valid.>"
'               Else
'                   strDeletedFiles = strDeletedFiles & "<br>" & "<a href='file://" & _
'                   strFile & "'>" & strFile & "</a>"
'               End If
                Next i
'               If objMsg.BodyFormat <> olFormatHTML Then
'                   objMsg.Body = vbCrLf & "The file(s) were saved to " & strDeletedFiles & vbCrLf & objMsg.Body
'               Else
'                   objMsg.HTMLBody = "<p>" & "The file(s) were saved to " & strDeletedFiles & "</p>" & objMsg.HTMLBody
'               End If
'               objMsg.Save
            End If
        Next
        ExitSub:
        Set objAttachments = Nothing
        Set objMsg = Nothing
        Set objSelection = Nothing
        Set objOL = Nothing
    End Sub