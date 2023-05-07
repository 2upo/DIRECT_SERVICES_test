	var weatherBtn = document.getElementById("weather-btn");
	var inputBtn = document.getElementById("input-btn");
	var inputField = document.getElementById("input-field");
	var resultBlock = document.getElementById("result-block");

	weatherBtn.addEventListener("click", function() {
	resultBlock.innerHTML = "Погода для 5 случайных городов: ...";
	});

	inputBtn.addEventListener("click", function() {
	var value = inputField.value;
	resultBlock.innerHTML = "Вы ввели: " + value;
	});