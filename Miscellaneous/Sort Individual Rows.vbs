' Source: https://www.extendoffice.com/documents/excel/4265-excel-sort-multiple-columns-independently.html
Sub SortIndividualR()
'Updateby Extendoffice 20161123
    Dim xRg As Range, yRg As Range
    If TypeName(Selection) <> "Range" Then Exit Sub
    Set xRg = Selection
    If xRg.Count = 1 Then
        MsgBox "Select multiple cells!", vbExclamation, "Kutools for Excel"
        Exit Sub
    End If
    With Application
        .ScreenUpdating = False
        .EnableEvents = False
        .Calculation = xlCalculationManual
    End With
    Application.ScreenUpdating = False
    For Each yRg In xRg.Rows
        yRg.Sort Key1:=yRg.Cells(1, 1), _
        Order1:=xlAscending, _
        Header:=xlNo, _
        Orientation:=xlSortRows
    Next yRg
    With Application
        .ScreenUpdating = True
        .EnableEvents = True
        .Calculation = xlCalculationAutomatic
    End With
    Application.ScreenUpdating = True
End Sub



