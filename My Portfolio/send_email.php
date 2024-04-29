
<!DOCTYPE html>
<html>
<body>

<?php
phpinfo(); 
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST["name"];
    $email = $_POST["email"];
    $message = $_POST["message"];

    // Set up the email
    $to = "shanemashele0935@gmail.com"; // Change this to your email address
    $subject = "Contact Form Submission";
    $body = "Name: $name\nEmail: $email\n\nMessage:\n$message";

    // Send the email
    if (mail($to, $subject, $body)) {
        echo "Message sent successfully!";
    } else {
        echo "Message failed to send.";
    }
}
?>
</body>
</html>