<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>Zmiana hasła</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; }
        input { display: block; margin: 10px 0; padding: 8px; width: 300px; }
        button { padding: 10px 20px; }
        .message { margin-top: 20px; padding: 10px; border-radius: 5px; }
        .success { background-color: #c8e6c9; }
        .error { background-color: #ffcdd2; }
    </style>
</head>
<body>
    <h1>Zmiana hasła użytkownika</h1>
    <form method="post">
        <input type="text" name="username" placeholder="Nazwa użytkownika" required>
        <input type="password" name="old_password" placeholder="Stare hasło">
        <input type="password" name="new_password" placeholder="Nowe hasło" required>
        <button type="submit">Zmień hasło</button>
    </form>

    <?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $api_url = "http://172.17.0.1:5000/change_password";


        $data = [
            'username' => $_POST['username'],
            'old_password' => $_POST['old_password'] ?? '',
            'new_password' => $_POST['new_password']
        ];

        $ch = curl_init($api_url);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

        $response = curl_exec($ch);

        if(curl_errno($ch)) {
            echo '<div class="message error">Błąd cURL: ' . curl_error($ch) . '</div>';
        } else {
            $result = json_decode($response, true);
            if ($result) {
                $class = $result['status'] === 'ok' ? 'success' : 'error';
                echo '<div class="message ' . $class . '">' . htmlspecialchars($result['message']) . '</div>';
            } else {
                echo '<div class="message error">Nie udało się odczytać odpowiedzi z API</div>';
            }
        }

        curl_close($ch);
    }
    ?>
</body>
</html>
