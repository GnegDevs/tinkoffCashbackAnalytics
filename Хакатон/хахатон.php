
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="style.css">
    <title>Прiект</title>
</head>
<body>
    <div class="box1">
        <img class="img1" src="tinkoff.jpg" />
        <img class="img2" src="58sch.png" />
        <img class="img3" src="venya.png">
    </div>

    <div class="line"></div>

    <br><br><br>

    <div class="box2">
        <form action="хахатон.php" method="post" id="userDataForm">
            <input type="text" id="name" placeholder="Имя партнера" name="name" required>
            <br>
            <input type="text" id="budget" placeholder="Бюджет" name="budget" required>
            <br>
            <div class="box3">
                <label class="input-file">
                    <input type="file" name="file" id="file" onchange="fileUploaded()">
                    <span class="input-file-btn" id="fileUploadText">Прикрепить базу данных</span>
                </label>
                <button class="button" type="button" onclick="submitForm()">Рассчитать</button>
            </div>
        </form>
    </div>

    <br><br><br>

    <div class="box4" style="display: none;">
        <div class="box41">
            <div class="graphic" id="image-container"></div>
            <div class="box5">
                <h1 class="h1 name">Burger King</h1>
                <div class="line 1"></div>
                <br>
                    <div class="text"><h2 class="h2 id">ID: 1487</h2></div>
                    <div class="text"><h2 class="h2 budget">Бюджет: бургер и кортошка</h2></div>
                    <div class="text"><h2 class="h2 budget_ost">Остаток бюджета: бургер</h2></div>
                    <div class="text"><h2 class="h2 budget_lost">Уже потрачено: кортошка</h2></div>
            </div>
        </div>

        <div class="box61" style="display: none;">
            <div class="box6">
                <div class="text1"><h3 class="h3 result">Дата окончания контракта:</h3></div>
                <div class="text1"><h3 class="h3 num_result">32.03.2024</h3></div>
            </div>

            <div class="box7" style="display: none;">
                <div class="text12"><h3 class="h31">Закрытие контракта не требуется</h3></div>
            </div>
        </div>
    </div>

    <br><br><br>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script>
        function fileUploaded() {
            document.getElementById("fileUploadText").innerText = "Файл загружен";
        }

        function submitForm() {
            var name = document.getElementById("name").value;
            var budget = document.getElementById("budget").value;
            var file = document.getElementById("file").files[0];
            
            var formData = new FormData();
            formData.append('name', name);
            formData.append('budget', budget);
            formData.append('file', file);

            $.ajax({
                url: 'хахатон.php',
                type: 'POST',
                data: formData,
                contentType: false,
                processData: false,
                success: function(response) {
                    document.querySelector('.box4').style.display = 'block';
                    document.querySelector('.box61').style.display = 'block';
                    document.querySelector('.box7').style.display = 'block';
                    document.querySelector('.name').textContent = response.name;
                    document.querySelector('.budget').textContent = response.budget;

// Получение URL картинки с сервера
                    $.ajax({
                        url: 'get_image_url.php', // Путь к вашему PHP скрипту на сервере
                        type: 'GET',
                        success: function(response) {
                            // Здесь response содержит URL картинки
                            // Изменяем атрибут src элемента с классом graphic на полученный URL
                            $('.graphic').html('<img src="' + response + '">');
                        },
                        error: function(error) {
                            console.log(error);
                        }
                    });
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }
    </script>
</body>
</html>
