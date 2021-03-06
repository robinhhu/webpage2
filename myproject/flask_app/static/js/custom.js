jQuery( document ).ready(function( $ ) {


	"use strict";


        // Page loading animation

        $("#preloader").animate({
            'opacity': '0'
        }, 600, function(){
            setTimeout(function(){
                $("#preloader").css("visibility", "hidden").fadeOut();
            }, 300);
        });
        

        $(window).scroll(function() {
          var scroll = $(window).scrollTop();
          var box = $('.header-text').height();
          var header = $('header').height();

          if (scroll >= box - header) {
            $("header").addClass("background-header");
          } else {
            $("header").removeClass("background-header");
          }
        });

        if ($('.owl-clients').length) {
            $('.owl-clients').owlCarousel({
                loop: true,
                nav: false,
                dots: true,
                items: 1,
                margin: 30,
                autoplay: false,
                smartSpeed: 700,
                autoplayTimeout: 6000,
                responsive: {
                    0: {
                        items: 1,
                        margin: 0
                    },
                    460: {
                        items: 1,
                        margin: 0
                    },
                    576: {
                        items: 3,
                        margin: 20
                    },
                    992: {
                        items: 5,
                        margin: 30
                    }
                }
            });
        }

        if ($('.owl-banner').length) {
            $('.owl-banner').owlCarousel({
                loop: true,
                nav: true,
                dots: true,
                items: 3,
                margin: 10,
                autoplay: false,
                smartSpeed: 700,
                autoplayTimeout: 6000,
                responsive: {
                    0: {
                      items: 1,
                      margin: 0
                    },
                    460: {
                        items: 1,
                        margin: 0
                    },
                    576: {
                        items: 1,
                        margin: 10
                    },
                    992: {
                      items: 3,
                      margin: 10
                    }
                }
            });
        }

//add to my like, render the icon when the button is clicked
//that is, if is liked then it should be unliked and vice versa
//also a ajax request is rendered to send request to backend
//so that the information can be stored in a database
    $("#like").click(function () {
        if (this.name == "far") {
            this.innerHTML = "<i class='fas fa-heart'></i>";
            this.name = "fas";

            var content = $("#temp").html();
            $.ajax({
                type: 'POST',
                url: "/likes/".concat(content),
                data: {
                    'id': content
                },
                contentType: 'application/json; charset=UTF-8',
                dataType: 'json',
                success: function (data) {
                    window.history.back();
                }
            });
        }
        else {
            this.innerHTML = "<i class='far fa-heart'></i>";
            this.name = "far";

            var content = $("#temp").html();
            $.ajax({
                type: 'POST',
                url: "/likes/".concat(content),
                data: {
                    'id': content
                },
                contentType: 'application/json; charset=UTF-8',
                dataType: 'json',
                success: function (data) {
                    window.history.back();
                }
            });
        }
     });

//add to my collection, render the icon when the button is clicked
//that is, if is collected then it should be uncollected and vice versa
//also a ajax request is rendered to send request to backend
//so that the information can be stored in a database
    $("#sc").click(function () {
        if (this.name == "far") {
            this.innerHTML = "<i class='fas fa-star'></i>";
            this.name = "fas";

            var content = $("#temp").html();
            $.ajax({
                type: 'POST',
                url: "/collects/".concat(content),
                data: {
                    'id': content
                },
                contentType: 'application/json; charset=UTF-8',
                dataType: 'json',
                success: function (data) {
                    window.history.back();
                }
            });
        }
        else {
            this.innerHTML = "<i class='far fa-star'></i>";
            this.name = "far";

            var content = $("#temp").html();
            $.ajax({
                type: 'POST',
                url: "/collects/".concat(content),
                data: {
                    'id': content
                },
                contentType: 'application/json; charset=UTF-8',
                dataType: 'json',
                success: function (data) {
                    window.history.back();
                }
            });

        }
     });
});

