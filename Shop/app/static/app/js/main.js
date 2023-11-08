$(document).ready(() => {
    updateCountProductsInCart();

    function showMessage(text, callback = null) {
        $('body').prepend('<div id="message" class="alert alert-success" style="display: none;">' + text + '</div>');
        $('#message').fadeIn();
        setTimeout(function () {
            $('#message').fadeOut();
            setTimeout(function () {
                $('#message').remove();
                if (callback) callback();
            }, 1000);
        }, 2000);
    }

    function ajaxSetup() {
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", $('[name=csrfmiddlewaretoken]').val());
                }
            }
        });
    }

    function updateCart(count) {
        if (count === 0) {
            $('.cart-count-bg').remove();
        } else {
            if ($('.cart-count-bg').length === 0) {
                $('.cart-button').append('<div class="cart-count-bg"><span class="cart-count">' + count + '</span></div>');
            } else {
                $('.cart-count-bg .cart-count').text(count);
            }
        }
    }

    function search() {
        let query = $('.search-bar input').val();
        if (query.length < 3) {
            alert('Request is too short');
            return;
        }
        window.location.href = '/search/' + query;
    }

    function updateCountProductsInCart() {
        ajaxSetup();
        $.post('/api/get-count-products/in-cart/', {}, (res) => {
            if (res.sc) updateCart(res.count);
        });
    }

    function updateCountFromCart(type, tr) {
        let id = $(tr).find('button').data('id');
        let count = parseInt(tr.find('.count-products').text());
        if (type === 'reduce') count -= 1
        else count += 1
        ajaxSetup();
        $.post('/api/update-count-from-cart/', {id, count}, (res) => {
            if (count < 1) tr.remove();
            else {
                tr.find('.total-price-product').text((count * parseFloat(tr.find('.product-price').text())).toFixed(2));
            }
            if (res.sc) {
                $('.total-price').html(res['total_price'])
                tr.find('.count-products').html(count);
                updateCart(res.count);
                if (res.count === 0) emptyTrash()
            }
        });
    }

    function emptyTrash() {
        updateCart(0);
        $('main .container').html('<div class="alert alert-danger alert-dismissible" role="alert">\n' +
            '                Cart is empty\n' +
            '            </div>');
    }

    $('body').on('click', '.buy', function (e) {
        e.preventDefault();
        let productId = $(this).data('id');
        ajaxSetup();
        $.post('/api/add-to-cart/', {productId}, (res) => {
            if (res.sc) {
                updateCart(res.count)
                showMessage('Product added to cart');
                $(this).replaceWith('<span class="in-cart">In cart</span>');
            }
        });
    });

    $('body').on('click', '.search-bar button', function () {
        search();
    });

    $('body').on('keypress', '.search-bar input', function (e) {
        if (e.which === 13) search();
    });

    $('body').on('click', '.remove-from-cart', function () {
        let id = $(this).data('id');
        ajaxSetup();
        $.post('/api/remove-from-cart/', {id}, (res) => {
            $(this).closest('tr').remove();
            if (res.sc) {
                $('.total-price').html(res['total_price'])
                updateCart(res.count);
                if (res.count === 0) emptyTrash();
            }
        });
    });

    $('body').on('click', '.reduce', function () {
        updateCountFromCart('reduce', $(this).closest('tr'));
    });

    $('body').on('click', '.increase', function () {
        updateCountFromCart('increase', $(this).closest('tr'));
    });

    $('body').on('click', '.checkout', function () {
        ajaxSetup();
        $.post('/api/checkout/', {}, (res) => {
            if (res.sc) {
                emptyTrash();
                showMessage('Your order has been placed');
            }
        });
    });

    $('#profile').submit(function (e) {
        e.preventDefault();
        let email = $('#profile input[name="email"]').val();
        let password = $('#profile input[name="password"]').val();
        let confirm_password = $('#profile input[name="confirm_password"]').val();
        let username = $('#profile input[name="username"]').val();
        let surname = $('#profile input[name="surname"]').val();
        let phoneNumber = $('#profile input[name="phoneNumber"]').val();
        let address = $('#profile input[name="address"]').val();

        console.log(email)

        if (email.length === 0 || password.length === 0 || confirm_password.length === 0 || username.length === 0 ||
            surname.length === 0 || phoneNumber.length === 0 || address.length === 0) {
            showMessage('Fill in all the fields');
        } else {
            ajaxSetup();
            $.post('/api/update_profile/', {
                email, password, confirm_password, username, surname, phoneNumber, address
            }, (res) => {
                if (res.sc) {
                    showMessage('Data updated', () => {
                        location.href = '/login/';
                    });
                } else {
                    showMessage(res.error);
                }
            });
        }
    });
});