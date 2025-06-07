function handleSubmit(event) {
  event.preventDefault();
  const email = document.getElementById("email").value;

  fetch("/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email }),
  })
    .then((res) => res.text())
    .then((msg) => {
      alert("You're on the list! 📨");
      document.getElementById("email").value = "";
    })
    .catch((err) => {
      alert("Something went wrong.");
      console.error(err);
    });
}
