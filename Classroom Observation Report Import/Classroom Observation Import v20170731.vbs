Sub getWordFormDataTusome()
Dim wdApp As New Word.Application
Dim myDoc As Word.Document
Dim CCtl As Word.ContentControl
Dim myFolder As String, strFile As String
Dim myWkSht As Worksheet, i As Long, j As Long

myFolder = "C:\Dropbox\Kenya Tusome\Technical\tool development\CLO Consolidation Tool\Observations"
Application.ScreenUpdating = False

If myFolder = "" Then Exit Sub
Set myWkSht = ActiveSheet
ActiveSheet.Cells.Clear
Range("A1") = "County"
Range("a1").Font.Bold = True
Range("B1") = "Zone/Cluster"
Range("b1").Font.Bold = True
Range("C1") = "School"
Range("c1").Font.Bold = True
Range("D1") = "CSO/EARC/IC"
Range("d1").Font.Bold = True
Range("E1") = "Class"
Range("e1").Font.Bold = True
Range("F1") = "Teacher"
Range("f1").Font.Bold = True
Range("G1") = "RTI Officer"
Range("g1").Font.Bold = True
Range("H1") = "MOE Officer"
Range("h1").Font.Bold = True
Range("I1") = "TSC Officer"
Range("I1").Font.Bold = True
Range("J1") = "Date"
Range("J1").Font.Bold = True
Range("K1") = "Subject"
Range("K1").Font.Bold = True
Range("L1") = "Week"
Range("L1").Font.Bold = True
Range("M1") = "Day"
Range("M1").Font.Bold = True
Range("N1") = "Lesson Duration"
Range("N1").Font.Bold = True
Range("O1") = "Pupils Present"
Range("O1").Font.Bold = True
Range("P1") = "Girls"
Range("P1").Font.Bold = True
Range("Q1") = "Boys"
Range("Q1").Font.Bold = True
Range("R1") = "Take-up Rating"
Range("R1").Font.Bold = True
Range("S1") = "Class 3 Book"
Range("S1").Font.Bold = True
Range("T1") = "Avg Fluency (cwpm)"
Range("T1").Font.Bold = True
Range("U1") = "Qualitative Background Information"
Range("U1").Font.Bold = True
Range("V1") = "What Went Well"
Range("V1").Font.Bold = True
Range("W1") = "What Did Not Go Well"
Range("W1").Font.Bold = True
Range("X1") = "Feedback From CSO/DICECE"
Range("X1").Font.Bold = True
Range("Y1") = "Feedback to CSO/DICECE"
Range("Y1").Font.Bold = True
Range("Z1") = "Overall Observations and Recommendations"
Range("Z1").Font.Bold = True


i = myWkSht.Cells(myWkSht.Rows.Count, 1).End(xlUp).Row
strFile = Dir(myFolder & "\*.docx", vbNormal)

While strFile <> ""
i = i + 1

Set myDoc = wdApp.Documents.Open(Filename:=myFolder & "\" & strFile, AddToRecentFiles:=False, Visible:=False)

With myDoc
j = 0
For Each CCtl In .ContentControls
j = j + 1
myWkSht.Cells(i, j) = CCtl.Range.Text
Next
myWkSht.Columns.AutoFit
End With
myDoc.Close SaveChanges:=False
strFile = Dir()
Wend
wdApp.Quit
Set myDoc = Nothing: Set wdApp = Nothing: Set myWkSht = Nothing
Application.ScreenUpdating = True

End Sub
