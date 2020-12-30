window.addEventListener("load",function(){
    window.cookieconsent.initialise({
    palette:{
     popup: {background: "#fff"},
     button: {background: "#aa0000"},
    },
    revokable:true,
    onStatusChange: function(status) {
     console.log(this.hasConsented() ?
      'enable cookies' : 'disable cookies');
    },
    content: {
         message: "The website uses cookies so that we can remember you for your next login.",
    },

   });
});