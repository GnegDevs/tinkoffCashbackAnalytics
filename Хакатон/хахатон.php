<?php
session_start();
// Проверяем, была ли отправлена форма
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Получаем данные из формы
    $name = $_POST['name'];
    $budget = $_POST['budget'];
    // Проверяем, что данные были получены
    if (!empty($name) && !empty($budget)) {
        // Формируем данные для отправки в формате multipart/form-data
        $data = [
            'name' => $name,
            'budget' => $budget
        ];

        // URL REST API для отправки name и budget
        $url = 'http://localhost:8080/tca/api/partners';

        // Настройки запроса для отправки name и budget
        $options = [
            'http' => [
                'header'  => "Content-type: application/x-www-form-urlencoded\r\n" .
                             "Accept: application/json\r\n",
                'method'  => 'POST',
                'content' => http_build_query($data)
            ]
        ];

        // Отправляем запрос для отправки name и budget
        $context  = stream_context_create($options);
        $response = file_get_contents($url, false, $context);

        // Проверяем ответ
        if ($response === false) {
            // Если ответ не получен, возвращаем ошибку
            http_response_code(500);
            echo json_encode(['error' => 'Ошибка: не удалось отправить данные на сервер.']);
            exit;
        }

        // Проверяем, был ли загружен файл
        if (isset($_FILES['file']) && $_FILES['file']['error'] === UPLOAD_ERR_OK) {
            // Получаем имя файла
            $filename = $_FILES['file']['name'];

            // Получаем тип файла
            $filetype = $_FILES['file']['type'];

            // Получаем содержимое файла
            $filecontent = file_get_contents($_FILES['file']['tmp_name']);

            // URL REST API для отправки файла
            $url_file = 'http://localhost:8080/tca/api/partners/upload'; // Измененный URL

            // Настройки запроса для отправки файла
            $options_file = [
                'http' => [
                    'header'  => "Content-type: multipart/form-data\r\n" .
                                 "Accept: application/json\r\n",
                    'method'  => 'POST',
                    'content' => http_build_query(['file' => new CURLFile($_FILES['file']['tmp_name'], $filetype, $filename)])
                ]
            ];

            // Отправляем запрос для отправки файла
            $context_file  = stream_context_create($options_file);
            $response_file = file_get_contents($url_file, false, $context_file);

            // Проверяем ответ
            if ($response_file === false) {
                // Если ответ не получен, возвращаем ошибку
                http_response_code(500);
                echo json_encode(['error' => 'Ошибка: не удалось отправить файл на сервер.']);
                exit;
            }
        }

        // Возвращаем данные в формате JSON
        header('Content-Type: application/json');
        echo json_encode([
            'name' => $name,
            'budget' => $budget,
            // Добавленные данные, которые могли бы вернуться с сервера
            'response' => json_decode($response), // Для примера
            'file_upload_response' => json_decode($response_file) // Для примера
        ]);

    } else {
        // Если данные не были получены, возвращаем ошибку
        http_response_code(400);
        echo json_encode(['error' => 'Ошибка: не удалось получить данные из формы.']);
    }
} else {
    // Если форма не была отправлена, возвращаем ошибку
    http_response_code(400);
    echo json_encode(['error' => 'Ошибка: форма не была отправлена.']);
}
?>
