<?php session_start();?>
<html>
<head>
<!--link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

<!-- jQuery library -->
<!--script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>

<!-- Latest compiled JavaScript -->
<!--script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script-->
</head>
<body>
<?php
//session_start();
$_SESSION['manish1']=$_GET['v1'];
$_SESSION['manish2']=$_GET['v2'];
$_SESSION['name'] = $_GET['name'];

//echo '1#'.$_SESSION['manish1'].'2#'.$_SESSION['manish2'].'3#'.$_SESSION['name'];
$con= new mysqli('localhost','root','','patents');

if(isset($_POST['export_excel']))
{
	

if(!empty($_SESSION['manish2']))
{
	$x1=$_SESSION['name'];
    $x2=$_SESSION['manish2'];
$sql3 = "Select * from patent_tables where ".$x2." like '%".$x1."%'";
}
else if(!empty($_SESSION['manish1']))
{
	$x=$_SESSION['manish1'];
	
    $sql3 = "Select * from patent_tables ORDER BY $x";
	
}	
$result=$con->query($sql3);
$output ='';
$output .='<table class="table" bordered="1">
<tr>
<th>Application No.</th>
<th>Date of filling of Application</th>
<th>Publication Date</th>
<th>Name of Applicant</th>
<th>Title of Invention</th>
<th>Name of Inventor(s)</th>
<th>Abstract</th>
<th>No. of pages</th>
<th>No. of claims</th>
<th>International classification</th>
<th>Priority Document No.</th>
<th>Priority Date</th>
<th>Name of priority country</th>
<th>International Application No.</th>
<th>International Application Filling Date</th>
<th>International Publication No.</th>
<th>Patent of addition to Application No.</th>
<th>Patent of addition to Application No. Filling Date</th>
<th>Divisional to Application No.</th>
<th>Divisional to Application No. Filling Date</th>
</tr>';

if ($result->num_rows > 0) {
  while($row=$result->fetch_assoc())
{
  $output .='
            <tr>
     <td>' . $row['Application_No'] .'</td>
     <td>' . $row['Date_of_filing_of_Application'] . '</td>
     <td>' . $row['Publication_Date'] . '</td>
     <td>' . $row['Name_of_Applicant'] . '</td>
	 <td>' . $row['Title_of_Invention'] .'</td>
     <td>' . $row['Name_of_Inventor'] . '</td>
	 <td>' . $row['Abstract'] .'</td>
	 <td>' . $row['No_of_pages'] .'</td>
	 <td>' . $row['No_of_claims'] .'</td>
	 <td>' . $row['International_classification'] .'</td>
	 <td>' . $row['Priority_Document_No'] .'</td>
	 <td>' . $row['Priority_Date'] .'</td>
	 <td>' . $row['Name_of_priority_country'] .'</td>
	 <td>' . $row['International_Application_No'] .'</td>
	 <td>' . $row['International_Application_Filing_Date'] .'</td>
	 <td>' . $row['International_Publication_No'] .'</td>
	 <td>' . $row['Patent_of_addition_to_Application_No'] .'</td>
	 <td>' . $row['Patent_of_addition_to_Application_No_Filing_Date'] .'</td>
	 <td>' . $row['Divisional_to_Application_No'] .'</td>
	 <td>' . $row['Divisional_to_Application_No_Filing_Date'] .'</td>
	
     </tr>';
}
}
   $output .='</table>';
   header("Content-Type:application/octet-stream");
   header("content-Disposition: attachment;filename=download.xls");
   header("Pragma: no-cache");
   header ("Expires: 0");
  
   echo $output;
}
session_destroy();
?>
</body>
</html>