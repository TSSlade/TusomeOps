Option Explicit
Private Sub trigger_reminder_emails()
    'Dim FormulaRange As Range
    'These are the named ranges in the worksheet in question'
    Dim countdownRange As Range
    Dim emailStatusRange As Range
    Dim emailAddressRange As Range
    Dim nameFirstRange As Range
    Dim nameLastRange As Range
    Dim advanceIDRange As Range
    Dim advanceReasonRange As Range
    Dim advanceRequiredDateRange As Range
    Dim eventEndDateRange As Range    
    Dim NotSentMsg As String
    Dim MyMsg As String
    Dim SentMsg As String
    Dim MyLimit As Double

    'These are helper ranges defined for other functions to work'
    Dim activeRowRange As Range

    Dim countdownFeedbackOffset As Double
    Dim emailAddressColumn As String
    Dim firstNameColumn As String
    Dim eventNameColumn As String
    Dim advanceAmountColumn As String
    Dim advanceDateColumn As String
    Dim eventStartColumn As String
    Dim eventEndColumn As String


    countdownFeedbackOffset = 2
    emailAddressColumn = "F"
    firstNameColumn = "C"
    advanceDateColumn = "I"
    eventNameColumn = "G"
    eventStartColumn = "J"
    eventEndColumn = "K"

    NotSentMsg = "Not Sent"
    SentMsg = "Sent"

    'Below the MyLimit value it will run the macro
    MyLimit = 1

    'Set the range with Formulas that you want to check
    'Set FormulaRange = Me.Range("I3:I7")
    'Workbooks("Test auto-mail.xlsm").Names("interface").RefersToRange.Interior.Color = vbYellow
    Set countdownRange = worksheets("interface").Range("tbl_interface[Days until Liquidation due]")
    Set emailStatusRange = worksheets("interface").Range("tbl_interface[E-mail Reminder Status]")
    Set emailAddressRange = worksheets("interface").Range("tbl_interface[e-mail]")
    Set nameFirstRange = worksheets("interface").Range("tbl_interface[first name]")
    Set nameLastRange = worksheets("interface").Range("tbl_interface[surname]")
    Set advanceIDRange = worksheets("interface").Range("tbl_interface[user id]")
    Set advanceReasonRange = worksheets("interface").Range("tbl_interface[Advance Reason]")
    Set advanceRequiredDateRange = worksheets("interface").Range("tbl_interface[Date Advance Required]")
    Set eventEndDateRange = worksheets("interface").Range("tbl_interface[Event End Date]")

    On Error GoTo EndMacro:
    For Each countdownCell In countdownRange.Cells
        With countdownCell
            If IsNumeric(.Value) = False Then
                '.Offset(0, 3).Value = "Not numeric"
                MyMsg = "Not numeric"
            Else
                If .Value < MyLimit Then
                    MyMsg = SentMsg
                    'If .Offset(0, 3).Value = NotSentMsg Then
                    If .Offset(0, countdownFeedbackOffset).Value = NotSentMsg Then
                     'If Cells(countdownCell.Row, emailAddressRange).Value = NotSentMsg Then
                        Call Mail_adv_liq_reminder
                    End If
                Else
                    MyMsg = NotSentMsg
                End If
            End If
            Application.EnableEvents = False
            .Offset(0, countdownFeedbackOffset).Value = MyMsg
            Application.EnableEvents = True
        End With
    Next countdownCell

ExitMacro:
    Exit Sub

EndMacro:
    Application.EnableEvents = True

    MsgBox "Some Error occurred." _
         & vbLf & Err.Number _
         & vbLf & Err.Description

End Sub

'Reference websites'
'http://www.globaliconnect.com/excel/index.php?option=com_content&view=article&id=186:excel-vba-referencing-ranges-range-cells-item-rows-a-columns-properties-offset-activecell-selection-insert&catid=79&Itemid=475'
'http://stackoverflow.com/questions/17228318/whats-the-right-way-to-reference-named-cells-in-excel-2013-vba-i-know-im-mes'
'http://www.ozgrid.com/forum/showthread.php?t=37265
