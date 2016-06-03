Imports L2L_Integration_Sample.Leading2Lean.API

<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class Form1
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.btnAvailable = New System.Windows.Forms.Button()
        Me.txtTechnician_ID = New System.Windows.Forms.TextBox()
        Me.Label1 = New System.Windows.Forms.Label()
        Me.btnUnavailable = New System.Windows.Forms.Button()
        Me.txtDispatchNumber = New System.Windows.Forms.TextBox()
        Me.lblDispatchNumber = New System.Windows.Forms.Label()
        Me.btnGetDispatch = New System.Windows.Forms.Button()
        Me.txtResults = New System.Windows.Forms.TextBox()
        Me.lblResults = New System.Windows.Forms.Label()
        Me.GroupBox1 = New System.Windows.Forms.GroupBox()
        Me.GroupBox2 = New System.Windows.Forms.GroupBox()
        Me.GroupBox1.SuspendLayout()
        Me.GroupBox2.SuspendLayout()
        Me.SuspendLayout()
        '
        'btnAvailable
        '
        Me.btnAvailable.Location = New System.Drawing.Point(18, 51)
        Me.btnAvailable.Name = "btnAvailable"
        Me.btnAvailable.Size = New System.Drawing.Size(93, 22)
        Me.btnAvailable.TabIndex = 0
        Me.btnAvailable.Text = "Set Available"
        Me.btnAvailable.UseVisualStyleBackColor = True
        '
        'txtTechnician_ID
        '
        Me.txtTechnician_ID.Location = New System.Drawing.Point(100, 25)
        Me.txtTechnician_ID.Name = "txtTechnician_ID"
        Me.txtTechnician_ID.Size = New System.Drawing.Size(68, 20)
        Me.txtTechnician_ID.TabIndex = 1
        '
        'Label1
        '
        Me.Label1.AutoSize = True
        Me.Label1.Location = New System.Drawing.Point(20, 28)
        Me.Label1.Name = "Label1"
        Me.Label1.Size = New System.Drawing.Size(74, 13)
        Me.Label1.TabIndex = 2
        Me.Label1.Text = "Technician ID"
        '
        'btnUnavailable
        '
        Me.btnUnavailable.Location = New System.Drawing.Point(117, 51)
        Me.btnUnavailable.Name = "btnUnavailable"
        Me.btnUnavailable.Size = New System.Drawing.Size(93, 22)
        Me.btnUnavailable.TabIndex = 3
        Me.btnUnavailable.Text = "Set Unavailable"
        Me.btnUnavailable.UseVisualStyleBackColor = True
        '
        'txtDispatchNumber
        '
        Me.txtDispatchNumber.Location = New System.Drawing.Point(116, 25)
        Me.txtDispatchNumber.Name = "txtDispatchNumber"
        Me.txtDispatchNumber.Size = New System.Drawing.Size(69, 20)
        Me.txtDispatchNumber.TabIndex = 4
        '
        'lblDispatchNumber
        '
        Me.lblDispatchNumber.AutoSize = True
        Me.lblDispatchNumber.Location = New System.Drawing.Point(22, 28)
        Me.lblDispatchNumber.Name = "lblDispatchNumber"
        Me.lblDispatchNumber.Size = New System.Drawing.Size(92, 13)
        Me.lblDispatchNumber.TabIndex = 5
        Me.lblDispatchNumber.Text = "Dispatch Number:"
        '
        'btnGetDispatch
        '
        Me.btnGetDispatch.Location = New System.Drawing.Point(25, 51)
        Me.btnGetDispatch.Name = "btnGetDispatch"
        Me.btnGetDispatch.Size = New System.Drawing.Size(91, 22)
        Me.btnGetDispatch.TabIndex = 6
        Me.btnGetDispatch.Text = "Get Dispatch"
        Me.btnGetDispatch.UseVisualStyleBackColor = True
        '
        'txtResults
        '
        Me.txtResults.Location = New System.Drawing.Point(14, 131)
        Me.txtResults.Multiline = True
        Me.txtResults.Name = "txtResults"
        Me.txtResults.ScrollBars = System.Windows.Forms.ScrollBars.Both
        Me.txtResults.Size = New System.Drawing.Size(428, 207)
        Me.txtResults.TabIndex = 7
        '
        'lblResults
        '
        Me.lblResults.AutoSize = True
        Me.lblResults.Location = New System.Drawing.Point(13, 116)
        Me.lblResults.Name = "lblResults"
        Me.lblResults.Size = New System.Drawing.Size(42, 13)
        Me.lblResults.TabIndex = 8
        Me.lblResults.Text = "Results"
        '
        'GroupBox1
        '
        Me.GroupBox1.Controls.Add(Me.btnGetDispatch)
        Me.GroupBox1.Controls.Add(Me.lblDispatchNumber)
        Me.GroupBox1.Controls.Add(Me.txtDispatchNumber)
        Me.GroupBox1.Location = New System.Drawing.Point(15, 12)
        Me.GroupBox1.Name = "GroupBox1"
        Me.GroupBox1.Size = New System.Drawing.Size(195, 90)
        Me.GroupBox1.TabIndex = 9
        Me.GroupBox1.TabStop = False
        Me.GroupBox1.Text = "Dispatch Records"
        '
        'GroupBox2
        '
        Me.GroupBox2.Controls.Add(Me.btnUnavailable)
        Me.GroupBox2.Controls.Add(Me.Label1)
        Me.GroupBox2.Controls.Add(Me.txtTechnician_ID)
        Me.GroupBox2.Controls.Add(Me.btnAvailable)
        Me.GroupBox2.Location = New System.Drawing.Point(216, 12)
        Me.GroupBox2.Name = "GroupBox2"
        Me.GroupBox2.Size = New System.Drawing.Size(216, 90)
        Me.GroupBox2.TabIndex = 10
        Me.GroupBox2.TabStop = False
        Me.GroupBox2.Text = "Technicians"
        '
        'Form1
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(454, 349)
        Me.Controls.Add(Me.GroupBox2)
        Me.Controls.Add(Me.GroupBox1)
        Me.Controls.Add(Me.lblResults)
        Me.Controls.Add(Me.txtResults)
        Me.Name = "Form1"
        Me.Text = "L2L Integration Sample"
        Me.GroupBox1.ResumeLayout(False)
        Me.GroupBox1.PerformLayout()
        Me.GroupBox2.ResumeLayout(False)
        Me.GroupBox2.PerformLayout()
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub
    Friend WithEvents btnAvailable As System.Windows.Forms.Button
    Friend WithEvents txtTechnician_ID As System.Windows.Forms.TextBox
    Friend WithEvents Label1 As System.Windows.Forms.Label
    Friend WithEvents btnUnavailable As System.Windows.Forms.Button

    Private Sub btnAvailable_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnAvailable.Click
        Dim Tech As New Technician
        Dim result As String

        If Me.txtTechnician_ID.Text <> "" Then
            result = Tech.set_availability(Me.txtTechnician_ID.Text, True)
            MsgBox(result)
        Else
            MsgBox("Technician ID must not be blank.")
        End If
    End Sub

    Private Sub btnUnavailable_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnUnavailable.Click
        Dim Tech As New Technician
        Dim result As String

        If Me.txtTechnician_ID.Text <> "" Then
            result = Tech.set_availability(Me.txtTechnician_ID.Text, False)
            Me.txtResults.Text = result
        Else
            MsgBox("Technician ID must not be blank.")
        End If
    End Sub
    Friend WithEvents txtDispatchNumber As System.Windows.Forms.TextBox
    Friend WithEvents lblDispatchNumber As System.Windows.Forms.Label
    Friend WithEvents btnGetDispatch As System.Windows.Forms.Button

    Private Sub btnGetDispatch_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnGetDispatch.Click
        Dim Dispatch_Data As New Dispatch
        Dim result As String

        If Me.txtDispatchNumber.Text <> "" Then
            result = Dispatch_Data.get_dispatch(Me.txtDispatchNumber.Text)
            Me.txtResults.Text = PrettyFormat(result)
        Else
            MsgBox("Dispatch Number must not be blank.")
        End If

    End Sub
    Friend WithEvents txtResults As System.Windows.Forms.TextBox
    Friend WithEvents lblResults As System.Windows.Forms.Label
    Friend WithEvents GroupBox1 As System.Windows.Forms.GroupBox
    Friend WithEvents GroupBox2 As System.Windows.Forms.GroupBox

    Private Sub Form1_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load

    End Sub

    Private Sub Form1_Resize(ByVal sender As Object, ByVal e As System.EventArgs) Handles Me.Resize
        Me.txtResults.Width = Me.Width - 50
        Me.txtResults.Height = Me.Height - Me.txtResults.Top - 50
    End Sub

    Private Function PrettyFormat(ByVal str As String) As String
        str = str.Replace(",", "," + vbCrLf)
        str = str.Replace("{", "{" + vbCrLf)
        str = str.Replace("}", "}" + vbCrLf)
        Return str
    End Function
End Class
