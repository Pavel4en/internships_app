document.addEventListener("DOMContentLoaded", function() {
    var registerButton = document.getElementById("register-button");
    var loginButton = document.getElementById("login-button");
    var registerModal = document.getElementById("register-modal");
    var closeModal = document.getElementsByClassName("modal")[0];
  
    registerButton.addEventListener("click", function() {
      registerModal.style.display = "block";
    });
  
    loginButton.addEventListener("click", function() {
      // Обработка нажатия кнопки "Авторизация"
    });
  
    closeModal.addEventListener("click", function() {
      registerModal.style.display = "none";
    });
  
    var customerRegisterButton = document.getElementById("customer-register");
    var internRegisterButton = document.getElementById("intern-register");
    var LoginButton = document.getElementById("login-button");
  
    customerRegisterButton.addEventListener("click", function() {
      window.location.href = "/register/customer"; 
    });
  
    internRegisterButton.addEventListener("click", function() {
      window.location.href = "/register/intern"; 
    });

    LoginButton.addEventListener("click", function() {
        window.location.href = "/login"; 
      });
});
