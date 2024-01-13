

function get_form_values() {
    let client_name = $('#id_name').val();
    let email = $('#id_email').val();
    let address = $('#id_address').val();
    let phone = $('#id_phone').val()
    let delivery = $('#id_delivery option:selected').val();
    console.log('Считываем данные введенные пользователем:', client_name, email, address, delivery, phone);

    if (client_name, email, delivery, phone) {
        $.ajax({
            method: 'POST',
            url: '/create/',
            data: {
                "type": 'for_cost',
                'cn': client_name,
                'email': email,
                'addr': address,
                'delivery': delivery,
                'phone': phone

            },

            success: function (data) {
                console.log('Ответ с сервера получен', data.order_id, data.itog1, data.itog2)
                $('#result').html('Номер вашего заказа:'+ data.order_id + '. Для окончательного подтверждения заказа наш специалист свяжется с вами.')
                $('#cost_discount').html('Стоимость с учетом персональной скидки (руб.):'+ data.itog1)
                $('#cost_discount_delivery').html('Итоговая стоимость с учетом доставки (руб.):'+ data.itog2)
                $('#go_home').html('Вернуться к покупкам')

            },
            error: function (error) {
                console.log('Error retrieving dependent options:', error)
            }


        })

    } else {
        alert('Заполнены не все данные')
    }

}