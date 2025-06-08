const form = document.getElementById("waitlist-form");
const messageDiv = document.getElementById("form-message");

form.addEventListener("submit", async function (e) {
  e.preventDefault();

  const email = document.getElementById("email").value;

  try {
    const res = await fetch("https://formspree.io/f/xjkryvgo", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json"
      },
      body: JSON.stringify({ email: email }) // Make sure it's a plain object
    });

    const result = await res.json();

    if (res.ok) {
      form.style.display = "none";
      messageDiv.innerHTML = "<p>thank you. you're on the waitlist ✨</p>";
    } else {
      console.error("Formspree error:", result);
      messageDiv.innerHTML = "<p>something went wrong. please try again.</p>";
    }
  } catch (err) {
    console.error("Network error:", err);
    messageDiv.innerHTML = "<p>error submitting form. check your connection.</p>";
  }
});
