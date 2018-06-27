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
    'Set FormulaRange = Me.Range("M3:M61")
    'Set FormulaRange = Workbooks("Advance Request & Tracking Form rebuild.xlsm").Range("tbl_interface[Liquidation in]").RefersToRange
    Set FormulaRange = Worksheets("interface").Range("M3:M61")

    'MsgBox FormulaRange
    
    countdownFeedbackOffset = 2

    On Error GoTo EndMacro:
    For Each FormulaCell In FormulaRange.Cells
        With FormulaCell
            If IsNumeric(.Value) = False Then
                .Offset(0, 2).Value = "Not numeric"
                MyMsg = "Not numeric"
            Else
                If .Value < MyLimit Then
                    MyMsg = SentMsg
                    If .Offset(0, countdownFeedbackOffset).Value = NotSentMsg Then
                        Call Mail_adv_liq_reminder
                        'Call Mail_with_outlook1
                    End If
                Else
                    MyMsg = NotSentMsg
                End If
            End If
            Application.EnableEvents = False
            .Offset(0, countdownFeedbackOffset).Value = MyMsg
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
