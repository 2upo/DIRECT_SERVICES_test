$(document).ready(function(){
    $('#weather-btn').click(function() {
        $('#forecast-container').empty();
        $(".aggregated-table").css("display", "none");
        $.ajax({
            url: "http://127.0.0.1:5000/api/weather/random",	
            method: "GET",
            success: function(response) {
                if (response["errors"].length > 0) {
                    $('#error-message').text(response['errors']);
                    $('#error-modal').modal('show');
                }
                var data = response
                // Display aggregated data
                $('#average-temperature').text(data.aggregated["Average Temperature (C)"]);
                $('#maximum-temperature').text(data.aggregated["Maximum Temperature (C)"]);
                $('#minimum-temperature').text(data.aggregated["Minimum Temperature (C)"]);

                // Display forecast data
                var forecastContainer = $('#forecast-container');
                $.each(data.forecast, function(cityName, cityData) {
                var card = $('<div class="card">');
                const cityDate = new Date(cityData['Timestamp']*1000 - cityData['Timezone']* 1000);
                const options = {
                weekday: 'long', 
                month: 'short', 
                day: 'numeric', 
                hour: 'numeric', 
                minute: 'numeric'};
                const formattedDate = cityDate.toLocaleString('en-US', options);

                var cardHeader = $('<div class="card-header">').text(formattedDate);
                var cardBody = $('<div class="card-body">');
                var cardText = $('<div class="card-text">');
                var cityNameElem = $('<div class="city-name">').text(cityName);
                var iconElem = $('<img class="icon">').attr('src', 'https://openweathermap.org/img/wn/' + cityData.Icon + '.png');
                var temperatureElem = $('<span class="temperature">').text(cityData["Temperature (C)"]);
                var unitElem = $('<span class="unit">&deg;C</span>');
                var descriptionElem = $('<div class="description">').text(cityData.Description);
                var humidityElem = $('<div class="humidity">').text('Humidity: ' + cityData["Humidity (%)"] + '%');

                // Append elements to card
                cardText.append(iconElem);
                cardText.append(temperatureElem);
                cardText.append(unitElem);
                cardText.append(descriptionElem);
                cardText.append(humidityElem);
                cardText.append(cityNameElem);
                cardBody.append(cardText);
                card.append(cardHeader);
                card.append(cardBody);
          
              // Append card to container
              forecastContainer.append(card);
              });
              $(".aggregated-table").css("display", "table");
            },
            error: function(xhr, status, error) {
                $('#error-message').text(status + ': ' + error);
                $('#error-modal').modal('show');
              }
        });
    });

    $('#input-btn').click(function() {
        var value = $('#input-field').val();
        $.ajax({
            url: "http://127.0.0.1:5000/api/weather/" + value,
            method: "GET",
            success: function(response) {
                console.log(response["errors"])
                if (response["errors"].length > 0) {
                    $('#error-message').text(response['errors']);
                    $('#error-modal').modal('show');
                }

                var weather = response['forecast']['Description'][value];
                var temperature = response['forecast']['Temperature (C)'][value];
                var humidity = response['forecast']['Humidity (%)'][value];
                var country = response['forecast']['Country Code'][value];
                
                var table = $('<table>').addClass('table');
                $('#forecast-container').html(table);
                
                var tbody = $('<tbody>');
                tbody.append($('<tr>').append($('<td>').text('City:')).append($('<td>').text(value)));
                tbody.append($('<tr>').append($('<td>').text('Country:')).append($('<td>').text(country)));
                tbody.append($('<tr>').append($('<td>').text('Description:')).append($('<td>').text(weather)));
                tbody.append($('<tr>').append($('<td>').text('Temperature:')).append($('<td>').text(temperature + 'C')));
                tbody.append($('<tr>').append($('<td>').text('Humidity:')).append($('<td>').text(humidity + '%')));
                table.append(tbody);

                $(".aggregated-table").css("display", "none");
            },
            error: function(xhr, status, error) {
              }
        });
    });
});
