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
      alert("thank you. you're on the waitlist.");
      document.getElementById("email").value = "";
    })
    .catch((err) => {
      alert("something went wrong.");
      console.error(err);
    });
}
