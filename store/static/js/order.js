function get_form_values() {
    let client_name = $('#id_name').val();
    let email = $('#id_email').val();
    let address = $('#id_address').val();
    let phone = $('#id_phone').val()
    let delivery = $('#id_delivery option:selected').val();
    console.log('Считываем данные введенные пользователем:', client_name, email, address, delivery, phone);
    let url = '/create/'
    if (client_name, email, delivery, phone) {
        $.ajax(url, {
                method: 'POST',
                data: {cn: client_name, email: email, addr: address, delivery: delivery, phone: phone},

                success: function (response) {
                    console.log(response.mes)
                    window.location.href = response.link
                },
                error: function (response) {
                    console.log(response)
                },

            }
        )
    } else {
        alert('Заполнены не все данные')
    }

}