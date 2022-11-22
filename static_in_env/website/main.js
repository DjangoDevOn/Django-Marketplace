
$('.owl-carousel').owlCarousel({
  margin: 15,
  nav: true,
  navText: ["<i class='carousel-control-prev-icon'></i>", "<i class='carousel-control-next-icon'></i>"],
  responsive: {
    0: {
      items: 1
    },
    600: {
      items: 2
    },
    1000: {
      items: 3
    }
  }
});
