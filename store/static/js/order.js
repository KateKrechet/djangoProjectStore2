function get_form_values() {
    let client_name = $('#id_name').val();
    let email = $('#id_email').val();
    let address = $('#id_address').val();
    let phone = $('#id_phone').val()
    let delivery = $('#id_delivery option:selected').val();
    const pattern_phone = /^\+\d{11}$/
    const pattern_email = /[^\s]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/
    let url = '/create/'
    if (client_name === "" || email === "" || address === "" || phone === "") {
        alert('Заполните все необходимые данные в формате по образцу!')
    } else if (!email.match(pattern_email)) {
        alert('Заполните адрес электронной почты по образцу!')
    } else if (!phone.match(pattern_phone)) {
        alert('Заполните номер мобильного телефона по образцу!')
    } else {
        console.log('Считываем данные введенные пользователем:', client_name, email, address, delivery, phone);
        $.ajax(url, {
                method: 'POST',
                data: {
                    'cn': client_name,
                    'email': email,
                    'addr': address,
                    'delivery': delivery,
                    'phone': phone

                },

                success: function (data) {
                    console.log('Ответ с сервера получен', data.order_id, data.itog1, data.itog2)
                    $('#result').html('Номер вашего заказа:' + data.order_id + '. Для окончательного подтверждения заказа наш специалист свяжется с вами.')
                    $('#cost_discount').html('Стоимость с учетом персональной скидки (руб.):' + data.itog1)
                    $('#cost_discount_delivery').html('Итоговая стоимость с учетом доставки (руб.):' + data.itog2)
                    $('#go_home').html('Вернуться к покупкам')
                    $('#go_pay').html('Оплатить')

                },
                error: function (error) {
                    console.log('Error retrieving dependent options:', error)
                },


            }
        )

    }


}

