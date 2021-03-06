Option Explicit
Public FormulaCell As Range
Sub Mail_adv_liq_reminder()
'For mail code examples visit my mail page at:
'http://www.rondebruin.nl/sendmail.htm
    Dim OutApp As Object
    Dim OutMail As Object
    Dim strto As String, strcc As String, strbcc As String
    Dim strsub As String, strbody As String

    Set OutApp = CreateObject("Outlook.Application")
    Set OutMail = OutApp.CreateItem(0)

    strto = Cells(FormulaCell.Row, "C").Value
    strcc = "finance@tusome.rti.org; songele@tusome.rti.org; tslade@rti.org"
    strbcc = ""
    strsub = "Liquidation due for " & Cells(FormulaCell.Row, "B").Value & " Advance"
    strbody = "Hi " & Cells(FormulaCell.Row, "A").Value & vbNewLine & vbNewLine & _
              "Your liquidation of the advance you received on " & Cells(FormulaCell.Row, "D") & " for the " & Cells(FormulaCell.Row, "B").Value & " event ending " & Cells(FormulaCell.Row, "H") & " is now due. Please submit it today." & _
              vbNewLine & vbNewLine & "Thank you!" & _
              vbNewLine & vbNewLine & "~Tusome Operations Team"

    With OutMail
        .To = strto
        .CC = strcc
        .BCC = strbcc
        .Subject = strsub
        .Body = strbody
        'You can add a file to the mail like this
        '.Attachments.Add ("C:\test.txt")
        .Display    ' or use .Send
    End With

    Set OutMail = Nothing
    Set OutApp = Nothing
End Sub

Sub Mail_with_outlook1()
'For mail code examples visit my mail page at:
'http://www.rondebruin.nl/sendmail.htm
    Dim OutApp As Object
    Dim OutMail As Object
    Dim strto As String, strcc As String, strbcc As String
    Dim strsub As String, strbody As String

    Set OutApp = CreateObject("Outlook.Application")
    Set OutMail = OutApp.CreateItem(0)

    strto = "ron@something.abc"
    strcc = ""
    strbcc = ""
    strsub = "Customers"
    strbody = "Hi Ron" & vbNewLine & vbNewLine & _
              "The total Customers of all stores this week is : " & Cells(FormulaCell.Row, "B").Value & _
              vbNewLine & vbNewLine & "Good job"

    With OutMail
        .To = strto
        .CC = strcc
        .BCC = strbcc
        .Subject = strsub
        .Body = strbody
        'You can add a file to the mail like this
        '.Attachments.Add ("C:\test.txt")
        .Display    ' or use .Send
    End With

    Set OutMail = Nothing
    Set OutApp = Nothing
End Sub