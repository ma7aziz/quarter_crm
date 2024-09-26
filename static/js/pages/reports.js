// generate random colors
function generateRandomColors(numColors) {
    var colors = [];
    for (var i = 0; i < numColors; i++) {
        var r = Math.floor(Math.random() * 256);
        var g = Math.floor(Math.random() * 256);
        var b = Math.floor(Math.random() * 256);
        var color = "rgb(" + r + ", " + g + ", " + b + ")";
        colors.push(color);
    }
    return colors;
}

let start_date = document.getElementById("startDate").value;
let end_date = document.getElementById("endDate").value;
// service distributions
var service_ctx = document.getElementById("service-chart").getContext("2d");
let numElements = 0;

$.ajax({
    url: "/service_chart?start_date=" + start_date + "&end_date=" + end_date,
    method: "GET",
    success: function (data) {
        var chart = new Chart(service_ctx, {
            type: "pie",
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: "الطلبات",
                        data: data.counts,
                        backgroundColor: [
                            "rgba(75, 192, 192, 0.5)",
                            "rgba(75, 192, 192, 0.3)",
                            "rgba(75, 192, 192, 0.7)",
                        ],
                        borderColor: [
                            "rgb(75, 192, 192)",
                            "rgb(75, 192, 192)",
                            "rgb(75, 192, 192)",
                        ],
                    },
                ],
            },
            options: {
                responsive: true,
            },
        });
    },
    error: function () {
        console.log("Error retrieving chart data.");
    },
});

// user performance
var user_chart = document.getElementById("user-performance").getContext("2d");

$.ajax({
    url:
        "/sales_performance_chart?start_date=" +
        start_date +
        "&end_date=" +
        end_date,
    method: "GET",
    success: function (data) {
        var chart = new Chart(user_chart, {
            type: "bar",
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: "طلبات المستخدمين",
                        data: data.counts,
                        backgroundColor: generateRandomColors(
                            data.counts.length
                        ),
                        borderWidth: 1,
                    },
                ],
            },
            options: {
                responsive: true,
                scales: {
                    yAxes: [
                        {
                            ticks: {
                                beginAtZero: true,
                            },
                        },
                    ],
                },
            },
        });
    },
    error: function () {
        console.log("Error retrieving chart data.");
    },
});

// daily sales
let sales_chart = document.getElementById("daily-sales").getContext("2d");

$.ajax({
    url:
        "/daily_performance_chart?start_date=" +
        start_date +
        "&end_date=" +
        end_date,
    method: "GET",
    success: function (data) {
        console.log("Data received:", data);
        var chart = new Chart(sales_chart, {
            type: "line",
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: "الطلبات اليومية",
                        data: data.counts,
                        fill: false,
                        borderColor: "rgb(75, 192, 192)",
                        borderWidth: 1,
                    },
                ],
            },
            options: {
                scales: {
                    xAxes: [
                        {
                            type: "time",
                            time: {
                                unit: "day",
                                displayFormats: {
                                    day: "d MMM",
                                },
                            },
                        },
                    ],
                    yAxes: [
                        {
                            ticks: {
                                beginAtZero: true,
                            },
                        },
                    ],
                },
            },
        });
    },
    error: function () {
        console.log("Error retrieving chart data.");
    },
});
