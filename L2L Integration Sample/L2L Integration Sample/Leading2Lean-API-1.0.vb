'
' Leading2Lean-API-1.0.vb: Helper functions for Dispatch API calls
' 
' Authors:
'   Tyler Whitaker <tyler@leading2lean.com>
' 
' Copyright 2016 Leading2Lean, LLC. (www.leading2lean.com)
' Licensed under the MIT license. See LICENSE file in the project root for full license information.
' 

Imports System
Imports System.IO
Imports System.Net
Imports System.Text
Imports System.Web


Namespace Leading2Lean.API

    Public Class L2LConnection
        Public API_END_POINT As String = "http://beta.leading2lean.com/api/1.0/"    ' Put your server API URL here.  Example: http://beta.leading2lean.com/api/1.0/
        Public API_KEY As String = "YourKeyGoesHere"                                ' You'll want to put your API Key Here
        Public API_SITE As String = "0"                                             ' This is the site code you are accessing
        Public API_USER_AGENT As String = "L2L Integration Sample Code vb.NET"      ' Change this value to be the name of your application

        Public Sub New()
            ' Basic Constructor
        End Sub

        Public Sub New(ByVal End_Point As String, ByVal Key As String, ByVal Site As String)
            Me.API_END_POINT = End_Point
            Me.API_KEY = Key
            Me.API_SITE = Site
        End Sub

        Public Function GetURL(ByVal apiCall As String, ByVal apiData As String)
            Dim request As HttpWebRequest
            Dim response As HttpWebResponse = Nothing
            Dim reader As StreamReader
            Dim result As New StringBuilder
            Dim errormsg As String

            If apiCall Is Nothing Then Throw New ArgumentNullException("apiCall")

            ' Create the web request  
            request = DirectCast(WebRequest.Create(API_END_POINT + apiCall + "/?" + apiData), HttpWebRequest)
            request.UserAgent = API_USER_AGENT
            request.KeepAlive = False
            request.Timeout = 15 * 1000

            Try
                ' Get response  
                response = DirectCast(request.GetResponse(), HttpWebResponse)

                If request.HaveResponse = True AndAlso Not (response Is Nothing) Then

                    ' Get the response stream  
                    reader = New StreamReader(response.GetResponseStream())

                    ' Read it into a StringBuilder  
                    result = New StringBuilder(reader.ReadToEnd())

                End If
            Catch wex As WebException
                ' This exception will be raised if the server didn't return 200 - OK  
                ' Try to retrieve more information about the network error  
                If Not wex.Response Is Nothing Then
                    Dim errorResponse As HttpWebResponse = Nothing
                    Try
                        errorResponse = DirectCast(wex.Response, HttpWebResponse)
                        errormsg = "The server returned '" + errorResponse.StatusDescription + "' with the status code: " + errorResponse.StatusCode
                        Throw New ApplicationException(errormsg)
                    Finally
                        If Not errorResponse Is Nothing Then errorResponse.Close()
                    End Try
                End If
            Finally
                If Not response Is Nothing Then response.Close()
            End Try
            Return result.ToString()

        End Function



        Public Function PostURL(ByVal apiCall As String, ByVal apiData As String)
            ' We use the HttpUtility class from the System.Web namespace  
            Dim request As HttpWebRequest
            Dim response As HttpWebResponse = Nothing
            Dim reader As StreamReader
            Dim address As Uri
            Dim byteData() As Byte
            Dim postStream As Stream = Nothing
            Dim result As New StringBuilder
            Dim errormsg As String

            If apiCall Is Nothing Then Throw New ArgumentNullException("apiCall")
            address = New Uri(API_END_POINT + apiCall)

            ' Create the web request  
            request = DirectCast(WebRequest.Create(address), HttpWebRequest)
            request.UserAgent = API_USER_AGENT
            request.KeepAlive = False
            request.Timeout = 15 * 1000

            ' Set type to POST  
            request.Method = "POST"
            request.ContentType = "application/x-www-form-urlencoded"

            ' Set the content length in the request headers  
            request.ContentLength = apiData.Length

            ' Create a byte array of the data we want to send  
            byteData = UTF8Encoding.UTF8.GetBytes(apiData)

            ' Write data  
            Try
                postStream = request.GetRequestStream()
                postStream.Write(byteData, 0, byteData.Length)
            Finally
                If Not postStream Is Nothing Then postStream.Close()
            End Try

            Try
                ' Get response  
                response = DirectCast(request.GetResponse(), HttpWebResponse)

                If request.HaveResponse = True AndAlso Not (response Is Nothing) Then

                    ' Get the response stream  
                    reader = New StreamReader(response.GetResponseStream())

                    ' Read it into a StringBuilder  
                    result = New StringBuilder(reader.ReadToEnd())

                End If
            Catch wex As WebException
                ' This exception will be raised if the server didn't return 200 - OK  
                ' Try to retrieve more information about the network error  
                If Not wex.Response Is Nothing Then
                    Dim errorResponse As HttpWebResponse = Nothing
                    Try
                        errorResponse = DirectCast(wex.Response, HttpWebResponse)
                        errormsg = "The server returned '" + errorResponse.StatusDescription + "' with the status code: " + errorResponse.StatusCode
                        Throw New ApplicationException(errormsg)
                    Finally
                        If Not errorResponse Is Nothing Then errorResponse.Close()
                    End Try
                End If
            Finally
                If Not response Is Nothing Then response.Close()
            End Try
            Return result.ToString()

        End Function

    End Class

    Public Class Dispatch
        ' Good example of retrieving data
        Public Function get_dispatch(ByVal dispatchnumber As String)
            Dim L2LConn As New L2LConnection()

            Dim urlData = New StringBuilder()
            Dim byteData = New StringBuilder()

            urlData.Append("dispatches/")

            byteData.Append("auth=" + Uri.EscapeDataString(L2LConn.API_KEY))
            byteData.Append("&site=" + Uri.EscapeDataString(L2LConn.API_SITE))
            byteData.Append("&dispatchnumber=" + Uri.EscapeDataString(dispatchnumber))

            Return L2LConn.GetURL(urlData.ToString(), byteData.ToString())
        End Function
    End Class

    Public Class Technician
        ' Good example of changing data in the system.
        Public Function set_availability(ByVal technician_id As String,
                                         ByVal available As Boolean)
            Dim L2LConn As New L2LConnection()

            Dim urlData = New StringBuilder()
            Dim byteData = New StringBuilder()

            urlData.Append("technicians/set_availability/" + Uri.EscapeDataString(technician_id) + "/")

            byteData.Append("auth=" + Uri.EscapeDataString(L2LConn.API_KEY))
            byteData.Append("&site=" + Uri.EscapeDataString(L2LConn.API_SITE))
            byteData.Append("&available=" + Uri.EscapeDataString(available))

            Return L2LConn.PostURL(urlData.ToString(), byteData.ToString())
        End Function
    End Class

End Namespace