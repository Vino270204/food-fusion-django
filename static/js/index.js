/* ================= MOBILE MENU ================= */

function toggleMenu() {

    const nav = document.querySelector(".nav-menu");
    const right = document.querySelector(".nav-right");

    if (!nav || !right) {
        return;
    }

    nav.classList.toggle("mobile-show");
    right.classList.toggle("mobile-show");

}


/* ================= FAVORITE ================= */

function addFavorite(element) {

    element.classList.toggle("liked");

    const icon = element.querySelector("i");

    if (!icon) {
        return;
    }

    if (element.classList.contains("liked")) {

        icon.classList.remove("fa-regular");
        icon.classList.add("fa-solid");

    } else {

        icon.classList.remove("fa-solid");
        icon.classList.add("fa-regular");

    }

}


/* ================= CLOSE MODAL ================= */

function closeModal(id) {

    const modal = document.getElementById(id);

    if (modal) {
        modal.classList.remove("show");
    }

}


/* ================= OPEN LOGIN ================= */

function openLogin() {

    const modal = document.getElementById(
        "loginModal"
    );

    if (modal) {
        modal.classList.add("show");
    }

}


/* ================= OPEN SIGNUP ================= */

function openSignup() {

    const modal = document.getElementById(
        "signupModal"
    );

    if (modal) {
        modal.classList.add("show");
    }

}


/* ================= SWITCH SIGNUP ================= */

function switchSignup() {

    closeModal("loginModal");

    openSignup();

}


/* ================= SWITCH LOGIN ================= */

function switchLogin() {

    closeModal("signupModal");

    openLogin();

}


/* ================= OUTSIDE MODAL CLICK ================= */

window.addEventListener(
    "click",
    function (event) {

        const loginModal =
            document.getElementById("loginModal");

        const signupModal =
            document.getElementById("signupModal");


        if (
            loginModal &&
            event.target === loginModal
        ) {

            closeModal("loginModal");

        }


        if (
            signupModal &&
            event.target === signupModal
        ) {

            closeModal("signupModal");

        }

    }
);
document.addEventListener("DOMContentLoaded", function () {

    const menuToggle = document.getElementById("menuToggle");
    const navMenu = document.getElementById("navMenu");

    if (menuToggle && navMenu) {

        menuToggle.addEventListener("click", function () {

            navMenu.classList.toggle("active");

        });

    }

});