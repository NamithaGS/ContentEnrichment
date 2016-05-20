<?php


$str = file_get_contents('Measurement.json');
$json = json_decode($str, true); 
//var_dump( $json);
$filenamearray = array();
$i = 0 ;
foreach ( $json as $key => $value)
{
	//var_dump ($key);
	$filenamearray[$i] = substr($key, strrpos($key, '/') + 1);
	//var_dump ($filenamearray[$i]);
	$i++;

}
$title = "Team10";
$restoffiles = "";

for ($x = 0; $x < sizeof($filenamearray); $x++) {
    echo "The number is: $x <br>";
	
	//echo "The title is: $title <br>";
	$url = urlencode($filenamearray[$x]);
	$api_url = 'http://localhost/YOURLS-master/yourls-api.php?title='.$title.'&signature=ae6a332cc0&action=shorturl&format=json&url='.$url;
	//echo $api_url;
	$arr_output = json_decode(file_get_contents($api_url));
	//print_r ($arr_output);
	$restoffiles = $restoffiles.'&urls[]='.$url;
}
/*
$api_urla = 'http://localhost/YOURLS-master/yourls-api.php?title='.$title.'&signature=ae6a332cc0&action=bulkshortener&format=json'.$restoffiles;
echo $api_urla;
//$api_urlex = 'http://localhost/YOURLS-master/yourls-api.php?title=Team10&signature=ae6a332cc0&action=bulkshortener&urls[]=http://url1&urls[]=http://url2';
//echo $api_urlex;
//$arr_output = json_decode(file_get_contents($api_urla));
	
$format  = 'json';                       // output format: 'json', 'xml' or 'simple'

//echo sizeof($filenamearray);
$ch = curl_init();
curl_setopt( $ch, CURLOPT_HEADER, 0 );            // No header in the result
curl_setopt( $ch, CURLOPT_RETURNTRANSFER, true ); // Return, do not echo result
curl_setopt( $ch, CURLOPT_POST, 1 );              // This is a POST request
curl_setopt ( $ch, CURLOPT_URL, $api_urla );
curl_setopt( $ch, CURLOPT_POSTFIELDS, array(      // Data to POST
		'url'      => $api_urla,
		'title'    => $title,
		'format'   => $format,
		'action'   => 'bulkshortener',
		'signature' => 'ae6a332cc0'
	) );

// Fetch and return content
$data = curl_exec($ch);
//sleep(5);

//}
curl_close($ch);

*/

//Connect to db to get the short url and filename to json
$servername = "localhost";
$username = "root";
$password = "aateaate";

// Create connection
$conn = new mysqli($servername, $username, $password);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}  	 	
echo "Connected successfully";
//$result = mysqli_query($conn ,"SELECT keyword,url FROM ngsurl;");
$db = mysqli_select_db( $conn,"yourls");

if(!$result = $conn->query('SELECT keyword,url FROM ngsurl')){
    die('There was an error running the query [' . $conn->error . ']');
}

while ( $row = $result->fetch_assoc()) {
		//var_dump( $row);
	$url=$row['url']; 
	$shorturl='polar.usc.edu/'.$row['keyword']; 
	//var_dump ($url);
	//var_dump ($shorturl);
	$posts[] = array('url'=> $url, 'shorturl'=> $shorturl);
	 
}


//var_dump ($posts);
$response['DOI'] = $posts;

$fp = fopen('DOI_url.json', 'w');
$str = json_encode($response, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES );
//$str1 = preg_replace('/\\\\\"/',"\"", $str);
fwrite($fp,$str );
fclose($fp);

?>