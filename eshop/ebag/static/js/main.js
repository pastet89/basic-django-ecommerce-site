 AOS.init({
 	duration: 800,
 	easing: 'slide',
 	once: true
 });

jQuery(document).ready(function($) {

	"use strict";
    /*
     * 
     * Custom app functions
     * 
     * 
     * */
    $('.noclick').click(function(e){
       e.preventDefault();
    });
    
    $(".modify-quantity").click(function(){
        /*
        * Updates the product quantity on the
        * category page when the user clicks on the
        * plus/minus buttons.
        */
        let element_data = $(this).attr("id").split("_");
        let product_id = element_data[1];
        let action = element_data[0];
        let min_val = 0;
        if (action=="increase") {
            $("#quantity_"+product_id).val(
                parseInt($("#quantity_"+product_id).val())+1
            );
        } else if  (action=="decrease") {
            let new_value = parseInt($("#quantity_"+product_id).val())-1;
            new_value = (new_value < min_val) ? min_val : new_value
           $("#quantity_"+product_id).val(new_value);
        } else {
            alert("Quantity modification error!");
        }
        return false;
    });

    function update_cart_count(items_num=-1) {
        /*
        * Updates the cart indicator showing the number
        * of products in the cart and respectively hides it
        * if there are no products inside.
        */
        if (items_num < 0) {
            items_num = items_in_cart;
        }
        if (items_num < 1) {
            $('#cart_counter').addClass('invisible');
        }
        else {
            $('#cart_counter').removeClass('invisible');
            $('#cart_counter').html(items_num);
        }
    }
    
    function update_cart_prices_html() {
        /*
        * Updates the product totals (price * quantity)
        * and the cart total at the cart page. Called
        * when the user changes the product quantity
        * or removes a product. If the product quantity
        * is set to zero, removes the product.
        */
       let total_cart_amount = 0;
        $(".cart-item").each(function () {
            let quantity = parseInt($(this).find('.item-quantity').val());
            if (quantity < 1) {
                $(this).fadeOut(400, function(){
                   $(this).remove(); 
                });
            } else {
                let unit_price = parseFloat(
                    $(this).find('.price-placeholder').html()
                );
                let total_price = quantity * unit_price;
                total_cart_amount += total_price;
                $(this).find('.total-placeholder').html(total_price.toFixed(2));
            }
        });
        $('#total-cart-placeholder').html(total_cart_amount);
    }
    
    function get_product_cart_data(element) {
        /*
        * Extracts the product id and quantity
        * from a given HTML element.
        */
        let product_id = element.attr("id").split("_").pop();
        let quantity = $("#quantity_"+product_id).val();
        return {
            "product_id": product_id,
            "quantity": quantity
        };
    }
    
    function send_ajax_cart_data(update_or_add, items) {
        /*
        * Sends via AJAX a POST request to the back-end so that the
        * cart is updated in the session. Called both on the category
        * and cart pages. Updates the HTML after a successful request.
        */
        $.post( "/cart/"+update_or_add+"/", {
                "csrfmiddlewaretoken": csrf_token,
                "items": JSON.stringify(items)
        }).done(function(data) {
            if (data.success == 1) {
                if (update_or_add == "add") {
                    update_cart_count(data.items_in_cart);
                } else if (update_or_add == "update") {
                    update_cart_count(data.items_in_cart);
                    update_cart_prices_html();
                }
            } else {
                alert("AJAX error:\n" + data.err_msg);
            }
        });
    }
    
    $(".add-to-cart").click(function(){
        /*
        * Calls send_ajax_cart_data() from the category page
        * when new products are added to the cart or their
        * quantity is modified.
        */
        let product_data = get_product_cart_data($(this));
        let items = [product_data];
        send_ajax_cart_data("add", items);
    });
        
    function update_cart() {
        /*
        * Calls send_ajax_cart_data() from the cart page
        * when the products quantity is modified or they
        * are removed.
        */
        let items = [];
        $(".cart-item").each(function () {
            let product_data = get_product_cart_data($(this));
            items.push(product_data);
        });
        send_ajax_cart_data("update", items);
    }
    
    $(".update-cart").click(function(){
        /*
        * Updates the cart, triggered on the cart page.
        */
        update_cart();
    });
    
    $(".remove-item").click(function(){
        /*
        * Triggered on the cart page. Removes a product
        * by setting its quantity to 0 after hiding it
        * visually and calling update_cart().
        */
        let product_id = $(this).attr("id").split("_").pop();
        $("#product_"+product_id).fadeOut(400, function(){
            $("#quantity_"+product_id).val(0);
            update_cart();
        });
    });
    
    update_cart_count();
    if (window.location.pathname == "/cart/") {
        update_cart_prices_html();
    }

    /*
     * 
     * Built-in template functions
     * 
     * 
     * */
	var slider = function() {
		$('.nonloop-block-3').owlCarousel({
	    center: false,
	    items: 1,
	    loop: false,
			stagePadding: 15,
	    margin: 20,
	    nav: true,
			navText: ['<span class="icon-arrow_back">', '<span class="icon-arrow_forward">'],
	    responsive:{
        600:{
        	margin: 20,
          items: 2
        },
        1000:{
        	margin: 20,
          items: 3
        },
        1200:{
        	margin: 20,
          items: 3
        }
	    }
		});
	};
	slider();


    
	var siteMenuClone = function() {

		$('<div class="site-mobile-menu"></div>').prependTo('.site-wrap');

		$('<div class="site-mobile-menu-header"></div>').prependTo('.site-mobile-menu');
		$('<div class="site-mobile-menu-close "></div>').prependTo('.site-mobile-menu-header');
		$('<div class="site-mobile-menu-logo"></div>').prependTo('.site-mobile-menu-header');

		$('<div class="site-mobile-menu-body"></div>').appendTo('.site-mobile-menu');

		

		$('.js-logo-clone').clone().appendTo('.site-mobile-menu-logo');

		$('<span class="ion-ios-close js-menu-toggle"></div>').prependTo('.site-mobile-menu-close');
		

		$('.js-clone-nav').each(function() {
			var $this = $(this);
			$this.clone().attr('class', 'site-nav-wrap').appendTo('.site-mobile-menu-body');
		});


		setTimeout(function() {
			
			var counter = 0;
      $('.site-mobile-menu .has-children').each(function(){
        var $this = $(this);
        
        $this.prepend('<span class="arrow-collapse collapsed">');

        $this.find('.arrow-collapse').attr({
          'data-toggle' : 'collapse',
          'data-target' : '#collapseItem' + counter,
        });

        $this.find('> ul').attr({
          'class' : 'collapse',
          'id' : 'collapseItem' + counter,
        });

        counter++;

      });

    }, 1000);

		$('body').on('click', '.arrow-collapse', function(e) {
      var $this = $(this);
      if ( $this.closest('li').find('.collapse').hasClass('show') ) {
        $this.removeClass('active');
      } else {
        $this.addClass('active');
      }
      e.preventDefault();  
      
    });

		$(window).resize(function() {
			var $this = $(this),
				w = $this.width();

			if ( w > 768 ) {
				if ( $('body').hasClass('offcanvas-menu') ) {
					$('body').removeClass('offcanvas-menu');
				}
			}
		})

		$('body').on('click', '.js-menu-toggle', function(e) {
			var $this = $(this);
			e.preventDefault();

			if ( $('body').hasClass('offcanvas-menu') ) {
				$('body').removeClass('offcanvas-menu');
				$this.removeClass('active');
			} else {
				$('body').addClass('offcanvas-menu');
				$this.addClass('active');
			}
		}) 

		// click outisde offcanvas
		$(document).mouseup(function(e) {
	    var container = $(".site-mobile-menu");
	    if (!container.is(e.target) && container.has(e.target).length === 0) {
	      if ( $('body').hasClass('offcanvas-menu') ) {
					$('body').removeClass('offcanvas-menu');
				}
	    }
		});
	}; 
	siteMenuClone();


	var sitePlusMinus = function() {
		$('.js-btn-minus').on('click', function(e){
			e.preventDefault();
			if ( $(this).closest('.input-group').find('.form-control').val() != 0  ) {
				$(this).closest('.input-group').find('.form-control').val(parseInt($(this).closest('.input-group').find('.form-control').val()) - 1);
			} else {
				$(this).closest('.input-group').find('.form-control').val(parseInt(0));
			}
		});
		$('.js-btn-plus').on('click', function(e){
			e.preventDefault();
			$(this).closest('.input-group').find('.form-control').val(parseInt($(this).closest('.input-group').find('.form-control').val()) + 1);
		});
	};
	sitePlusMinus();


	var siteSliderRange = function() {
    $( "#slider-range" ).slider({
      range: true,
      min: 0,
      max: 500,
      values: [ 75, 300 ],
      slide: function( event, ui ) {
        $( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
      }
    });
    $( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) +
      " - $" + $( "#slider-range" ).slider( "values", 1 ) );
	};
	siteSliderRange();


	var siteMagnificPopup = function() {
		$('.image-popup').magnificPopup({
	    type: 'image',
	    closeOnContentClick: true,
	    closeBtnInside: false,
	    fixedContentPos: true,
	    mainClass: 'mfp-no-margins mfp-with-zoom', // class to remove default margin from left and right side
	     gallery: {
	      enabled: true,
	      navigateByImgClick: true,
	      preload: [0,1] // Will preload 0 - before current, and 1 after the current image
	    },
	    image: {
	      verticalFit: true
	    },
	    zoom: {
	      enabled: true,
	      duration: 300 // don't foget to change the duration also in CSS
	    }
	  });

	  $('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
	    disableOn: 700,
	    type: 'iframe',
	    mainClass: 'mfp-fade',
	    removalDelay: 160,
	    preloader: false,

	    fixedContentPos: false
	  });
	};
	siteMagnificPopup();


});
