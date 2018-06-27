Option Explicit
Private Sub Worksheet_Calculate()
    Dim FormulaRange As Range
    Dim countdownRange As Range
    Dim NotSentMsg As String
    Dim MyMsg As String
    Dim SentMsg As String
    Dim MyLimit As Double
    Dim countdownFeedbackOffset As Double

    NotSentMsg = "Not Sent"
    SentMsg = "Sent"

    'Below the MyLimit value it will run the macro
    MyLimit = 1

    'Set the range with Formulas that you want to check
    'Set FormulaRange = Me.Range("I3:I7")
    'Workbooks("Test auto-mail.xlsm").Names("interface").RefersToRange.Interior.Color = vbYellow
    Set FormulaRange = Worksheets("interface").Range("tbl_countdown[Days remaining]")
    'Set FormulaRange = Workbooks("Test auto-mail.xlsm").Range("tbl_countdown[Days remaining]").RefersToRange

    'MsgBox FormulaRange
    
    countdownFeedbackOffset = 3

    On Error GoTo EndMacro:
    For Each FormulaCell In FormulaRange.Cells
        With FormulaCell
            If IsNumeric(.Value) = False Then
                '.Offset(0, 3).Value = "Not numeric"
                MyMsg = "Not numeric"
            Else
                If .Value < MyLimit Then
                    MyMsg = SentMsg
                    If .Offset(0, countdownFeedbackOffset).Value = NotSentMsg Then
                        'Call Mail_adv_liq_reminder
                        Call Mail_with_outlook1
                    End If
                Else
                    MyMsg = NotSentMsg
                End If
            End If
            Application.EnableEvents = False
            .Offset(0, 3).Value = MyMsg
            Application.EnableEvents = True
        End With
    Next FormulaCell

ExitMacro:
    Exit Sub

EndMacro:
    Application.EnableEvents = True

    MsgBox "Some Error occurred." _
         & vbLf & Err.Number _
         & vbLf & Err.Description

End Sub



