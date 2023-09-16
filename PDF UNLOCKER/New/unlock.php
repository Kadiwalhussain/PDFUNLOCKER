<?php

// Function to unlock a PDF file using qpdf command line tool
function unlock_pdf($source, $password, $destination) {
  
  // Escape the arguments for shell command
  $source = escapeshellarg($source);
  $password = escapeshellarg($password);
  $destination = escapeshellarg($destination);
  
  // Execute the qpdf command with the arguments and redirect the output to a variable
  exec("qpdf --decrypt --password=$password $source $destination 2>&1", $output);
  
  // Return the output as an array
  return $output;
  
}

// Check if the request method is POST
if ($_SERVER["REQUEST_METHOD"] == "POST") {
  
  // Check if the request has a file and a password
  if (isset($_FILES["file"]) && isset($_POST["password"])) {
    
    // Get the file data
    $file_name = $_FILES["file"]["name"];
    $file_type = $_FILES["file"]["type"];
    $file_size = $_FILES["file"]["size"];
    $file_tmp_name = $_FILES["file"]["tmp_name"];
    
    // Get the password data
    $password = $_POST["password"];
    
    // Validate the file type (must be PDF)
    if ($file_type == "application/pdf") {
      
      // Validate the file size (must be less than 10MB)
      if ($file_size < 10485760) {
        
        // Generate a unique name for the file using a random number and the current timestamp
        $new_file_name = rand(1000,9999).time().".pdf";
        
        // Set the source and destination paths for the unlock function
        $source_path = "uploads/".$new_file_name;
        $destination_path = "unlocked/".$new_file_name;
        
        // Move the uploaded file to the uploads folder
        move_uploaded_file($file_tmp_name, $source_path);
        
        // Call the unlock function and pass the required arguments
        $output = unlock_pdf($source_path, $password, $destination_path);
        
        // Check if the output array is empty (means no error occurred)
        if (empty($output)) {
          
          // Send a JSON response with a success message and a URL to download the unlocked PDF file
          header("Content-Type: application/json");
          echo json_encode(array("message" => "PDF unlocked successfully.", "url" => $destination_path));
          
        } else {
          
          // Send a JSON response with an error message from the output array
          header("Content-Type: application/json");
          echo json_encode(array("error" => implode("\n", $output)));
          
        }
        
      } else {
        
        // Send a JSON response with an error message for invalid file size
        header("Content-Type: application/json");
        echo json_encode(array("error" => "File size must be less than 10MB."));
        
      }
      
    } else {
      
      // Send a JSON response with an error message for invalid file type
      header("Content-Type: application/json");
      echo json_encode(array("error" => "File type must be PDF."));
      
    }
    
  } else {
    
    // Send a JSON response with an error message for missing file or password
    header("Content-Type: application/json");
    echo json_encode(array("error" => "Please select a file and enter a password."));
    
  }
  
} else {
  
  // Send a JSON response with an error message for direct access
  header("Content-Type: application/json");
  echo json_encode(array("error" => "You cannot access this page directly."));
  
}

?>
