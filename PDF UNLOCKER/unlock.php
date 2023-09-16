<?php
require 'path/to/itextpdf.php'; // Replace with the actual path

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $pdfFile = $_FILES['pdfFile']['tmp_name'];
    $password = $_POST['password'];
    
    $pdfReader = new PdfReader($pdfFile);
    
    if ($pdfReader->isEncrypted()) {
        $pdfReader->setPassword($password);
        if (!$pdfReader->encryptor->isEncryptionFinished()) {
            // Password is incorrect
            echo 'Incorrect password. Please try again.';
            exit;
        }
    }
    
    // The password is correct or the PDF is not encrypted
    $pdfWriter = new PdfWriter('unlocked.pdf');
    $pdfWriter->setPdfDocument($pdfReader->readPdf());
    $pdfWriter->writeAll();
    
    // Return the unlocked PDF as a response
    header('Content-Type: application/pdf');
    header('Content-Disposition: inline; filename="unlocked.pdf"');
    readfile('unlocked.pdf');
    exit;
}
