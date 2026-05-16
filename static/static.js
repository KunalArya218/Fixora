// =========================
// FIXORA SECURITY SCRIPT (CLEANED)
// =========================

// 🚫 Disable Right Click
document.addEventListener("contextmenu", (e) => e.preventDefault());

// 🚫 Disable Text Selection
document.addEventListener("selectstart", (e) => e.preventDefault());

// 🚫 Disable Copy
document.addEventListener("copy", (e) => e.preventDefault());

// 🚫 Disable Drag
document.addEventListener("dragstart", (e) => e.preventDefault());

// =========================
// FLASH AUTO REMOVE
// =========================

setTimeout(() => {

    const flashMessages = document.querySelectorAll(".flash");

    flashMessages.forEach(msg => {
        msg.style.opacity = "0";
        setTimeout(() => msg.remove(), 500);
    });

}, 5000);

// =========================
// EMAIL TOGGLE (CLEAN)
// =========================

document.addEventListener("DOMContentLoaded", () => {

    const emailToggle = document.getElementById("emailToggle");
    const sendReplyInput = document.getElementById("sendReplyInput");

    if (!emailToggle || !sendReplyInput) return;

    let enabled = false;

    emailToggle.addEventListener("click", () => {

        enabled = !enabled;

        if (enabled) {

            emailToggle.innerText = "Send Email";
            emailToggle.classList.add("active");
            emailToggle.classList.remove("inactive");

            sendReplyInput.value = "true";

        } else {

            emailToggle.innerText = "Send Email";
            emailToggle.classList.remove("active");
            emailToggle.classList.add("inactive");

            sendReplyInput.value = "false";
        }

    });

});

function validateReply(){

    const replyBox =
        document.getElementById(
            "reply_message"
        );

    if(replyBox.value.trim() === ""){

        alert(
            "Reply message is required for sending email!"
        );

        return false;
    }

    return true;
}


console.log("Fixora Loaded Successfully 🚀");