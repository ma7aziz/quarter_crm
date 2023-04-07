
//select2 
$('#customerSelect').select2({
    placeholder: 'اختر من القائمة ',
    minimumInputLength: 2,
    ajax: {
        url: "/api/customers",
        dataType: 'json',
        delay: 250,
        data: function (params) {
          return {
            q: params.term,
            page: params.page
          };
        },
    processResults: function (data, params) {
        console.log(data)
        params.page = params.page || 1;
        return {
            results: $.map(data, function (customer) {
                console.log(customer)
                return {
                    text: customer.name ,
                    id: customer.id,
                    phone_number : customer.phone_number,
                    address: customer.address,
                    city : customer.city ,
                }
            })
        }; 
    },
        cache: true
    },
}).on('change', function(e) {
    var customerId = $(this).val();
    if(customerId) {
        var customerData = $(this).select2('data')[0];
        var name = customerData.text;
        var address = customerData.address;
        var city = customerData.city;
        let phone_number = customerData.phone_number
        console.log(name, address, city);
        $('#cust_address').val(address)
        $('#cust_city').val(city)
        $('#cust_phone').val(phone_number)

        // 
    }
});


